from core import exceptions, conf, utils, schemas, email, crypto
from core.database import Session, get_db, User, Notification, Book, BookUser, ActionToken
from sqlalchemy import and_
from fastapi import FastAPI, HTTPException, Depends, Request, Header, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi_restful.tasks import repeat_every
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime, timedelta
from typing import Any, Union, List
from fastapi_jwt_auth import AuthJWT
from uuid import UUID
import stripe

app = FastAPI(docs_url=None, redoc_url=None)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
exceptions.init(app)
stripe.api_key = crypto.decode_sec("stripe_key")
AuthJWT.load_config(schemas.JWTSettings)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST", "GET", "OPTIONS"], allow_headers=["*"])

#=============================================#
#== MIDDLEWARE ===============================#
#=============================================#

@app.middleware("http")
async def log_requests(req:Request, call_next):
    res = await call_next(req)
    return res

#=============================================#
#== AUTH INFO ================================#
#=============================================#

@app.get("/auth-info")
async def auth_info(request:Request, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.AuthInfo:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    user.last_activity_date = datetime.now()
    next_credit_date = None
    if user.last_book_credit_date and user.sub_current_period_end:
        last_plus_interval = user.last_book_credit_date + timedelta(days=conf.INTERVAL_NEW_BOOK)
        if not user.sub_cancel_at_period_end or last_plus_interval < user.sub_current_period_end:
            next_credit_date = last_plus_interval
    steps = schemas.Steps(is_sub=user.sub, set_pref=user.step_set_pref, pick_first_book=user.step_pick_first_book)
    settings = schemas.Settings(reader_theme=user.setting_reader_theme, reader_font=user.setting_reader_font, reader_zoom=user.setting_reader_zoom, library_sorting=user.setting_library_sorting)
    email_preferences = schemas.EmailPreferences(new_book=user.email_pref_new_book, ref_someone=user.email_pref_ref_someone, sub_will_expire=user.email_pref_sub_will_expire, promo=user.email_pref_promo)
    unread_notif_count = db.count(Notification, and_(Notification.user_id == user.id, Notification.opened == False))
    return schemas.AuthInfo(steps=steps, settings=settings, email_preferences=email_preferences, sub_since=user.sub_since, sub_discount=user.sub_discount, sub_current_period_end=user.sub_current_period_end, sub_cancel_at_period_end=user.sub_cancel_at_period_end, next_credit_date=next_credit_date, book_credit=user.book_credit, unread_notifications=unread_notif_count, referral_code=user.referral_code, email=user.email)

#=============================================#
#== REGISTER =================================#
#=============================================#

@app.post("/register")
@limiter.limit(conf.LIMIT_SIGNIN)
async def register(request:Request, background_tasks:BackgroundTasks, data:schemas.Credentials, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.AccessToken:
    if db.search(User, User.email == data.email):
        raise HTTPException(409, conf.MSG_EMAIL_ALREADY_EXISTS)
    customer = stripe.Customer.create(email=data.email)
    user = db.create(User(email=data.email, hashed_password=crypto.hash_password(data.password), stripe_customer_id=customer.id))
    try: 
        exp = datetime.now() + timedelta(seconds=conf.EXPIRATION_EMAIL_CONFIRMATION_TOKEN)
        token = db.create(ActionToken(user_id=user.id, type=schemas.ActionTokenType.EMAIL_CONFIRMATION.value, expiration_date=exp))
        background_tasks.add_task(email.send_welcome, user.email, token.id) 
    except: pass
    return utils.create_access_token(auth, user.id)

#=============================================#
#== LOGIN ====================================#
#=============================================#

@app.post("/login")
@limiter.limit(conf.LIMIT_LOGIN)
async def login(request:Request, data:schemas.Credentials, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.AccessToken:
    user = db.search(User, User.email == data.email)
    if not user or not crypto.is_valid_password(data.password, user.hashed_password): 
        raise HTTPException(401, conf.MSG_BAD_CREDENTIALS)   
    user.last_activity_date = datetime.now()
    return utils.create_access_token(auth, user.id)

#=============================================#
#== SUBSCRIBE ================================#
#=============================================#

@app.post("/subscribe")
@limiter.limit(conf.LIMIT_PROMO_CODE_VALIDATION)
async def subscribe(request:Request, code:Any = None, referrer:Any = None, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.Subscribe:
    auth.jwt_required()
    try: schemas.ReferralCode(code=referrer)
    except: referrer = "nobody"
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    if user.sub:
        raise HTTPException(409, conf.MSG_ALREADY_MEMBER)
    try: new_sub = stripe.Subscription.create(customer=user.stripe_customer_id, items=[{"price": conf.STRIPE_PRODUCT_ID}], payment_behavior="default_incomplete", payment_settings={"save_default_payment_method": "on_subscription", "payment_method_types": ["card"]}, expand=["latest_invoice.payment_intent"], metadata={"user_id":user.id, "ref":referrer})
    except: raise HTTPException(406, conf.MSG_NOT_ELIGIBLE)
    return schemas.Subscribe(client_secret=new_sub.latest_invoice.payment_intent.client_secret, invoice=new_sub.latest_invoice.id, is_first_sub=(not user.step_sub_once))

#=============================================#
#== PROMO-CODE-VALIDATION ====================#
#=============================================#

@app.get("/promo-code-validation")
@limiter.limit(conf.LIMIT_PROMO_CODE_VALIDATION)
async def promo_code_validation(request:Request, code:str, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.PromoValidation:
    auth.jwt_required()
    try: schemas.PromoCode(code=code)
    except: raise HTTPException(404, conf.MSG_PROMO_CODE_NOT_FOUND)
    user = db.get(User, auth.get_jwt_subject())
    if user.sub_discount:
        raise HTTPException(409, conf.MSG_ALREADY_REF_PROMO)
    result = stripe.PromotionCode.list(code=code, active=True)
    if len(result.data) != 1:
        raise HTTPException(404, conf.MSG_PROMO_CODE_NOT_FOUND)
    if result.data[0].restrictions.first_time_transaction and user.step_sub_once:
        raise HTTPException(403, conf.MSG_NOT_ELIGIBLE)
    if result.data[0].customer is not None and result.data[0].customer != user.stripe_customer_id:
        raise HTTPException(403, conf.MSG_NOT_ELIGIBLE)
    return schemas.PromoValidation(code=result.data[0].code, description=result.data[0].coupon.name)

#=============================================#
#== PREFERENCES ==============================#
#=============================================#

@app.post("/preferences")
async def preferences(request:Request, data:schemas.Preferences, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    for key, value in dict(data).items():
        if value == True:
            setattr(user, key, 1)
        else:
            setattr(user, key, 0)
    user.step_set_pref = True
    return schemas.ResponseSuccess()

#=============================================#
#== CHANGE EMAIL PREFERENCES =================#
#=============================================#

@app.post("/change-email-preferences")
async def change_email_preferences(request:Request, data:schemas.EmailPreferences, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    user.email_pref_new_book = data.new_book
    user.email_pref_ref_someone = data.ref_someone
    user.email_pref_sub_will_expire = data.sub_will_expire
    user.email_pref_promo = data.promo
    return schemas.ResponseSuccess()

#=============================================#
#== CHANGE SETTINGS ==========================#
#=============================================#

@app.post("/change-settings")
async def change_settings(request:Request, data:schemas.Settings, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    user.setting_reader_theme = data.reader_theme
    user.setting_reader_zoom = data.reader_zoom
    user.setting_reader_font = data.reader_font
    user.setting_library_sorting = data.library_sorting
    return schemas.ResponseSuccess()

#=============================================#
#== CANCEL SUBSCRIPTION ======================#
#=============================================#

@app.post("/cancel-subscription")
async def cancel_subscription(request:Request, data:schemas.CancelSubscription, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    if not user.sub:
        raise HTTPException(404, conf.MSG_NOT_MEMBER)
    stripe.Subscription.modify(user.sub_id, cancel_at_period_end=data.state).cancel_at_period_end
    return schemas.ResponseSuccess()

#=============================================#
#== CHANGE PASSWORD ==========================#
#=============================================#

@app.post("/change-password")
@limiter.limit(conf.LIMIT_CHANGE_PASSWORD)
async def change_password(request:Request, data:schemas.ChangePassword, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    if data.old_password == data.new_password:
        raise HTTPException(409, conf.MSG_PASSWORDS_ARE_IDENTICAL)
    if not utils.is_valid_password(data.old_password, user.hashed_password): 
        raise HTTPException(401, conf.MSG_BAD_PASSWORD)  
    user.hashed_password = crypto.hash_password(data.new_password)
    return schemas.ResponseSuccess()

#=============================================#
#== PASSWORD RECOVERY ========================#
#=============================================#

@app.get("/password-recovery-email")
@limiter.limit(conf.LIMIT_PASSWORD_RECOVERY)
async def password_recovery_email(request:Request, background_tasks:BackgroundTasks, send_to:str = Query(regex=conf.REGEX_EMAIL), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    user = db.search(User, User.email == send_to)
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    exp = datetime.now() + timedelta(seconds=conf.EXPIRATION_PASSWORD_RECOVERY_TOKEN)
    token = db.create(ActionToken(user_id=user.id, type=schemas.ActionTokenType.PASSWORD_RECOVERY.value, expiration_date=exp))
    background_tasks.add_task(email.send_password_recovery, user.email, token.id)
    return schemas.ResponseSuccess()

@app.post("/password-recovery")
@limiter.limit(conf.LIMIT_PASSWORD_RECOVERY)
async def password_recovery(request:Request, data:schemas.PasswordRecovery, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.AccessToken:
    token = db.get(ActionToken, data.token)
    if not token or token.type != schemas.ActionTokenType.PASSWORD_RECOVERY.value:
        raise HTTPException(401, conf.MSG_BAD_TOKEN)
    elif token.used:
        raise  HTTPException(409, conf.MSG_BAD_TOKEN)
    elif datetime.now().timestamp() > token.expiration_date.timestamp():
        raise  HTTPException(410, conf.MSG_BAD_TOKEN)
    user = db.get(User, token.user_id)
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    token.used = True
    user.hashed_password = crypto.hash_password(data.new_password) 
    return utils.create_access_token(auth, user.id)

#=============================================#
#== EMAIL CONFIRMATION =======================#
#=============================================#

@app.post("/email-confirmation")
async def email_confirmation(request:Request, data:schemas.ConfirmEmail, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    token = db.get(ActionToken, data.token)
    if not token or token.type != schemas.ActionTokenType.EMAIL_CONFIRMATION.value:
        raise HTTPException(401, conf.MSG_BAD_TOKEN)
    elif token.used:
        raise  HTTPException(409, conf.MSG_BAD_TOKEN)
    elif (datetime.now().timestamp() > token.expiration_date.timestamp() or not token.active):
        raise  HTTPException(410, conf.MSG_BAD_TOKEN)
    user = db.get(User, token.user_id)
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    token.used = True
    user.step_confirm_email = True
    return schemas.ResponseSuccess()

#=============================================#
#== CHANGE EMAIL =============================#
#=============================================#

@app.post("/change-email")
@limiter.limit(conf.LIMIT_CHANGE_EMAIL)
async def change_email(request:Request, background_tasks: BackgroundTasks, data:schemas.ChangeEmailAddress, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    if db.search(User, User.email == data.new_email):
        raise HTTPException(409, conf.MSG_EMAIL_ALREADY_EXISTS)
    user.email = stripe.Customer.modify(user.stripe_customer_id, email=data.new_email).email
    user.step_confirm_email = False
    tokens = db.search_all(ActionToken, and_(ActionToken.user_id == user.id, ActionToken.type == schemas.ActionTokenType.EMAIL_CONFIRMATION.value, ActionToken.active == True))
    for token in tokens:
        token.active = False
    try:   
        exp = datetime.now() + timedelta(seconds=conf.EXPIRATION_EMAIL_CONFIRMATION_TOKEN)
        token = db.create(ActionToken(user_id=user.id, type=schemas.ActionTokenType.EMAIL_CONFIRMATION.value, expiration_date=exp))
        background_tasks.add_task(email.send_change_email, user.email, token.id) 
    except: pass
    return schemas.ResponseSuccess()

#=============================================#
#== PASS BOOK ================================#
#=============================================#

@app.post("/pass-book")
async def pass_book(request:Request, data:schemas.PassBook, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    try:
        db.create(BookUser(user_id=auth.get_jwt_subject(), book_id=data.book_id, rating=data.book_rating))
    except:
        raise HTTPException(406, conf.MSG_NOT_ACCEPTABLE) 
    return schemas.ResponseSuccess()
    
#=============================================#
#== RATE BOOK ================================#
#=============================================#

@app.post("/rate-book")
async def rate_book(request:Request, data:schemas.RateBook, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    book_user = db.search(BookUser, and_(BookUser.user_id == auth.get_jwt_subject(), BookUser.book_id == data.book_id))
    if not book_user:
        raise HTTPException(404, conf.MSG_BOOK_NOT_FOUND)
    book_user.rating = data.book_rating
    return schemas.ResponseSuccess()

#=============================================#
#== GET NEW BOOK =============================#
#=============================================#

@app.get("/new-book")
async def new_book(request:Request, id:UUID, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    if user.book_credit < 1:
        raise HTTPException(412, conf.MSG_NOT_ENOUGH_CREDIT)
    try:
        db.create(BookUser(user_id=auth.get_jwt_subject(), book_id=id, is_in_library=True, progress=0, progress_chapter=0, added_in_library_date=datetime.now(), last_activity_date=datetime.fromtimestamp(0)))
    except:
        raise HTTPException(406, conf.MSG_NOT_ACCEPTABLE) 
    user.book_credit = user.book_credit - 1
    user.book_credit_spent = user.book_credit_spent + 1
    if not user.step_pick_first_book:
        user.step_pick_first_book = True
    return schemas.ResponseSuccess()

#=============================================#
#== GET BOOK =================================#
#=============================================#

@app.get("/book")
async def book(request:Request, id:UUID, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.Book:
    auth.jwt_required()
    book = db.get_book(auth.get_jwt_subject(), id)
    if not book:
        raise HTTPException(404, conf.MSG_BOOK_NOT_FOUND)
    return book

#=============================================#
#== LIBRARY ==================================#
#=============================================#

@app.get("/library")
async def library(request:Request, sort:schemas.LibrarySorting, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> list[schemas.BookLibrary]:
    auth.jwt_required()
    return db.get_library(auth.get_jwt_subject(), sort)

#=============================================#
#== NOTIFICATION =============================#
#=============================================#

@app.get("/notifications")
async def notifications(request:Request, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> List[schemas.Notification]:
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    unread_notif = db.search_all(Notification, and_(Notification.user_id == user_id, Notification.opened == False), by=Notification.date)
    unread_counter = len(unread_notif)
    for n in unread_notif:
        n.opened = True
    return db.get_notifications(user_id, (conf.DEFAULT_NB_NOTIF if conf.DEFAULT_NB_NOTIF > unread_counter else unread_counter))

#=============================================#
#== RECOMMENDATION ===========================#
#=============================================#

@app.get("/recommendation")
async def recommendation(request:Request, book_id:Union[UUID, None] = None, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.Recommendation:
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    if book_id:
        book = db.get(Book, book_id)
        if not book:
            raise HTTPException(404, conf.MSG_BOOK_NOT_FOUND)
        book_user = db.search(BookUser, and_(BookUser.user_id == user_id, BookUser.book_id == book_id))
        if book_user:
            if book_user.is_in_library:
                raise HTTPException(409, conf.MSG_BOOK_EXISTS)
            else:
                db.delete(book_user)
        return schemas.Recommendation.from_orm(book)
    else:
        book = db.get_recommendation(user_id)
        if not book: 
            db.delete_passed(user_id)
            book = db.get_recommendation(user_id)
        if not book: 
            raise HTTPException(410, conf.MSG_BOOK_NOT_FOUND)
        return schemas.Recommendation.from_orm(book)

#=============================================#
#== SAVE PROGRESS ============================#
#=============================================#

@app.post("/save-progress")
async def save_progress(request:Request, data:schemas.SaveProgress, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    book = db.search(BookUser, and_(BookUser.book_id == data.book_id, BookUser.user_id == user_id))
    if not book:
        raise HTTPException(404, conf.MSG_BOOK_NOT_FOUND)
    book.chapter = data.chapter
    book.progress_chapter = data.progress_chapter
    if data.progress_book > 0:
        book.progress = data.progress_book
    book.last_activity_date = datetime.now()
    return schemas.ResponseSuccess()

#=============================================#
#== PROGRESS =================================#
#=============================================#

@app.get("/progress")
async def progress(request:Request, book_id:UUID, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.Progress:
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    progress = db.get_progress(user_id, book_id)
    if not progress:
        raise HTTPException(404, conf.MSG_BOOK_NOT_FOUND)
    return progress

#=============================================#
#== REPORT ===================================#
#=============================================#

@app.post("/report")
@limiter.limit(conf.LIMIT_REPORT)
async def report(request:Request, background_tasks:BackgroundTasks, data:schemas.Report, auth:AuthJWT = Depends()) -> schemas.ResponseSuccess:
    auth.jwt_required()
    background_tasks.add_task(email.send_report, auth.get_jwt_subject(), data.book_id, data.report_type)
    return schemas.ResponseSuccess()

#=============================================#
#== CONTACT ==================================#
#=============================================#

@app.post("/contact")
@limiter.limit(conf.LIMIT_CONTACT)
async def contact(request:Request, background_tasks:BackgroundTasks, data:schemas.Contact,  auth:AuthJWT = Depends()) -> schemas.ResponseSuccess:
    try:
        uid = auth.get_jwt_subject()
    except:
        uid = None
    background_tasks.add_task(email.send_contact, uid, data.email, data.msg)
    return schemas.ResponseSuccess()

#=============================================#
#== DELETE-ACCOUNT ===========================#
#=============================================#

@app.post("/delete-account")
async def delete_account(request:Request, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or not user.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    stripe.Customer.delete(user.stripe_customer_id)
    user.email, user.hashed_password = utils.get_anon_values()  
    user.active = False  
    return schemas.ResponseSuccess()

#=============================================#
#== HEALTH-CHECK =============================#
#=============================================#

@app.get("/health")
async def health_check(request:Request) -> schemas.ResponseSuccess:
    return schemas.ResponseSuccess()

#=============================================#
#== ADMIN : FREE-CREDIT ======================#
#=============================================#

@app.get("/admin/credit")
async def admin_get_credit(request:Request, user_id:UUID, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    raise HTTPException(404)
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or str(user.id) not in conf.ADMINS:
        raise HTTPException(403, conf.MSG_FORBIDDEN)
    target = db.get(User, user_id)
    if not target or not target.active:
        raise HTTPException(404, conf.MSG_USER_DOES_NOT_EXIST)
    target.book_credit = target.book_credit + 1
    db.create(Notification(type=schemas.NotificationType.NEW_BOOK.value, user_id=target.id))
    return schemas.ResponseSuccess()

#=============================================#
#== ADMIN : BOOKS ============================#
#=============================================#

@app.get("/admin/books")
async def admin_get_books(request:Request, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> List[schemas.AdminBooks]:
    raise HTTPException(404)
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or str(user.id) not in conf.ADMINS:
        raise HTTPException(403, conf.MSG_FORBIDDEN)
    return db.get_all(Book)

#=============================================#
#== ADMIN : BOOK =============================#
#=============================================#

@app.get("/admin/book")
async def admin_get_book(request:Request, book_id:UUID, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.AdminBook:
    raise HTTPException(404)
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or str(user.id) not in conf.ADMINS:
        raise HTTPException(403, conf.MSG_FORBIDDEN)
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, conf.MSG_BOOK_NOT_FOUND)
    return book

@app.put("/admin/book")
async def admin_put_book(request:Request, data:schemas.AdminBook, background_tasks:BackgroundTasks, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    raise HTTPException(404)
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or str(user.id) not in conf.ADMINS:
        raise HTTPException(403, conf.MSG_FORBIDDEN)
    book = db.get(Book, data.id)
    if not book:
        raise HTTPException(404, conf.MSG_BOOK_NOT_FOUND)
    for key, value in data.dict().items():
        setattr(book, key, value) 
    background_tasks.add_task(email.send_notif_admin, conf.EMAIL_NOTIF_ADMIN_PUT_BOOK, f"{data.id} | {data.title}")
    return schemas.ResponseSuccess()

@app.post("/admin/book")
async def admin_post_book(request:Request, data:schemas.AdminBook, background_tasks:BackgroundTasks, auth:AuthJWT = Depends(), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    auth.jwt_required()
    user = db.get(User, auth.get_jwt_subject())
    if not user or str(user.id) not in conf.ADMINS:
        raise HTTPException(403, conf.MSG_FORBIDDEN)
    if db.search(Book, and_(Book.title == data.title, Book.author_name == data.author_name)):
        raise HTTPException(409, conf.MSG_BOOK_ALREADY_EXISTS)
    try:
       db.create(Book(**data.dict()))
    except:
        raise HTTPException(406, conf.MSG_NOT_ACCEPTABLE) 
    background_tasks.add_task(email.send_notif_admin, conf.EMAIL_NOTIF_ADMIN_POST_BOOK, f"{data.id} | {data.title}")
    return schemas.ResponseSuccess()

#=============================================#
#== STRIPE-WEBHOOK ===========================#
#=============================================#

@app.post("/stripe-webhook")
async def stripe_webhook(request:Request, background_tasks:BackgroundTasks, stripe_signature: str = Header(str), db:Session = Depends(get_db)) -> schemas.ResponseSuccess:
    try: 
        event = stripe.Webhook.construct_event(await request.body(), stripe_signature, crypto.decode_sec("stripe_wh"))
        utils.debug(f"Stripe webhook {event.type}")
    except: 
        raise HTTPException(400) 

    if event.type == "customer.subscription.updated" or event.type == "customer.subscription.deleted":
        sub = event.data.object
        user = db.get(User, sub.metadata.user_id)
        notif = None

        if user:
            if(sub.status == "active"):
                if not user.sub:
                    user.book_credit = user.book_credit + 1
                    user.last_book_credit_date = datetime.now()
                    if not user.step_sub_once and sub.metadata.ref != "nobody":
                        referrer = db.search(User, User.referral_code == sub.metadata.ref)
                        if referrer:      
                            referrer.book_credit = referrer.book_credit + conf.REF_BONUS_CREDIT
                            user.referrer = referrer.id
                            referrer.step_ref_someone = True
                            if not referrer.sub_discount and referrer.sub_id:
                                stripe.Subscription.modify(referrer.sub_id, coupon=conf.STRIPE_COUPON_ID)
                                if referrer.email_pref_ref_someone:
                                    background_tasks.add_task(email.send_referral, referrer.email, True)
                                notif = (schemas.NotificationType.REF_DISCOUNT_START.value, referrer.id)
                            else:
                                if referrer.email_pref_ref_someone:
                                    background_tasks.add_task(email.send_referral, referrer.email, False)
                                notif = (schemas.NotificationType.REF_SOMEONE.value, referrer.id)
                user.step_sub_once = True
                user.sub = True
                user.sub_id = sub.id
                user.sub_since = datetime.fromtimestamp(sub.start_date)
                user.sub_current_period_start = datetime.fromtimestamp(sub.current_period_start)
                user.sub_current_period_end  = datetime.fromtimestamp(sub.current_period_end)
                user.sub_cancel_at_period_end  = sub.cancel_at_period_end 
                user.sub_discount = True if sub.discount else False
            elif sub.id == user.sub_id:
                user.sub = False
                user.sub_id = None
                user.sub_since = None
                user.sub_current_period_start = None
                user.sub_current_period_end  = None
                user.sub_cancel_at_period_end  = None
                user.sub_discount = False
                if user.email_pref_sub_will_expire:
                    background_tasks.add_task(email.send_membership_expiration, user.email)
    if notif:
        db.create(Notification(type=notif[0], user_id=notif[1]))

    return schemas.ResponseSuccess()

#=============================================#
#== WORKER-NEW-BOOK ==========================#
#=============================================#

@app.on_event("startup")
@repeat_every(seconds=conf.WORKER_NEW_BOOK_INTERVAL)
def worker_new_book():
    try:
        db = Session()
        users = db.search_all(User, and_(User.last_book_credit_date + timedelta(days=conf.INTERVAL_NEW_BOOK) < datetime.now(), User.sub == True))
        for user in users:
            user.book_credit = user.book_credit + 1
            user.last_book_credit_date = datetime.now()
            db.create(Notification(type=schemas.NotificationType.NEW_BOOK.value, user_id=user.id))
            if user.email_pref_new_book:
                email.send_new_book(user.email)
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()
