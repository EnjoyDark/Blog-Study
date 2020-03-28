from .commom import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.enjoydark.cn', '62.234.127.130']  # 匹配 .enjoydark.cn的所有域名
