from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from enum import Enum
from typing import Union, Literal
from core import conf, crypto

class Credentials(BaseModel):
    email:str = Field(regex=conf.REGEX_EMAIL)
    password:str = Field(regex=conf.REGEX_PASSWORD)

class ActionTokenType(Enum):
    PASSWORD_RECOVERY = 0
    EMAIL_CONFIRMATION = 1

class NotificationType(str, Enum):
    NEW_BOOK = "NB"
    REF_SOMEONE = "R"
    REF_DISCOUNT_START = "RD"

class BookRating(str, Enum):
    DISLIKE = "D"
    NEUTRAL = "N"
    LIKE = "L"

class LibrarySorting(str, Enum):
    ACTIVITY = "ACTIVITY"
    ADDED = "ADDED"
    AUTHOR = "AUTHOR"
    TITLE = "TITLE"

class ReaderTheme(str, Enum):
    LIGHT_GREY = "LGREY"
    DARK_GREY = "DGREY"
    WHITE = "WHITE"

class ReaderFont(str, Enum):
    FUTURA = "FUTURA"
    MONSERRAT = "MONTSERRAT"
    BASKERVILLE = "BASKERVILLE"
    GARAMOND = "GARAMOND"

class Settings(BaseModel):
    library_sorting:LibrarySorting
    reader_theme:ReaderTheme
    reader_zoom:int = Field(ge=80, le=300)
    reader_font:ReaderFont
    class Config:  
        use_enum_values = True

class RateBook(BaseModel):
    book_id:UUID
    book_rating:BookRating
    class Config:  
        use_enum_values = True

class Report(BaseModel):
    book_id:UUID
    report_type:str = Field(max_length=conf.MAX_REPORT_TYPE)

class SaveProgress(BaseModel):
    book_id:UUID
    chapter:str = Field(max_length=conf.MAX_CHAPTER)
    progress_chapter:float = Field(ge=0, le=100)
    progress_book:float = Field(ge=0, le=100)

class Progress(BaseModel):
    chapter:Union[str, None]
    progress_chapter:Union[float, None]
    class Config:
        orm_mode = True

class PassBook(BaseModel):
    book_id:UUID
    book_rating:Union[Literal["D", "L"], None]

class Recommendation(BaseModel):
    id:UUID
    author_name:str = Field(max_length=conf.MAX_AUTHOR)
    title:str = Field(max_length=conf.MAX_TITLE)
    summary:str = Field(max_length=conf.MAX_SUMMARY)
    keyword_biographie:float = Field(ge=0, le=1)
    keyword_drame:float = Field(ge=0, le=1)
    keyword_histoire_vraie:float = Field(ge=0, le=1)
    keyword_psychologie:float = Field(ge=0, le=1)
    keyword_historique:float = Field(ge=0, le=1)
    keyword_mystere:float = Field(ge=0, le=1)
    keyword_suspense:float = Field(ge=0, le=1)
    keyword_philosophie:float = Field(ge=0, le=1)
    keyword_humour:float = Field(ge=0, le=1)
    keyword_science_fiction:float = Field(ge=0, le=1)
    keyword_enquete_policiere:float = Field(ge=0, le=1)
    keyword_realiste:float = Field(ge=0, le=1)
    keyword_mythes_et_legendes:float = Field(ge=0, le=1)
    keyword_aventure:float = Field(ge=0, le=1)
    keyword_espionnage:float = Field(ge=0, le=1)
    keyword_histoire_d_amour:float = Field(ge=0, le=1)
    keyword_guerre:float = Field(ge=0, le=1)
    keyword_horreur:float = Field(ge=0, le=1)
    keyword_surnaturel:float = Field(ge=0, le=1)
    class Config:
        orm_mode = True

class ActionToken(BaseModel):
    id:UUID
    action:str
    email:str = Field(regex=conf.REGEX_EMAIL)
    expiration_date:date

class AccessToken(BaseModel):
    access_token:str = Field(regex=conf.REGEX_JWT)

class JWTSettings(BaseModel):
    authjwt_secret_key:str = crypto.decode_sec("jwt")

class AccessToken(BaseModel):
    access_token:str = Field(regex=conf.REGEX_JWT)

class Subscribe(BaseModel):
    client_secret:str
    invoice:str
    is_first_sub:bool

class Contact(BaseModel):
    email:str = Field(regex=conf.REGEX_EMAIL)
    msg:str = Field(regex=conf.REGEX_MSG_CONTACT)

class Steps(BaseModel):
    is_sub:bool
    set_pref:bool
    pick_first_book:bool

class EmailPreferences(BaseModel):
    new_book:bool
    ref_someone:bool
    sub_will_expire:bool
    promo:bool

class Notification(BaseModel):
    type:str
    date:date
    class Config:
        orm_mode = True

class BookLibrary(BaseModel):
    id:UUID
    title:str
    author_name:str
    progress:float
    class Config:
        orm_mode = True

class Book(BaseModel):
    id:UUID
    title:str
    author_name:str
    summary:str
    img:Union[str, None]
    next_book:Union[UUID, None]
    progress:float
    rating:Union[str, None]
    complexity:float
    emotion_joie:float
    emotion_colere:float
    emotion_tristesse:float
    emotion_peur:float
    emotion_degout:float
    emotion_surprise:float
    keyword_biographie:float
    keyword_drame:float
    keyword_histoire_vraie:float
    keyword_psychologie:float
    keyword_historique:float
    keyword_mystere:float
    keyword_suspense:float
    keyword_philosophie:float
    keyword_humour:float
    keyword_science_fiction:float
    keyword_enquete_policiere:float
    keyword_realiste:float
    keyword_mythes_et_legendes:float
    keyword_aventure:float
    keyword_espionnage:float
    keyword_histoire_d_amour:float
    keyword_guerre:float
    keyword_horreur:float
    keyword_surnaturel:float
    class Config:
        orm_mode = True

class AuthInfo(BaseModel):
    steps:Steps
    email_preferences:EmailPreferences
    settings:Settings
    unread_notifications:int
    book_credit:int
    sub_since:Union[date, None]
    sub_current_period_end:Union[date, None]
    sub_cancel_at_period_end:Union[bool, None]
    next_credit_date:Union[date, None]
    sub_discount:Union[bool, None]
    referral_code:str = Field(regex=conf.REGEX_REFERRAL)
    email:str = Field(regex=conf.REGEX_EMAIL)

class ResponseSuccess(BaseModel):
    success:bool = True

class CancelSubscription(BaseModel):
    state:bool

class ReferralCode(BaseModel):
    code:str = Field(regex=conf.REGEX_REFERRAL)

class PromoCode(BaseModel):
    code:str = Field(regex=conf.REGEX_PROMO)

class PromoValidation(BaseModel):
    code:str = Field(regex=conf.REGEX_PROMO)
    description:str

class ChangePassword(BaseModel):
    old_password:str = Field(regex=conf.REGEX_PASSWORD)
    new_password:str = Field(regex=conf.REGEX_PASSWORD)

class PasswordRecovery(BaseModel):
    token:UUID
    new_password:str = Field(regex=conf.REGEX_PASSWORD)

class ConfirmEmail(BaseModel):
    token:UUID

class ChangeEmailAddress(BaseModel):
    new_email:str = Field(regex=conf.REGEX_EMAIL)

class Preferences(BaseModel):
    pref_reader_type:float = Field(ge=0, le=1)
    pref_time_period:float = Field(ge=0, le=1)
    pref_complexity:float = Field(ge=0, le=1)
    pref_keyword_biographie:bool
    pref_keyword_drame:bool
    pref_keyword_histoire_vraie:bool
    pref_keyword_psychologie:bool
    pref_keyword_historique:bool
    pref_keyword_mystere:bool
    pref_keyword_suspense:bool
    pref_keyword_philosophie:bool
    pref_keyword_humour:bool
    pref_keyword_science_fiction:bool
    pref_keyword_enquete_policiere:bool
    pref_keyword_realiste:bool
    pref_keyword_mythes_et_legendes:bool
    pref_keyword_aventure:bool
    pref_keyword_espionnage:bool
    pref_keyword_histoire_d_amour:bool
    pref_keyword_guerre:bool
    pref_keyword_horreur:bool
    pref_keyword_surnaturel:bool

class AdminBooks(BaseModel):
    id:UUID
    title:str
    author_name:str
    class Config:
        orm_mode = True

class AdminBook(BaseModel):
    id:UUID
    title:str
    author_name:str
    summary:str
    img:Union[str, None]
    is_first:bool
    next_book:Union[UUID, None]
    public_score:float
    popularity:int
    complexity:float
    emotion_joie:float
    emotion_colere:float
    emotion_tristesse:float
    emotion_peur:float
    emotion_degout:float
    emotion_surprise:float
    keyword_biographie:float
    keyword_drame:float
    keyword_histoire_vraie:float
    keyword_psychologie:float
    keyword_historique:float
    keyword_mystere:float
    keyword_suspense:float
    keyword_philosophie:float
    keyword_humour:float
    keyword_science_fiction:float
    keyword_enquete_policiere:float
    keyword_realiste:float
    keyword_mythes_et_legendes:float
    keyword_aventure:float
    keyword_espionnage:float
    keyword_histoire_d_amour:float
    keyword_guerre:float
    keyword_horreur:float
    keyword_surnaturel:float
    class Config:
        orm_mode = True