from core import utils, conf, schemas, crypto
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, ForeignKey, DateTime, Integer, Float, ARRAY
from sqlalchemy.sql import func
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, load_only
from typing import List, Any, Union
import uuid

#============================================#
#== MODEL ===================================#
#============================================#

@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return utils.camel_to_snake(cls.__name__)

class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    email = Column(String(conf.MAX_EMAIL), unique=True, index=True, nullable=False)
    hashed_password = Column(String(conf.MAX_H_PASSWORD), nullable=False)
    referral_code = Column(String(conf.MAX_REFERRAL_CODE), unique=True, nullable=False, default=utils.generate_referral_code)
    referrer = Column(ForeignKey("user.id"), nullable=True)
    registration_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    last_activity_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    stripe_customer_id = Column(String(conf.MAX_CUSTOMER_ID), unique=True, nullable=False)
    sub = Column(Boolean, nullable=False, default=False)
    sub_id = Column(String(conf.MAX_SUB_ID), nullable=True)
    sub_since = Column(DateTime(timezone=True), nullable=True)
    sub_current_period_start = Column(DateTime(timezone=True), nullable=True)
    sub_current_period_end = Column(DateTime(timezone=True), nullable=True)
    sub_cancel_at_period_end = Column(Boolean, nullable=True)
    sub_discount = Column(Boolean, nullable=False, default=False)
    book_credit = Column(Integer, nullable=False, default=0)
    last_book_credit_date = Column(DateTime(timezone=True), nullable=True)
    book_credit_spent = Column(Integer, nullable=False, default=0)
    setting_reader_theme = Column(String(conf.MAX_SETTINGS), nullable=False, default=schemas.ReaderTheme.DARK_GREY.value)
    setting_reader_zoom = Column(Integer, nullable=False, default=130)
    setting_reader_font = Column(String(conf.MAX_SETTINGS), nullable=False, default=schemas.ReaderFont.FUTURA.value)
    setting_library_sorting = Column(String(conf.MAX_SETTINGS), nullable=False, default=schemas.LibrarySorting.ACTIVITY.value)
    email_pref_new_book = Column(Boolean, nullable=False, default=False)
    email_pref_ref_someone = Column(Boolean, nullable=False, default=True)
    email_pref_sub_will_expire = Column(Boolean, nullable=False, default=True)
    email_pref_promo = Column(Boolean, nullable=False, default=True)
    pref_reader_type = Column(Float, nullable=True)
    pref_time_period = Column(Float, nullable=True)
    pref_complexity = Column(Float, nullable=True)
    pref_keyword_biographie = Column(Float, nullable=True)
    pref_keyword_drame = Column(Float, nullable=True)
    pref_keyword_histoire_vraie = Column(Float, nullable=True)
    pref_keyword_psychologie = Column(Float, nullable=True)
    pref_keyword_historique = Column(Float, nullable=True)
    pref_keyword_mystere = Column(Float, nullable=True)
    pref_keyword_suspense = Column(Float, nullable=True)
    pref_keyword_philosophie = Column(Float, nullable=True)
    pref_keyword_humour = Column(Float, nullable=True)
    pref_keyword_science_fiction = Column(Float, nullable=True)
    pref_keyword_enquete_policiere = Column(Float, nullable=True)
    pref_keyword_realiste = Column(Float, nullable=True)
    pref_keyword_mythes_et_legendes = Column(Float, nullable=True)
    pref_keyword_aventure = Column(Float, nullable=True)
    pref_keyword_espionnage = Column(Float, nullable=True)
    pref_keyword_histoire_d_amour = Column(Float, nullable=True)
    pref_keyword_guerre = Column(Float, nullable=True)
    pref_keyword_horreur = Column(Float, nullable=True)
    pref_keyword_surnaturel = Column(Float, nullable=True)
    step_set_pref = Column(Boolean, nullable=False, default=False)
    step_pick_first_book = Column(Boolean, nullable=False, default=False)
    step_confirm_email = Column(Boolean, nullable=False, default=False)
    step_sub_once = Column(Boolean, nullable=False, default=False)
    step_ref_someone = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)
    recommendation = Column(ARRAY(Float), nullable=True)

class Book(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String(conf.MAX_TITLE), nullable=False)
    author_name = Column(String(conf.MAX_AUTHOR), nullable=False)
    summary = Column(String(conf.MAX_SUMMARY), nullable=False)
    img = Column(String(conf.MAX_URL), nullable=True)
    is_first = Column(Boolean, nullable=False, default=True)
    next_book = Column(ForeignKey("book.id"), nullable=True)
    public_score = Column(Float, nullable=False, default=5)
    popularity = Column(Integer, nullable=False, default=1)
    complexity = Column(Float, nullable=False, default=0.5)
    emotion_joie = Column(Float, nullable=False, default=0.5)
    emotion_colere = Column(Float, nullable=False, default=0.5)
    emotion_tristesse = Column(Float, nullable=False, default=0.5)
    emotion_peur = Column(Float, nullable=False, default=0.5)
    emotion_degout = Column(Float, nullable=False, default=0.5)
    emotion_surprise = Column(Float, nullable=False, default=0.5)
    keyword_biographie = Column(Float, nullable=False, default=0.5)
    keyword_drame = Column(Float, nullable=False, default=0.5)
    keyword_histoire_vraie = Column(Float, nullable=False, default=0.5)
    keyword_psychologie = Column(Float, nullable=False, default=0.5)
    keyword_historique = Column(Float, nullable=False, default=0.5)
    keyword_mystere = Column(Float, nullable=False, default=0.5)
    keyword_suspense = Column(Float, nullable=False, default=0.5)
    keyword_philosophie = Column(Float, nullable=False, default=0.5)
    keyword_humour = Column(Float, nullable=False, default=0.5)
    keyword_science_fiction = Column(Float, nullable=False, default=0.5)
    keyword_enquete_policiere = Column(Float, nullable=False, default=0.5)
    keyword_realiste = Column(Float, nullable=False, default=0.5)
    keyword_mythes_et_legendes = Column(Float, nullable=False, default=0.5)
    keyword_aventure = Column(Float, nullable=False, default=0.5)
    keyword_espionnage = Column(Float, nullable=False, default=0.5)
    keyword_histoire_d_amour = Column(Float, nullable=False, default=0.5)
    keyword_guerre = Column(Float, nullable=False, default=0.5)
    keyword_horreur = Column(Float, nullable=False, default=0.5)
    keyword_surnaturel = Column(Float, nullable=False, default=0.5)

class BookUser(Base):
    user_id = Column(ForeignKey("user.id"), primary_key=True, nullable=False)
    book_id = Column(ForeignKey("book.id"), primary_key=True, nullable=False)
    progress = Column(Float, nullable=True)
    progress_chapter = Column(Float, nullable=True)
    chapter = Column(String(conf.MAX_CHAPTER), nullable=True)
    rating = Column(String(conf.MAX_RATING), nullable=True)
    is_in_library = Column(Boolean, nullable=False, default=False)
    added_in_library_date = Column(DateTime(timezone=True), nullable=True)
    last_activity_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
class Notification(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    type = Column(String(conf.MAX_NOTIF_TYPE), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    user_id = Column(ForeignKey("user.id"), nullable=False)
    opened = Column(Boolean, nullable=False, default=False)

class ActionToken(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    type = Column(Integer, nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    expiration_date = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)

#============================================#
#== ENGINE ==================================#
#============================================#

engine = None

def get_engine():
    try:
        engine.connect()
    except:
        engine = create_engine(f"postgresql://postgres:{crypto.decode_sec('db')}@127.0.0.1:5432/malib?sslmode=require") 
    finally:
        return engine

#============================================#
#== SESSION =================================#
#============================================#

class Session:
    session = None
 
    def __init__(self):
        SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
        self.session = SessionMaker()

    def close(self):
        self.session.close()

    def commit(self):
        self.session.commit()
        
    def rollback(self):
        self.session.rollback()

    # GENERIC

    def create(self, obj:Base) -> Base:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj:Base):
        self.session.delete(obj)

    def get(self, req_obj:Base, id:Union[UUID,str]) -> Base:
        return self.session.query(req_obj).filter(req_obj.id == id).first()

    def get_all(self, req_obj:Base, by:Any=None, skip:int = None, limit:int = None) -> List[Base]:
        return self.session.query(req_obj).order_by(by).offset(skip).limit(limit).all()

    def search(self, req_obj:Base, search:Any) -> Base:
        return self.session.query(req_obj).filter(search).first()
    
    def search_all(self, req_obj:Base, search:Any,  by:Any = None, skip:int = None, limit:int = None) -> List[Base]:
        return self.session.query(req_obj).filter(search).order_by(by).offset(skip).limit(limit).all()

    def count(self, req_obj:Base, search:Any) -> List[Base]:
        return self.session.query(req_obj).filter(search).count()

    # CUSTOM

    def get_library(self, uid, sort) -> List[Base]:
        if sort == schemas.LibrarySorting.ACTIVITY:
            return self.session.query(Book.id, Book.title, Book.author_name, BookUser.progress).join(Book, Book.id == BookUser.book_id).filter(and_(BookUser.user_id == uid, BookUser.is_in_library == True)).order_by(BookUser.last_activity_date.desc()).all()
        elif sort == schemas.LibrarySorting.AUTHOR:
            return self.session.query(Book.id, Book.title, Book.author_name, BookUser.progress).join(Book, Book.id == BookUser.book_id).filter(and_(BookUser.user_id == uid, BookUser.is_in_library == True)).order_by(Book.author_name).all()
        elif sort == schemas.LibrarySorting.TITLE:
            return self.session.query(Book.id, Book.title, Book.author_name, BookUser.progress).join(Book, Book.id == BookUser.book_id).filter(and_(BookUser.user_id == uid, BookUser.is_in_library == True)).order_by(Book.title).all()
        else:
            return self.session.query(Book.id, Book.title, Book.author_name, BookUser.progress).join(Book, Book.id == BookUser.book_id).filter(and_(BookUser.user_id == uid, BookUser.is_in_library == True)).order_by(BookUser.added_in_library_date.desc()).all()

    def get_book(self, uid, bid) -> Base:
        return self.session.query(Book.id, Book.title, Book.author_name, Book.summary, Book.img, Book.next_book, BookUser.progress, BookUser.rating, Book.complexity, Book.emotion_joie,
        Book.emotion_colere, Book.emotion_tristesse, Book.emotion_peur, Book.emotion_degout, Book.emotion_surprise, Book.keyword_biographie, Book.keyword_drame, Book.keyword_histoire_vraie, 
        Book.keyword_psychologie, Book.keyword_historique, Book.keyword_mystere, Book.keyword_suspense, Book.keyword_philosophie, Book.keyword_humour, Book.keyword_science_fiction, 
        Book.keyword_enquete_policiere, Book.keyword_realiste, Book.keyword_mythes_et_legendes, Book.keyword_aventure, Book.keyword_espionnage, Book.keyword_histoire_d_amour, Book.keyword_guerre,
        Book.keyword_horreur, Book.keyword_surnaturel).join(Book, Book.id == BookUser.book_id).filter(and_(BookUser.book_id == bid, BookUser.user_id == uid)).first()

    def get_recommendation(self, uid) -> List[Base]:
        # ****REDACTED****
        return # ****REDACTED****

    def delete_passed(self, uid) -> List[Base]:
        self.session.query(BookUser).filter(and_(BookUser.user_id == uid, BookUser.is_in_library == False)).delete()
    
    def get_notifications(self, uid, limit):
        return self.session.query(Notification.type, Notification.date, Notification.opened).filter(Notification.user_id == uid).order_by(Notification.date.desc()).limit(limit).all()
    
    def get_progress(self, uid, bid):
        return self.session.query(BookUser.progress_chapter, BookUser.chapter).filter(and_(BookUser.user_id == uid, BookUser.book_id == bid)).first()

def create_db():
    Base.metadata.create_all(bind=get_engine())

def get_db():
    try:
        db = Session()
        yield db
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()
        

