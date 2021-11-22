from flask import Flask
import hashlib

app=Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

@app.route('/health_check')
def health_check():
    return 'OK'

@app.route('/shorten')
def shorten():
    '''
    16**11 =  17592186044416
    62**8  = 218340105584896
    16**12 = 281474976710656
    get first 11 digits of dexdigest md5
    convert it to base 62  8 digits
    '''
    digest = hashlib.md5(b"kjasdflkalsdkflkjdj").hexdigest()
    _base16_to_base62(digest[:11])
    # check if this short url already exists in db
    #if exist:
        # if the content is the same, return short url to the user
        # else: different long urls but same short url, found collision
        # increment it and retry

    #else:
        #write to db

        # return as response to user

def _base16_to_base62(s):
    # truncate first 11 digits
    hex= s[:11]
    # convert base16 to base10
    dec = int(hex, 16)
    # convert decimal to base 62
    alphanum='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    digits=[]
    while dec >= 62:
        m=dec%62
        dec=dec//62
        digits.append(alphanum[m])
    digits.append(alphanum[dec])
    base62=''.join(digits[::-1])
    if len(base62)<8:
        base62 = '0'*(8-len(base62)) + base62
    return base62


if __name__=='__main__':
    r=_base16_to_base62('aaa45b')
    print(r)
    #shorten()
    #app.run( debug=True)
