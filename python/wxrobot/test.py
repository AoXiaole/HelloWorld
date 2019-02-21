class test:
    g_var = None
    def __init__(self,url):
        self.url = url
    def chrome_open(self):
        if test.g_var :
           return None
        test.g_var = "nihao"

    def log_int(self):
        self.dir = "/tmp/{0}".format(self.url)



tt=test("http:www.baidu.com")
tt.chrome_open()

p = test("http:www.qq.com")
p.log_int()
print("p.g_var",p.g_var)
print("p.url",p.url)
print("p.dir",p.dir)