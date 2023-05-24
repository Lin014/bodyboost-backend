from django.core.mail import send_mail
from email.utils import formataddr

from random import choice, randint

from ..models import EmailVerifyCode
from bodyboost.settings import EMAIL_HOST_USER

def getAlphanumericRandomCode():
    codeSource = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''

    for i in range(6):
        code += choice(codeSource)

    return code

def getNumberRandomCode():
    code = ''

    for i in range(6):
        code += str(randint(0, 9))

    return code

def sendVerificationMail(email, userID):
    code = getNumberRandomCode()
    emailVerifyCode = EmailVerifyCode.objects.create(
        code = code,
        email = email,
        send_type = 'register',
        user_id = userID
    )
    
    sendTitle = "歡迎註冊 BodyBoost APP 會員帳號！"
    sendContent = "以下是您的驗證碼：\n\n " + emailVerifyCode.code
    sender = formataddr(('Body Boost', EMAIL_HOST_USER))
    send_mail(sendTitle, sendContent, sender, [emailVerifyCode.email], fail_silently=False)

