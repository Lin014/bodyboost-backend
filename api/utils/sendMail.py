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

def sendRegisterMail(email, user):
    code = getNumberRandomCode()
    emailVerifyCode = EmailVerifyCode.objects.create(
        code = code,
        email = email,
        send_type = 'register',
        user_id = user
    )
    
    sendTitle = "歡迎註冊 Body Boost APP 會員帳號！"
    sendContent = "以下是您的驗證碼：\n\n " + emailVerifyCode.code
    sender = formataddr(('Body Boost', EMAIL_HOST_USER))
    send_mail(sendTitle, sendContent, sender, [emailVerifyCode.email], fail_silently=False)

def sendForgetMail(email, user):
    code = getAlphanumericRandomCode()
    emailVerifyCode = EmailVerifyCode.objects.create(
        code = code,
        email = email,
        send_type = 'forget',
        user_id = user
    )

    sendTitle = "Body Boost 重設密碼驗證"
    sendContent = "以下是您的驗證碼：\n\n " + emailVerifyCode.code
    sender = formataddr(('Body Boost', EMAIL_HOST_USER))
    send_mail(sendTitle, sendContent, sender, [emailVerifyCode.email], fail_silently=False)

