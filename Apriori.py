#每个数是一个个体，每一行是一条购买记录

import time
def compare(a,b):
    if len(a) == 1:
        return a + b
    else:
        count = 0
        for i in range(0,len(a)):
            if a[i] == b[i]:
                count +=1
            else:
                break
        if count ==len(a) - 1:
            if b[-1] > a[-1]:
                return a + [b[-1]]
            else:
                return b + [a[-1]]

        else:
            return -1

def link(L,C,m):
    for i in range(0, len(L)):
        for j in range(i+1, len(L)):
            new = compare(L[i][0],L[j][0])
            if new != -1:
                C.append([new,0])
    print("C",m,":",len(C))
    #print(C)

def search(data,C,m):
    t0 = time.time()
    print("how many to search:",len(C))
    for i in range(0,len(C)):
        for k in range(0,len(data)):
            """p = 0
            d = 0
            if C[i][0][p] == data[k][d]"""
            flag_1 = 1
            for j in range(0,m):
                if data[k].count(C[i][0][j]) == 0:
                    flag_1 = 0
                    break
            if flag_1 == 1:
                C[i][1] += 1
    print("search:")
    print(time.time() - t0, 's')
    print("after")
    #print(C)

def cut(C,L,m):
    t0 = time.time()
    check = [0]*len(C)
    for i in range(0,len(C)):
        flag2 = 1
        for j in range(0,m):
            temp = C[i][0].copy()
            #print("before",temp)
            temp.remove(temp[j])
            #print("then", temp)
            flag1 = 0
            for k in range (0,len(L)):
                #print(L[k])
                if temp == L[k][0]:
                    flag1 = 1
                    #print("yes")
                    break
            if flag1 == 0 :
                flag2 = 0
                break
        if flag2 == 0:
            check[i] = 1
    i = 0
    newC = []
    while i < len(check):
        if check[i] == 0:
            newC.append(C[i])
        i += 1
    print("cut:", len(newC))
    print(time.time() - t0, 's')
    return newC





def main():
    t0 = time.time()
    r = open('retail.dat', 'r')
    lines = r.readlines()
    r.close()
    w = open('A-result.dat','w')
    print(len(lines))
    data = []
    num = 0
    for i in range(0,len(lines)):
        temp = lines[i].split(" ")
        d = []
        for j in range(0,len(temp)-1):
            d.append(int(temp[j]))
        data.append(d)
        #print(d)
    print(data[2])

    support = 0.02 * len(lines)
    L = []
    C = []
    """第一次筛选出候选"""
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            if len(C) <= data[i][j]:
                for k in range(0, data[i][j] - len(C) + 1):
                    C.append(0)
                C[data[i][j]] += 1
            else:
                C[data[i][j]] += 1
    print("C1:",len(C))
    #print(C)
    """第一次项集的生成，[[1,2,3],3],项集+支持度"""
    for i in range(0, len(C)):
        if C[i] >= support:
            L.append([[i], C[i]])
    print("L1:",len(L))
    #print(L)
    m = 2
    num = len(L)
    while len(L)!= 0 :
        print("working...")
        C = []
        newC = []
        link(L,C,m)
        newC = cut(C,L,m)
        for i in range(0,len(L)):
            s = ""
            for j in range(0,len(L[i][0])):
                s = s + str(L[i][0][j]) + " "
            s = s + '[' + str(L[i][1]) + ']' + '\n'
            w.write(s)
        L =[]  #清空之前写入另一个文件
        search(data,newC,m)
        for i in range(0, len(newC)):
            if newC[i][1] >= support:
                L.append(newC[i])
        print("L",m,":",len(L))
        num += len(L)
        print("++++++++++++++++++++++++")
        m +=1
    print(time.time() - t0,'s')
    print(num)






if __name__=='__main__':
    main();