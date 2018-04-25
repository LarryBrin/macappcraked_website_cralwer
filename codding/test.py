import unicodedata
import string

def shave_marks(txt):
    """Remove all diacritics marks"""
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt if not
                     unicodedata.combining(c))
    return shaved

order = '“Herr Voß: • 1⁄2 cup of ŒtkerTM caffè latte • bowl of açaí.”'

a = shave_marks(order)
print(a)

Greek = 'Ζέφυρος, Zéfiro'

b = shave_marks(Greek)

print(b)
