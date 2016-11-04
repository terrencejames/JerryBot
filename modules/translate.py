from microsofttranslator import Translator
from auth import MSFT_CLIENTID,MSFT_CLIENTSECRET
from language_table import languages

translator = Translator(MSFT_CLIENTID, MSFT_CLIENTSECRET)

def translate_text(args=[]):
    global translator

    if args[0] == "help":
        return "!translate $from$>$to$ words"
    langs = args[0].split("->")
    words = " ".join(args[1:])
    if len(langs) == 1:
        try:
            lang = languages[langs[0].lower()]
            return translator.translate(words, lang)
        except:
            return "language not found"
    else:
        try:
            from_lang = languages[langs[0]]
            new_text = ""
            for i in range(len(langs)-1):
                to_lang = languages[langs[i+1]]
                print("from %s to %s" %(from_lang, to_lang))
                new_text = translator.translate(words, to_lang, from_lang)
                from_lang = to_lang
            return new_text
        except Exception, e:
            print(str(e))
            return ""
