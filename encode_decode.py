str = 'you 你'
bs = b'\xc4\xe3'
print("utf-8 encode:",str.encode("utf-8"))
print("gbk encode:",str.encode("gbk"))
print("gb2312 encode:",str.encode("gb2312"))
a = bs.decode("gb2312")
print(bs.decode("gb2312"))