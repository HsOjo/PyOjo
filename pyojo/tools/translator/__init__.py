from .baidu import BaiduTranslate
from .google import GoogleTranslate
from .zhconv import ZHConv


def baidu_translate(appid=None, key=None):
    return BaiduTranslate(appid, key)


def google_translate():
    return GoogleTranslate()


def zhconv():
    return ZHConv()
