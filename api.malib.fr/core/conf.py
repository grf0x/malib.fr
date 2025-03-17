PROJECT_NAME = "Malib"
REFERRAL_CODE_LENGTH = 8
REFERRAL_CHARSET = "345679ACEFGHJKLMNPQRSTWXY"
REF_BONUS_CREDIT = 2
INTERVAL_NEW_BOOK = 7 #days
DEFAULT_NB_NOTIF = 15
FRONT_DOMAIN = "https://malib.fr"
WORKING_DIR = "/home/malib/api.malib.fr"
PASSWORD_RECOVERY_PAGE = "/reinitialiser-son-mot-de-passe"
EMAIL_CONFIRMATION_PAGE = "/confirmation-e-mail"
LIBRARY_PAGE = "/bibliotheque"
ACCOUNT_PAGE = "/compte"
SEC_PATH = "****REDACTED****"
ADMINS = ["****REDACTED****"]

#STRIPE
STRIPE_PRODUCT_ID = "****REDACTED****"
STRIPE_PAYMENT_CONF = "****REDACTED****"
STRIPE_COUPON_ID = "****REDACTED****"

#WORKERS
WORKER_NEW_BOOK_INTERVAL = 60

#TOKEN EXPIRATION
EXPIRATION_ACCESS_TOKEN = 60*60*24*3 #3days
EXPIRATION_ACCESS_TOKEN_ADMIN = 60*60 #1hour
EXPIRATION_PASSWORD_RECOVERY_TOKEN = 60*60*24 #24hours
EXPIRATION_EMAIL_CONFIRMATION_TOKEN = 60*60*24*365*100 #100years

#LIMITS
LIMIT_CONTACT = "20/10minute"
LIMIT_REPORT = "20/10minute"
LIMIT_LOGIN = "20/30minute"
LIMIT_SIGNIN = "10/30minute"
LIMIT_PASSWORD_RECOVERY = "10/30minute"
LIMIT_CHANGE_EMAIL = "1/60minute"
LIMIT_CHANGE_PASSWORD = "4/60minute"
LIMIT_PROMO_CODE_VALIDATION = "100/24hour"

# ERROR MESSAGES
MSG_BAD_PASSWORD = "Bad password"
MSG_BAD_TOKEN = "Bad token"
MSG_NO_EMAIL = "No email address provided"
MSG_BAD_CREDENTIALS = "Bad email or password"
MSG_PASSWORDS_ARE_IDENTICAL = "Passwords are identical"
MSG_EMAIL_ALREADY_EXISTS = "This email address is already in use"
MSG_BOOK_ALREADY_EXISTS = "This book already exists"
MSG_ALREADY_MEMBER = "A subscription is already active"
MSG_NOT_MEMBER = "User doesn't have any active subscription"
MSG_VALIDATION = "Some validation error happened"
MSG_LIMIT = "Request limit reached"
MSG_UNEXPECTED = "Something unexpected happened"
MSG_STRIPE = "Stripe error"
MSG_USER_DOES_NOT_EXIST = "User not found"
MSG_SMTP = "Smtp error"
MSG_BOOK_NOT_FOUND = "Book not found"
MSG_BOOK_EXISTS = "Book already in library"
MSG_NOT_ENOUGH_CREDIT = "Not enough credit"
MSG_NOT_ACCEPTABLE = "Not acceptable"
MSG_FORBIDDEN = "Forbidden"
MSG_PROMO_CODE_NOT_FOUND = "Promo code not found"
MSG_ALREADY_REF_PROMO = "Discount already exists"
MSG_NOT_ELIGIBLE = "Not eligible"

# DATA MAX LENGTH
MAX_REFERRAL_CODE = 10
MAX_H_PASSWORD = 64
MAX_EMAIL = 255
MAX_CUSTOMER_ID = 127
MAX_SUB_ID = 127
MAX_SUB_STATUS = 15
MAX_SUMMARY = 800
MAX_NOTIF_TYPE = 2
MAX_RATING = 1
MAX_AUTHOR = 63
MAX_TITLE = 127
MAX_CHAPTER = 255
MAX_URL = 511
MAX_CONTACT_MSG = 3000
MAX_SETTINGS = 12
MAX_REPORT_TYPE = 20

# REGEX
REGEX_EMAIL = "^(?=.{1,254}$)(?:[a-z0-9!#$%&'*+-/=?^_`{|}~]+(?:\.[a-z0-9!#$%&'*+-/=?^_`{|}~]+)*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)$"
REGEX_PASSWORD = "^.{8,128}$"
REGEX_REFERRAL = "^[" + REFERRAL_CHARSET + "]{" + str(REFERRAL_CODE_LENGTH) + "}$"
REGEX_PROMO = "^[A-Z0-9]{3,25}$"
REGEX_INVOICE = "^in_[A-Za-z0-9]{16,32}$"
REGEX_JWT = "^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$"
REGEX_MSG_CONTACT = "^.{1,1000}$"

# EMAIL
SMTP_USER = "****REDACTED****"
SMTP_HOST = "****REDACTED****"
SMTP_PORT = 587
SMTP_TLS = True
EMAIL_FROM = ("Malib", "****REDACTED****")
EMAIL_ADMIN = "****REDACTED****"
EMAIL_ADMIN_DB_FAILED_SUBJECT = "La base de données de malib.fr ne répond pas."
EMAIL_NEW_ACCOUNT_SUBJECT = "Bienvenue sur Malib ! 🥳"
EMAIL_CHANGE_EMAIL_SUBJECT = "Confirmez votre nouvelle adresse e-mail."
EMAIL_PASSWORD_RECOVERY_SUBJECT = "Réinitialisation de votre mot de passe. 🔑"
EMAIL_CONTACT = "Message de : "
EMAIL_REPORT = "Signalement de : "
EMAIL_REFERRAL_SUBJECT = "Vous avez parrainé un utilisateur !"
EMAIL_REFERRAL_DISCOUNT = "Félicitations, vous venez de parrainer un nouvel utilisateur ! Votre abonnement passe de 6,99€ à 5,99€ par mois et vous recevez 2 nouveaux livres gratuits."
EMAIL_REFERRAL = "Félicitations, vous venez de parrainer un nouvel utilisateur ! Vous recevez 2 nouveaux livres gratuits."
EMAIL_MEMBERSHIP_EXPIRATION_SUBJECT = "Votre abonnement vient d'expirer."
EMAIL_NEW_BOOK_SUBJECT = "Vous avez reçu un nouveau livre. 🥳"
EMAIL_ADMIN_SUBJECT = "Alerte : Modification importante"
EMAIL_NOTIF_ADMIN_POST_BOOK = "Un nouveau livre a été ajouté."
EMAIL_NOTIF_ADMIN_PUT_BOOK = "Un livre a été modifié."
