#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")

class train():
    def run(self,data,mu=1,maxloopcnt=10000):
        datanum=len(data)
        if datanum==0:return None
        dimi=len(data[0][0])
        w=[0 for i in range(dimi)]
        b=0
        for i in range(maxloopcnt):
            loopend=True
            for j in range(datanum):
                x=data[j][0]
                y=data[j][1]
                wx=sum([x[k]*w[k] for k in range(dimi)])
                tmp=y*(wx + b)
                #print 'before',j,x,y,w,b,tmp
                while tmp <=0:
                    for k in range(dimi):
                        w[k]=w[k] + mu * y * x[k]
                    b=b + mu*y
                    wx=sum([x[m]*w[m] for m in range(dimi)])
                    tmp=y*(wx+b)
                    print j,x,y,w,b,tmp
                    loopend=False
            if loopend:
                print "train done"
                return w,b
        return None
    def dualtrain(self,data,mu=1,maxloopcnt=10000):
        datanum=len(data)
        dimi=len(data[0][0])
        gram=[
                [
                    sum( [data[i][0][k] * data[j][0][k]
                      for k in range(dimi)])
                for j in range(datanum) ]
              for i in range(datanum)]
        print gram
        alpha=[0]*datanum
        b=0
        for  i in range(maxloopcnt):
            loopend=True
            for j in range(datanum):
                tmp=sum([ alpha[k]*mu*data[k][1]*gram[k][j]  \
                           for k in range(datanum)])+ b
                tmp *= data[j][1]
                #print 'dual',j,data[j][0],data[j][1],alpha,b,tmp
                while tmp <= 0:
                    alpha[j]+=1
                    b +=mu*data[j][1]
                    tmp=sum([ alpha[k]*mu*data[k][1]*gram[k][j]  \
                           for k in range(datanum)])+ b
                    tmp *=data[j][1]
                    loopend=False
                    print 'dual change',j,data[j][0],data[j][1],alpha,b,tmp
            if loopend :
                return alpha,b
        return None
                        
class perception():
    def __init__(self,w,b):
        self.w=w
        self.b=b
    def percept(self,x):
        tmp = sum([self.w[i] * x[i] for i in range(len(x))])+self.b
        if tmp >0:
            return 1
        elif tmp < 0:
            return -1
        else:
            return 0            
            
if __name__=='__main__':
    print 'welcome to use perception tool'
    data=[((3,3),1),((4,3),1),((1,1),-1)]
    print 'data',data
    tr = train()
    w,b=tr.run(data)
    alpha,b=tr.dualtrain(data)
    print 'w,b',w,b
    per =perception(w=w,b=b)
    print per.percept((1,1))
