from Crypto.Cipher import AES
import hashlib
import json
from urllib.parse import urlencode
from Crypto.Util.Padding import pad

HashKey = b'dx4LYO9GZLngKQIfWnyAUgANi4R3pX85'
HashIV = b'CzqGUlCRvmaYW3NP'
dict = {'name' : 'john', 'age' : 80, 'from' : 'USA'}
dict2 = {'crypto' : '', 'tret' : 'sss'}

dicturlcode = urlencode(dict).encode(encoding='utf-8')
print('preAESCrypto ->', dicturlcode)
print(type(dicturlcode))
plaintext = pad(dicturlcode, 16)
print(plaintext)
cipher = AES.new(HashKey, AES.MODE_CBC, HashIV)
cryptoText = cipher.encrypt(plaintext)
shacryptoText = hashlib.sha256(cryptoText).hexdigest()
print(shacryptoText)
dict2['crypto'] = cryptoText.hex()
print(dict2)