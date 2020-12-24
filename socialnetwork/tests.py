from django.test import TestCase
from pyhunter import PyHunter
from django.conf import settings
from avasocial.avasocial.extapps import ClearBit


def test_hunter():
    # hunter = PyHunter(settings.CONFIG['Hunter']['secret_key'])

    hunter = PyHunter('ecf080f3ebd26143a43499aa652ffc6d755df3f0')
    verify = hunter.email_verifier('test@lflflflf.com')
    print(verify)

def test_clearbit():
    cb = ClearBit('a3469b7a3035920870fa18d6b4ba31f0')

    rich_data = cb.PersonData('egor.wexler@icloud.com')



test_clearbit()