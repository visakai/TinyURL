from flask import Flask, request, Response
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

    '''
    A working Curl example
    curl -v -X GET -H "If-None-Match:1234567" http://127.0.0.1:5000/link
    '''
    def get(self):
        print('doing get link')
        req_headers= request.headers
        client_etag = req_headers.get('If-None-Match')

        '''
        the client get request could use a If-None-Match header with etag value
        means please give me the new resource if this etag is stale
        the server will compare the etag with current etag, if they match, just respond with 304 Not Modified
        if not match, actually return the resource
        '''
        db_etag='1234567' # dummy etag to represent current version in database
        if client_etag==db_etag:
            return 'not modified', 304
        else:
            print('prepare the data and return it')
            # here we can insert the new etag to response header
            response = Response(status=200) # status=200 can be ommited here
            response.headers["ETag"] = db_etag
            return response

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
        if_match_etag = request.headers.get('If-Match')
        print('put request header If-Match = ', if_match_etag)
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
