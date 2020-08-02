from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# This takes two arguments, the app secret key and availability time in seconds
s = Serializer('secret_key', 30)
token = s.dumps({'user':1}).decode('utf-8')

# This is how a token in simply generated
