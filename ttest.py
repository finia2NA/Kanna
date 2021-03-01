from pygoogletranslation import Translator

t = Translator()

print(t.translate("これはテストです", dest="en").text)