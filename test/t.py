class Goods():
    def __init__(self,pr):
        self.pr=pr
    #     访问属性
    @property
    def price(self):
        return int(self.pr)
    # 设置属性值
    @price.setter
    def price(self,value):
        if self.pr>100:
            return None
        self.pr=value
    #     删除属性
    @price.deleter
    def price(self):
        del self.pr

g=Goods(20)
print(g.price) #20
g.price=30
print(g.price) #30
g.price=140
print(g.price) #30
del g.price
print(g.price) # 'Goods' object has no attribute 'pr'
