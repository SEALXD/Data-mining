import copy  # 实现list的深复制
import time
support = 0

"""相同项目在同一层"""
""" headT[i] = [内容，频繁度，第一个节点]"""
class Node:
    def __init__(self,value):
        self.count = 1  # 计算频繁度 只要被创建这个节点就有一个频繁度
        self.value = value  # 存储该节点的内容
        self.children = []  # 子节点
        self.father = None  # 父节点
        self.next = None  # 头表对应的链表 存node


class FPTree():
    def __init__(self):
        self.freq = [] #保存结果

    def gen_L(self,data,datafreq):  #生成频繁一项集
        C = []
        L = []
        newfreq = []
        global support
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                if len(C) <= data[i][j]:
                    for k in range(0, data[i][j] - len(C) + 1):
                        C.append(0)
                    C[data[i][j]] += datafreq[i]  #对于初始的FPtree datafreq全部为1
                else:
                    C[data[i][j]] += datafreq[i]
        for i in range(0, len(C)):
            if C[i] >= support:
                L.append([i, C[i]])  #z支持度和内容
        return L


    def check_node(self,p,val):  #查找节点子节点
        if len(p.children) == 0:  # 没有子节点
            return -1
        else:
            for i in range(0,len(p.children)):
                if p.children[i].value == val:  # k即代表一项集中的某一项的脚标，说明该node有指向这一项的子节点
                    p = p.children[i]
                    return p  # 返回子节点
            return -1

    def takeSecond(self, elem):  # 排序规则
        return elem[1]

    def build(self,data,datafreq): #建树
        L = self.gen_L(data,datafreq)
        L.sort(key=self.takeSecond, reverse=True)
        # print("频繁1:",L)
        phead = [0]*len(L) #存放每个头表的指针
        headtable = L
        root = Node("root")
        for i in range(0,len(data)):
            k = 0
            point = root
            for j in range(0, len(data[i])):
                for k in range(0, len(L)):
                    if data[i][j] == L[k][0]:
                        cnode = self.check_node(point, L[k][0]) # 检查指针指向的父节点是否有该子节点
                        if cnode != -1:
                            cnode.count += datafreq[i]
                            point = cnode
                        else:
                            newnode = Node(L[k][0])  # 创建节点
                            newnode.count = datafreq[i]
                            newnode.father = (point)  # 链接父亲节点
                            if phead[k] == 0: #更新头表
                                headtable[k].append(newnode)
                                phead[k] = newnode
                            else:
                                phead[k].next = newnode
                                phead[k] = newnode
                            point.children.append(newnode)  # 作为子节点加入
                            point = newnode
                            #print("创建",newnode.value)

        # print("条件模式树：",self.levelOrder(root)) #建好树后打印
        return root,headtable

    def print_tree(self,root): #深度优先遍历打印所有节点
        node = root
        for i in range(0, len(node.children)):
            tnode = node.children[i]
            if len(tnode.children) == 0:
                print(tnode.value,tnode.count)
            else:
                self.print_tree(tnode)
                print(tnode.value, tnode.count)
        print("level")
        return 1

    def levelOrder(self, root): #层次优先遍历打印所有节点
        if not root:
            return []
        back = []  # 函数返回的数据
        curLevel = [[root]]  # 当前遍历树的层级，双层列表
        while curLevel:
            temp = []  # 遍历当前层级时存放的临时结点值
            nextLevel = []  # 下一层树结点
            for i in curLevel:
                for j in i:  # 注意，层级节点存放为双层列表
                    temp.append([j.value,j.count])
                    if len(j.children) != 0:  # 当前结点是否存在子结点
                        nextLevel.append(j.children)
            back.append(temp)
            curLevel = nextLevel
        return back



    def single_path(self,root): #若是单一路径，返回该路径以及该路径各节点的频繁度，否则返回-1
        node = root
        res = []
        num = []
        while 1:
            if len(node.children) == 1:
                node = node.children[0]
                res.append(node.value)
                num.append(node.count)
            elif len(node.children) == 0:
                break
            else:
                return -1,-1
        return res,num

    def pattern(self,headT,id): #自底向上遍历所有属于headT[id]的节点 得到条件模式库
        data = []
        datafreq = [] #记录每条data的频繁度
        hnode = headT[id][2]
        while hnode != None:  #遍历headT[id]链表上的结点
            node = hnode.father #从当前结点的父亲节点开始记录 因为当前结点值都相同
            temp = []
            count = hnode.count  #该记录的频繁度为 其对应叶子节点的频繁度
            while node.value != "root": #自底向上遍历
                temp.append(node.value)
                node = node.father
            if len(temp) !=0:
                temp.reverse()
                data.append(temp)
                datafreq.append(count)
            hnode = hnode.next

        # print(headT[id][2].value,"的条件模式基",data)
        # print("次数",datafreq)
        return data,datafreq

    def combine(self,lst):
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


    def fpgrowth(self,cpb,cpbfreq,follow): #模式基，后缀list
        if len(cpb) == 0:
            return 1
        else:
            root,headtable = self.build(cpb,cpbfreq)
            p,n= self.single_path(root) #返回路径及结点支持度
            if p != -1 :
                res = self.combine(p) #对该路径上的结点排列组合，每种支持度取其最小
                resnum = self.combine(n)
                for i in range(0,len(resnum)):
                    resnum[i] = min(resnum)
                    res[i] += follow
                    #print("check",resnum[i])
                    self.freq.append([res[i],resnum[i][0]]) #加入结果
                #print("目前：", self.freq)
                return 1
            else:
                for id in range(0,len(headtable)):
                    i = len(headtable) - 1 - id #逆序遍历
                    #print(headtable)
                    newfollow = follow + [headtable[i][0]]  #更新后缀和后缀的频繁度
                    self.freq.append([newfollow, headtable[i][1]]) #加入结果
                    newcpb,newcpbfreq= self.pattern(headtable,i)
                    self.fpgrowth(newcpb, newcpbfreq, newfollow)


def main():
    global support
    t0 = time.time()
    r = open('retail.dat', 'r')
    lines = r.readlines()
    r.close()
    print(len(lines))
    data = []
    datafreq = []
    support = 441  #7712
    for i in range(0, len(lines)):
    #for i in range(0, 300):
        temp = lines[i].split(" ")
        d = []
        for j in range(0, len(temp) - 1):
            d.append(int(temp[j]))
        data.append(d)
        datafreq.append(1)
    #print("测试数据样例：",data[2],datafreq[2])

    T = FPTree()
    T.fpgrowth(data,datafreq,[])
    w = open('FP-result.dat', 'w')
    for i in range(0,len(T.freq)):
        w.write(str(T.freq[i][0]))
        w.write("  ")
        w.write(str(T.freq[i][1]))
        w.write("\n")
    print("最终结果：")
    print(T.freq)
    print(len(T.freq))
    w.close()
    t = time.time()-t0
    print("用时：",t,"s")
    #s = input()


if __name__=='__main__':
    main();

