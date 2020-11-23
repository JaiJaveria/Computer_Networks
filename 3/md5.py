import hashlib
print(hashlib.md5(open('debug2.txt','r', ).read().encode('utf-8')).hexdigest()=='70a4b9f4707d258f559f91615297a3ec')