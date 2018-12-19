import time
import copy
def combine(lst):
    result = []
    def next_num(li=0, ni=0):
        if ni == l:
            result.append(copy.copy(tmp))
            return
        for lj in range(li, length):
            tmp[ni] = lst[lj]
            next_num(lj + 1, ni + 1)

    for i in range(1, len(lst) + 1):
        l = i
        tmp = [0] * l
        length = len(lst)
        next_num()
    return result

def getrest(la,lb):
    res = []
    for i in range(0,len(la)):
        flag = 0
        for j in range(0,len(lb)):
            if la[i] == lb[j]:
                flag = 1
                break
        if flag == 0:
            res.append(la[i])
    return res



def main():
    r = open('A-result.dat', 'r')
    lines = r.readlines()
    r.close()
    items = [] #二维数组存所有频繁项集
    freq = [] #一维数组存每个频繁项集的支持度
    confidence = 0.7 #置信度
    for i in range(0,len(lines)):
        temp = lines[i].split(" ")
        item = []
        a = temp[-1]
        b = a.split("[")
        a = b[1].split("]")
        s = float(a[0])
        for j in range(0,len(temp)-1): # 除去频繁度 为频繁项内容
            item.append(int(temp[j]))
        items.append(item)
        freq.append(s)
    w = open('rules.dat', 'w')
    count = 0
    for i in range(0,len(items)):
        if len(items[i]) == 1: #只有一个元素不产生规则
            continue
        else:
            r = combine(items[i])
            s = freq[i]
            for j in range(0,len(r)-1): #最后一个是全集，不考虑
                rest = getrest(items[i],r[j])
                index = items.index(r[j])
                conf = s/freq[index]
                if conf > confidence:
                    print(str(r[j])+"->"+str(rest)+ " = " + str(conf)[0:6])
                    count += 1
                    # w.write(str(r[j])+"->"+str(rest)+ " = " + str(conf))
                    # w.write("\n")
    print(count)





if __name__ == '__main__':
    main();
