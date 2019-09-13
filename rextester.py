# Credit to @veetaw and @GingerPlusPlus for the Rextester functions

import requests
import json

with open('languages.json', 'r') as f:
    LANGUAGES = json.load(f)

with open('compiler-args.json', 'r') as f:
    COMPILER_ARGS = json.load(f)

class Rextester:
    URL = 'https://rextester.com/rundotnet/api'

    def __init__(self):
        self.session = requests.Session()  # keep alive

    def execute(self, language: str, code: str, stdin: str = ''):
        if language.lower() not in LANGUAGES.keys():
            raise RextesterException('unknown_lang')
        
        if "{}".format(LANGUAGES.get(language)) in COMPILER_ARGS.keys():
            compilerargs = COMPILER_ARGS.get("{}".format(LANGUAGES.get(language)))
        else:
            pass
        
        try:
            _data = {
            'LanguageChoiceWrapper': LANGUAGES.get(language),
            'Program': code,
            'Input': stdin,
            'CompilerArgs': compilerargs
            }
        except UnboundLocalError:
            _data = {
            'LanguageChoiceWrapper': LANGUAGES.get(language),
            'Program': code,
            'Input': stdin,
            'CompilerArgs': ''
            }

        r = self.session.post(self.URL, data=_data)

        if r.status_code != requests.codes.ok:
            raise RextesterException('status_code')

        return r.json()


class RextesterException(Exception):
    {}