from flask import Flask, request
from flask_restful import Api, Resource

import hashlib

app=Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

@app.route('/health_check')
def health_check():
    return 'OK get'

@app.route('/health_check_p', methods=['POST'])
def health_check_p():
    return 'OK post'

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

class Link(Resource):

    def __init__(self):
        print('initialize link')

    def get(self):
        print('doing get link')
        req_headers= request.headers
        header_list = req_headers.items()
        for header in header_list:
            print(header)
        etag='1234567' # dummy_etag
        print('returning response resource with etag header')
        return "Request headers:\n" + str(request.headers)


    def post(self):
        print('posting')
        return 'POST'

    '''
    A working Curl example
    curl -v -X PUT -H "If-Match:1234567" http://127.0.0.1:5000/link
    '''
    def put(self):
        print('put')
        req_headers= request.headers
        header_list = req_headers.items()
        if_match_etag = req_headers.get('If-Match')
        print('put request header If-Match is', if_match_etag)
        if if_match_etag == '1234567':
            return 'success', 200
        else:
            return 'failure', 412

api=Api(app)
api.add_resource(Link, '/link')

if __name__=='__main__':
    #r=_base16_to_base62('aaa45b')
    #print(r)
    #shorten()
    app.run(debug=True)
