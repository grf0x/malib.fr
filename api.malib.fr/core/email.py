from uuid import UUID
from core import conf, crypto
from emails.template import JinjaTemplate
from typing import Dict, Any, Union
import emails

def send_welcome(email_to:str, token:UUID):
    subject = conf.EMAIL_NEW_ACCOUNT_SUBJECT
    link = f"{conf.FRONT_DOMAIN}{conf.EMAIL_CONFIRMATION_PAGE}?t={token}"
    return send_email(to=email_to, subject=subject, template_name="new_account.html", env={"link":link})

def send_referral(email_to:str, first:bool):
    subject = conf.EMAIL_REFERRAL_SUBJECT
    link = f"{conf.FRONT_DOMAIN}{conf.LIBRARY_PAGE}"
    unsub = f"{conf.FRONT_DOMAIN}{conf.ACCOUNT_PAGE}"
    msg = conf.EMAIL_REFERRAL_DISCOUNT if first else conf.EMAIL_REFERRAL
    return send_email(to=email_to, subject=subject, template_name="referral.html", env={"link":link, "unsubscribe":unsub, "msg":msg})

def send_membership_expiration(email_to:str):
    subject = conf.EMAIL_MEMBERSHIP_EXPIRATION_SUBJECT
    link = f"{conf.FRONT_DOMAIN}{conf.LIBRARY_PAGE}"
    unsub = f"{conf.FRONT_DOMAIN}{conf.ACCOUNT_PAGE}"
    return send_email(to=email_to, subject=subject, template_name="membership_expiration.html", env={"link":link, "unsubscribe":unsub})

def send_new_book(email_to:str):
    subject = conf.EMAIL_NEW_BOOK_SUBJECT
    link = f"{conf.FRONT_DOMAIN}{conf.LIBRARY_PAGE}"
    unsub = f"{conf.FRONT_DOMAIN}{conf.ACCOUNT_PAGE}"
    return send_email(to=email_to, subject=subject, template_name="new_book.html", env={"link":link, "unsubscribe":unsub})

def send_change_email(email_to:str, token:UUID):
    subject = conf.EMAIL_CHANGE_EMAIL_SUBJECT
    link = f"{conf.FRONT_DOMAIN}{conf.EMAIL_CONFIRMATION_PAGE}?t={token}"
    return send_email(to=email_to, subject=subject, template_name="change_email.html", env={"link":link})

def send_password_recovery(email_to:str, token:UUID):
    subject = conf.EMAIL_PASSWORD_RECOVERY_SUBJECT
    link = f"{conf.FRONT_DOMAIN}{conf.PASSWORD_RECOVERY_PAGE}?u=r&t={token}"
    return send_email(to=email_to, subject=subject, template_name="password_recovery.html", env={"link":link})

def send_contact(user_id:Union[UUID, None], email_from:str, msg:str=""):
    subject = conf.EMAIL_CONTACT + email_from
    return send_email(to=conf.EMAIL_FROM[1], subject=subject, template_name="contact.html", env={"project":conf.PROJECT_NAME, "user_id":user_id, "from":email_from, "msg":msg})

def send_report(user_id:UUID, book_id:UUID, report_type:str):
    subject = conf.EMAIL_REPORT + user_id
    return send_email(to=conf.EMAIL_ADMIN, subject=subject, template_name="report.html", env={"project":conf.PROJECT_NAME, "book_id":book_id, "report_type":report_type})

def send_notif_admin(notif_type:str, details:str):
    subject = conf.EMAIL_ADMIN_ALERT + notif_type
    return send_email(to=conf.EMAIL_ADMIN, subject=subject, template_name="notif_admin.html", env={"project":conf.PROJECT_NAME, "notif_type":notif_type, "details":details})

def send_email(to:str, subject:str, template_name:str = "", env:Dict[str, Any] = {}):
    try:
        with open(conf.WORKING_DIR + "/email-templates/" + template_name) as f:
            html_template = f.read()
        message = emails.Message(subject=JinjaTemplate(subject), html=JinjaTemplate(html_template), mail_from=(conf.EMAIL_FROM))
        smtp_options = {"host":conf.SMTP_HOST, "port":conf.SMTP_PORT, "tls":conf.SMTP_TLS, "user":conf.SMTP_USER, "password":crypto.decode_sec("smtp")}
        message.send(to=to, render=env, smtp=smtp_options)
    except: pass
   