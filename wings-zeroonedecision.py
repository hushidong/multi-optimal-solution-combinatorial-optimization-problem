

"""
python基础测试
"""
import os
import string
import re
import sys
import datetime
import time
import copy
import json
import operator #数学计算操作符
import random
import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as mpl     #import matplotlib as mpl
#设置汉字格式
# sans-serif就是无衬线字体，是一种通用字体族。
# 常见的无衬线字体有 Trebuchet MS, Tahoma, Verdana, Arial, Helvetica,SimHei 中文的幼圆、隶书等等
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体 FangSong
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


import decimal 

nwings1=0
cn1=[]
vn1=[]
vc1={}
fv=np.zeros((3,3))

#读取菜单并根据购买鸡翅的数量构建代价和价值表
def readmenu(nwings):
    infile = open('menu.txt', 'r') #数据文件
    flines=infile.readlines()
    infile.close()
    dataset=flines[1:]
    dataset[-1]=dataset[-1]+"\n"
    #print('dataset=',dataset)
    datastr=[]
    for d1 in dataset:
        x=str.split(d1[:-1],",")
        y=[]
        for e in x:
            if e != "":
                y.append(e)
        datastr.append(y)

    number=[]
    money=[]
    vc={}
    n=len(datastr)
    for x in datastr:
        number.append(int(x[0]))
        money.append(float(x[1]))
        vc[int(x[0])]=float(x[1])
    #print('number=',number)
    #print('money=',money)

    cn=[]
    vn=[]
    for i in range(n):
        if number[i]<=nwings:
            mc=nwings//number[i]
            cn.extend([number[i]]*mc)
            vn.extend([money[i]]*mc)
    #print('len(cn)=',len(cn))
    #print('cn=',cn)
    #print('vn=',vn)
    return nwings,cn,vn,vc



#利用遍历的方法-列出附近的所有解
def sch_emuration_all():
    data=cn1
    vc=copy.deepcopy(vc1)
    cn=copy.deepcopy(cn1)
    vn=copy.deepcopy(vn1)
    suma=nwings1
    
    lendata=len(cn)
    res_data=[]
    res_st=100000.0
    i=0
    for k in range(1,lendata+1):
        for da in itertools.combinations(data,k):
            i=i+1
            sumt=sum(da)
            if (sumt == suma):
                sumb=0.0
                for x in da:
                    sumb+=vc[x]
                if sumb<res_st:
                    res_st=sumb
                    res=copy.deepcopy(da)
                    res_data=[res]
                elif sumb==res_st:
                    res=copy.deepcopy(da)
                    res_data.append(res)
    print("res=",res_data)




##采用整数规划的隐枚举法-宽度搜索
def implicitenum():
    nsum=nwings1
    #
    cn=copy.deepcopy(cn1)
    vn=copy.deepcopy(vn1)

    #
    #cn=sorted(data)
    #vn=sorted(data)
    #
    #cn=sorted(data,reverse=True)
    #vn=sorted(data,reverse=True)

    #print("nsum=",nsum)
    maxvrec=1000000
    pathrec=[]
                    #目标值，路径信息，阶段，状态
    root=[0,[],0,0] #fv，path，phase，state
    quene=[root]
    nleaf=0
    while quene:
        #print("quene=",quene)
        node=quene[0]
        #print("node=",node)
        quene.remove(node)
        phase=node[2]
        state=node[3]
        if phase==(len(cn)-1):
            nleaf+=1

        if abs(state-nsum)<0.00001:
            #print('sum(node[1])=',state)
            if node[0]<maxvrec-0.000001:
                maxvrec=node[0]
                pathrec=[node[1]]
            elif abs(node[0]-maxvrec)<0.000001 and node[1] not in pathrec:
                pathrec.append(node[1])
        if state>nsum+0.1:
            pass
        else:
            if phase<len(cn):
                c1=cn[phase]
                v1=vn[phase]

                sumv1=node[0]+v1
                path1=[]
                path1[:]=node[1][:]
                path1.append(c1)
                subnode1=[sumv1,path1,phase+1,state+c1]
                quene.append(subnode1)

                sumv2=node[0]
                path2=[]
                path2[:]=node[1][:]
                subnode2=[sumv2,path2,phase+1,state]
                quene.append(subnode2)

    #print("pathrec=",pathrec)
    #print("nleaf=",nleaf)



##采用整数规划的隐枚举法-宽度搜索-中间规约
def implicitenum2():
    nsum=nwings1
    #
    cn=copy.deepcopy(cn1)
    vn=copy.deepcopy(vn1)
    #
    #cn=sorted(data)
    #vn=sorted(data)
    #
    #cn=sorted(data,reverse=True)
    #vn=sorted(data,reverse=True)

    #print("nsum=",nsum)
    maxvrec=10000000
    pathrec=[]
                    #目标值，路径信息，阶段，状态
    root=[0,[],0,0] #fv，path，phase，state
    quene=[root]
    nleaf=0
    while quene:
        #print("quene=",quene)
        node=quene[0]
        #print("node=",node)
        quene.remove(node)
        phase=node[2]
        state=node[3]
        if phase==(len(cn)-1):
            nleaf+=1

        if abs(state-nsum)<0.00001:
            #print('sum(node[1])=',node)
            if node[0]<maxvrec-0.000001:
                maxvrec=node[0]
                pathrec=[node[1]]
            elif abs(node[0]-maxvrec)<0.000001 and node[1] not in pathrec:
                pathrec.append(node[1])
        if state>nsum+0.1:
            pass
        else:
            if phase<len(cn):
                c1=cn[phase]
                v1=vn[phase]

                for x in [1,0]: #原来的0,1有问题，反一下就解决了。因为使用0，1的话，会把同样数量的前一次选择删除掉。
                    sumv1=node[0]+v1*x
                    path1=copy.deepcopy(node[1])
                    if x==1:path1.append(c1)

                    #做规约，如果状态相同，路径对应的信息也相同（路径可能是不同的，但由于多次选择相同的数量，使其信息会相同），自然不用再添加，不管阶段是否相同。
                    flagsamestatepath=False
                    for nd in quene:
                        if nd[3]==state+c1*x and nd[1]==path1:
                            quene.remove(nd) #删除全部结果的节点
                            flagsamestatepath=True

                    if flagsamestatepath: #如果有相同的节点并已删除，那么就把本节点进去，然后continue
                        subnode1=[sumv1,path1,phase+1,state+c1*x]
                        quene.append(subnode1)
                        continue

                    #做规约，状态相同，且阶段相同，那么只留最优的方案。如果都是最优，那么把路径加进去
                    flagsamestatephase=False
                    samend=[]
                    for nd in quene:
                        if nd[3]==state+c1*x and nd[2]==phase+1:
                            samend=nd
                            flagsamestatephase=True
                            break
                    if flagsamestatephase:
                        if samend[0]==sumv1:
                            samend[1]=[samend[1],path1]
                        elif samend[0]>sumv1:
                            quene.remove(samend)
                            subnode1=[sumv1,path1,phase+1,state+c1*x]
                            quene.append(subnode1)
                    else:
                        subnode1=[sumv1,path1,phase+1,state+c1*x]
                        quene.append(subnode1)

    print("pathrec=",pathrec)
    print("nleaf=",nleaf)



# 顺序循环方式
# 指标递推：f(s_k+1)=max(v_k*x_k+f(s_k))
# 状态递推：定义状态为放入后的重量
# 则：s_0=0，s_1=s_0+c_1*x_1，s_2=s_1+c_2*x_2，即s_k=s_k-1+c_k*x_k
# 后面的程序实现中cn[0]表示c_1，cn[1]表示c_2
# 由于要放满，所以s_4=7是必须要达到的限制条件
#
#
def dpint():
    cn=copy.deepcopy(cn1)
    vn=copy.deepcopy(vn1)
    nstate=nwings1

    infp=1000
    nphase=len(cn)
    fv=np.zeros((nphase+1,nstate+1))
    fv[:][:]=infp

    statest=0
    stateed=nstate
    phasest=1
    phaseed=nphase
    phase=0
    fv[phase][statest]=0

    #必须装满
    #建表
    for phase in range(phasest,phaseed+1):
        if(phase!=phaseed):
            for state in range(statest,stateed+1): #通过结构来递推了状态，因此不用把状态单独拿出来计算一遍
                #print('state=',state)
                if(state-cn[phase-1]>=statest):
                    fv[phase][state]=min(vn[phase-1]+fv[phase-1][state-cn[phase-1]],fv[phase-1][state])
                else:
                    fv[phase][state]=fv[phase-1][state]
        else:
            state=stateed
            #print('phase=',phase)
            #print('state=',state)
            fv[phase][state]=min(vn[phase-1]+fv[phase-1][state-cn[phase-1]],fv[phase-1][state])

    #for x in fv:
    #    print(x)

    return fv

recres=[]
#递归查所有解，等于是深度搜索
def findxp1(phase,state,res):
    #print("res=",res,"phase=",phase,"state=",state)
    #print("fv[phase][state]=",fv[phase][state],"fv[phase-1][state]=",fv[phase-1][state])
    if state==0: #phase==0 or 
        #print("res=",res)
        if res not in recres:
            recres.append(res)
        return 0
    #print("state-cn1[phase-1]=",state-cn1[phase-1])
    if state-cn1[phase-1]>=0 :
        if abs(fv[phase][state] - fv[phase-1][state-cn1[phase-1]]-vn1[phase-1])<0.000001:
            res1=copy.deepcopy(res)
            res1.append(cn1[phase-1])
            phase1=phase-1
            state1=state-cn1[phase-1]
            #print("res=",res,"phase=",phase1,"state=",state1)
            findxp1(phase1,state1,res1)
    if abs(fv[phase][state]-fv[phase-1][state])<0.000001:
        phase1=phase-1
        state1=state
        #print("res=",res,"phase=",phase1,"state=",state1)
        findxp1(phase1,state1,res)



#循环查找所有解，采用宽度搜索  
def findxpbfs():
    nwings=nwings1
    cn=copy.deepcopy(cn1)
    vn=copy.deepcopy(vn1)
    minfe=fv[-1][-1]

    root=[]
    for p in range(len(cn)-1,-1,-1):
        for s in range(0,nwings+1):
            if s+cn[p]==nwings and abs(fv[p][s]+vn[p]-minfe)<0.000001:
                            #phase,state,fv[i][v],parent,path,pathcn
                root.append([p,s,fv[p][s],0,[p],[cn[p]]])
    #print("root=",root)

    seqt=[]
    for rootnode in root:
        opened=[]
        opened.append(rootnode)
        #closed=[]
        while opened:
            node=opened[0]
            opened.remove(node)
            #closed.append(node)
            #print('opened=',opened)
            #print('closed=',closed)

            if node[1]==0: #
                #print('find solution')
                path=node[4]
                pathcn=node[5]
                #print('solution=',path,pathcn)
                if pathcn not in seqt:
                    seqt.append(pathcn)
            else: #
                for p in range(node[0],0,-1):
                    for s in range(0,node[1]):
                        if s+cn[p]==node[1] and abs(fv[p][s]+vn[p]-node[2])<0.000001:
                            #i,v,fv[i][v],fe[i][v],parent,path
                            parent=node[0]
                            path=copy.deepcopy(node[4])
                            path.append(p)
                            pathcn=copy.deepcopy(node[5])
                            pathcn.append(cn[p])
                            flagexist=False
                            for subnode in opened:
                                if pathcn == subnode[5]:#这里做了路径信息相同情况下的限制，如果相同那么就无法继续计算了。
                                    flagexist=True
                                    break
                            if not flagexist:
                                opened.append([p,s,fv[p][s],parent,path,pathcn])
    #print("seqt=",seqt)
    return seqt


#显示结果
def outres(seqt):
    rest=[]
    for seq in seqt:
        res={}
        resc=seq
        resv=[vc1[x] for x in seq]
        res["number"]=resc
        res["money"]=resv
        if res not in rest:
            rest.append(res)
    #print(rest)

    print("最划算的组合方案数为：",len(rest))
    print("包括方案为：")
    for res in rest:
        print(res["number"],sum(res["money"]))
    print("在该组合方案下，购买%d只鸡翅的价格为:%.2f"%(nwings1,sum(rest[0]["money"])))


if __name__ == "__main__":
    

    '''
    buynumbers=[4,8,12,16,20,24,32,40,48,56,72,88,104,110,120,130,140,152,160,184,200,215,232,256,276]
    #buynumbers=[4,8,12,16,20,24,32,40,48]
    #buynumbers=[4]
    magnitudes=[]
    computimes=[]
    solutionsn=[]
    phasetotal=[]
    
    for number  in range(4,301):
        print("number=",number)
        nwings1,cn1,vn1,vc1=readmenu(number)
        recres=[]
        t1=time.process_time()
        #隐枚举
        #implicitenum()
        #递归的查表的动态规划
        #fv=dpint()
        #findxp1(len(cn1),nwings1,[])
        #循环的查表的动态规划
        fv=dpint()
        recres=findxpbfs()
        t2=time.process_time()
        timelapsed=t2-t1
        
        computimes.append(timelapsed)
        solutionsn.append(len(recres))
        phasetotal.append(len(cn1))
        magnitudes.append(number*len(cn1)+len(cn1)*len(recres))
        print('time elapsed',timelapsed)
        print("recres=",recres)

    print('buynumbers=',buynumbers)
    print('magnitudes=',magnitudes)
    print('computimes=',computimes)
    print('solutionsn=',solutionsn)
    print('phasetotal=',phasetotal)
    '''


    '''画图
    buynumbers= [4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 72, 88, 104, 110, 120, 130, 140, 152, 160, 184, 200, 218, 232, 256, 276]
    magnitudes= [4, 48, 156, 336, 600, 960, 1888, 3080, 4560, 6440, 11016, 16544, 23504, 26510, 32280, 37310, 43820, 51680, 57600, 76728, 91400, 107692, 122496, 150272, 174708]

    computimes= [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.015625, 0.0, 0.265625, 0.03125, 0.71875, 0.203125, 0.046875, 0.375, 81.609375, 0.171875, 0.703125, 0.09375, 3.8125, 1.03125, 0.15625, 67.890625, 30.765625, 10.1875, 2.8125]
    solutionsn= [1, 2, 2, 5, 15, 6, 3, 5, 68, 3, 54, 22, 7, 20, 211, 18, 22, 7, 36, 14, 7, 43, 33, 17, 10]
    phasetotal= [1, 6, 13, 21, 30, 40, 59, 77, 95, 115, 153, 188, 226, 241, 269, 287, 313, 340, 360, 417, 457, 485, 528, 587, 633]

    computimes2= [0.0, 0.0, 0.0, 0.0, 0.0, 0.015625, 0.0, 0.0, 0.03125, 0.015625, 0.078125, 0.09375, 0.078125, 0.203125, 1.0, 0.3125, 0.328125, 0.3125, 0.90625, 0.65625, 0.4375, 2.0, 3.265625, 2.21875, 2.328125]
    solutionsn= [1, 2, 2, 5, 15, 6, 3, 5, 68, 3, 54, 22, 7, 20, 211, 18, 22, 7, 36, 14, 7, 43, 33, 17, 10]

    buynumbers1= [4, 8, 12, 16, 20, 24, 28]
    computimes1= [0.0, 0.0, 0.0, 0.015625, 0.09375, 2.265625, 99.390625]

    y1= [x/40000 for x in magnitudes]
    #y2= [float(solutionsn[i])**(phasetotal[i]/2)/15000.0 for i in range(len(buynumbers))]

    #第一个图
    plt.figure() #绘图初始化
    plt.plot(buynumbers,computimes,'r*-',linewidth=1,label='动态规划法耗时') #绘制一条
    plt.plot(buynumbers1,computimes1,'g+-',linewidth=1,label='隐枚举法耗时') #绘制一条
    plt.plot(buynumbers,y1,'b-',linewidth=1,label='根据量级估计时间') #绘制一条
    #plt.plot(buynumbers,y2,'p-',linewidth=1,label='magnitude2') #绘制一条
    plt.legend(loc='upper right',frameon=True) #显示图例
    plt.xlabel("鸡翅数量") #增加x轴说明
    plt.ylabel("时间(s)") #增加y轴说明
    #plt.xticks(xdtick,ymtick,rotation=40)
    plt.show()

    #第二个图
    plt.figure() #绘图初始化
    plt.plot(buynumbers,computimes,'r*-',linewidth=1,label='深度优先递归查表') #绘制一条
    plt.plot(buynumbers,computimes2,'p-',linewidth=1,label='改进的宽度优先查表') #绘制一条
    plt.plot(buynumbers,y1,'b-',linewidth=1,label='根据量级估计时间') #绘制一条
    plt.legend(loc='upper right',frameon=True) #显示图例
    plt.xlabel("鸡翅数量") #增加x轴说明
    plt.ylabel("时间(s)") #增加y轴说明
    #plt.xticks(xdtick,ymtick,rotation=40)
    plt.show()
    '''

    #'''画图
    buynumbers=range(4,301)
    
    magnitudes= [5, 12, 21, 32, 60, 70, 108, 140, 182, 224, 320, 306, 441, 572, 550, 676, 1050, 800, 1122, 1575, 1200, 1092, 1188, 1288, 1450, 1581, 1848, 1792, 2065, 2340, 2196, 2624, 3174, 2760, 3220, 4047, 3465, 4158, 5670, 3969, 5376, 8008, 4895, 6764, 11020, 5760, 5200, 5252, 5616, 5616, 6264, 6710, 6785, 7192, 8190, 7254, 8820, 10206, 8568, 10062, 13200, 9782, 12330, 16851, 11259, 14700, 23944, 12556, 19278, 32130, 14688, 12089, 12402, 12880, 13120, 13776, 15480, 14616, 15660, 17574, 16109, 18300, 21594, 17296, 20680, 27260, 20094, 25273, 36582, 21909, 29949, 49126, 24871, 37202, 67520, 27264, 22660, 22660, 23532, 23310, 25086, 27258, 25641, 27027, 31758, 27255, 31330, 37355, 30381, 35321, 48057, 32630, 41745, 61965, 36210, 49858, 89039, 40770, 63180, 117720, 45257, 35346, 36120, 36960, 37073, 39054, 42476, 39319, 42632, 49098, 42042, 48438, 59494, 45602, 54416, 74784, 50706, 65104, 98908, 54810, 79781, 140400, 61425, 98427, 191552, 67568, 52235, 52235, 54060, 53694, 57436, 61766, 57728, 61600, 71808, 59840, 70560, 87242, 66246, 79422, 113036, 71410, 94350, 147260, 79590, 116280, 213331, 87010, 145522, 291044, 97388, 70952, 71857, 73842, 72651, 77018, 86100, 78310, 84870, 99774, 82566, 96140, 121510, 88410, 108454, 158898, 96954, 130416, 214020, 106575, 160515, 303534, 118014, 202878, 426438, 131865, 94599, 94599, 97341, 95931, 102786, 112288, 101152, 109510, 131880, 106898, 127995, 163737, 116160, 143748, 214412, 125130, 175015, 290966, 139308, 214396, 421000, 154114, 274135, 585995, 174587, 119995, 119995, 123600, 121965, 129750, 143028, 128625, 139920, 168432, 135382, 160200, 208650, 144450, 181844, 275994, 160632, 224112, 382814, 176808, 279057, 556640, 195789, 356379, 784785, 220350, 148200, 147630, 154593, 151641, 162099, 179288, 160251, 173752, 211680, 166687, 200515, 265068, 180294, 228054, 356964, 197230, 281504, 487616, 218631, 350175, 721754, 243886, 457282, 1025388, 278570, 179894, 181038, 186735, 182304, 195272, 219945, 193500, 211888, 260338, 201864, 244400, 328308, 218115, 283764, 448200, 241454, 348841, 617900, 265864, 440832, 911242, 297675, 570876, 1299048, 338640, 217222]
    computimes3= [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.015625, 0.0, 0.0, 0.0, 0.0, 0.015625, 0.0, 0.0, 0.0, 0.0, 0.015625, 0.0, 0.0, 0.0, 0.015625, 0.0, 0.0, 0.015625, 0.0, 0.0, 0.015625, 0.0, 0.015625, 0.015625, 0.015625, 0.0, 0.015625, 0.015625, 0.015625, 0.03125, 0.015625, 0.015625, 0.0, 0.03125, 0.015625, 0.015625, 0.0, 0.03125, 0.015625, 0.015625, 0.015625, 0.015625, 0.03125, 0.015625, 0.015625, 0.0625, 0.015625, 0.0625, 0.046875, 0.046875, 0.0625, 0.109375, 0.03125, 0.0625, 0.125, 0.03125, 0.03125, 0.015625, 0.03125, 0.03125, 0.046875, 0.046875, 0.03125, 0.0625, 0.078125, 0.046875, 0.0625, 0.15625, 0.046875, 0.09375, 0.140625, 0.0625, 0.109375, 0.234375, 0.09375, 0.171875, 0.296875, 0.078125, 0.203125, 0.484375, 0.09375, 0.0625, 0.046875, 0.078125, 0.0625, 0.09375, 0.140625, 0.0625, 0.140625, 0.234375, 0.09375, 0.234375, 0.34375, 0.09375, 0.34375, 0.53125, 0.15625, 0.390625, 0.765625, 0.21875, 0.4375, 1.078125, 0.25, 0.59375, 1.46875, 0.25, 0.078125, 0.125, 0.140625, 0.125, 0.203125, 0.328125, 0.125, 0.28125, 0.625, 0.1875, 0.46875, 0.828125, 0.21875, 0.53125, 1.109375, 0.265625, 0.765625, 1.46875, 0.28125, 0.796875, 1.890625, 0.390625, 1.03125, 2.515625, 0.453125, 0.125, 0.171875, 0.234375, 0.171875, 0.34375, 0.5625, 0.21875, 0.5, 1.015625, 0.3125, 0.78125, 1.609375, 0.375, 1.046875, 2.15625, 0.546875, 1.28125, 2.84375, 0.640625, 1.765625, 4.796875, 0.796875, 2.25, 6.328125, 0.96875, 0.1875, 0.3125, 0.46875, 0.328125, 0.578125, 1.078125, 0.359375, 1.140625, 2.46875, 0.71875, 1.6875, 3.59375, 0.796875, 1.984375, 4.453125, 1.0, 2.625, 6.0, 1.21875, 3.828125, 8.609375, 1.453125, 4.9375, 11.8125, 1.984375, 0.390625, 0.625, 0.921875, 0.578125, 1.0625, 2.28125, 0.765625, 1.875, 4.03125, 1.078125, 3.75, 7.46875, 1.515625, 4.046875, 9.96875, 2.0625, 6.140625, 12.296875, 2.171875, 6.640625, 17.78125, 2.828125, 8.859375, 23.65625, 2.96875, 0.484375, 0.765625, 1.203125, 0.78125, 1.5, 3.046875, 0.984375, 2.5625, 5.875, 1.546875, 4.5, 10.1875, 2.25, 5.625, 12.90625, 3.390625, 8.515625, 19.4375, 3.34375, 10.296875, 27.0625, 4.1875, 13.4375, 34.640625, 4.421875, 0.75, 1.234375, 2.25, 1.4375, 2.953125, 6.546875, 2.21875, 4.921875, 11.171875, 3.046875, 7.5625, 16.8125, 3.140625, 9.15625, 23.578125, 5.46875, 13.15625, 32.0, 6.125, 17.796875, 48.0625, 6.953125, 21.8125, 55.734375, 7.390625, 1.015625, 1.734375, 2.875, 1.640625, 3.5, 7.6875, 2.390625, 6.21875, 14.453125, 3.703125, 10.90625, 26.265625, 6.625, 16.34375, 36.390625, 7.484375, 20.28125, 47.515625, 8.03125, 26.46875, 67.78125, 10.671875, 32.625, 91.890625, 11.75, 1.796875]
    solutionsn= [1, 1, 1, 1, 2, 1, 2, 3, 2, 3, 6, 2, 5, 9, 4, 7, 15, 4, 11, 22, 6, 1, 1, 1, 1, 2, 3, 1, 3, 6, 2, 6, 10, 3, 8, 18, 5, 13, 28, 6, 20, 46, 9, 29, 68, 11, 2, 1, 2, 1, 4, 6, 3, 5, 12, 3, 10, 20, 6, 15, 36, 8, 24, 56, 13, 36, 94, 15, 54, 137, 22, 2, 2, 3, 2, 5, 10, 3, 8, 18, 5, 15, 32, 7, 22, 56, 12, 36, 90, 16, 55, 147, 23, 81, 222, 29, 3, 2, 4, 2, 7, 13, 5, 10, 26, 6, 20, 44, 11, 30, 79, 15, 49, 126, 24, 75, 211, 30, 112, 313, 43, 4, 3, 5, 3, 9, 18, 6, 14, 34, 9, 27, 61, 14, 41, 107, 22, 67, 174, 31, 103, 287, 43, 154, 436, 57, 5, 4, 7, 4, 12, 23, 8, 18, 46, 11, 36, 80, 19, 54, 144, 28, 89, 231, 42, 137, 387, 55, 205, 581, 77, 6, 5, 9, 5, 15, 30, 10, 23, 58, 14, 45, 104, 23, 69, 184, 36, 113, 300, 52, 175, 498, 71, 262, 756, 96, 7, 6, 11, 6, 18, 37, 12, 28, 72, 17, 55, 128, 28, 84, 229, 43, 139, 372, 64, 215, 622, 86, 323, 942, 119, 8, 7, 13, 7, 21, 44, 14, 33, 86, 20, 65, 154, 33, 100, 274, 51, 165, 449, 75, 257, 749, 103, 386, 1141, 141, 10, 8, 15, 8, 25, 52, 17, 39, 102, 24, 77, 183, 40, 119, 327, 61, 197, 535, 91, 306, 896, 123, 462, 1365, 171, 11, 10, 18, 10, 29, 61, 19, 46, 120, 28, 91, 216, 46, 140, 386, 72, 232, 633, 105, 362, 1059, 145, 545, 1618, 199, 13]
    phasetotal= [1, 2, 3, 4, 6, 7, 9, 10, 13, 14, 16, 18, 21, 22, 25, 26, 30, 32, 34, 35, 40, 42, 44, 46, 50, 51, 56, 56, 59, 60, 61, 64, 69, 69, 70, 71, 77, 77, 81, 81, 84, 88, 89, 89, 95, 96, 100, 101, 104, 104, 108, 110, 115, 116, 117, 117, 126, 126, 126, 129, 132, 134, 137, 137, 139, 140, 146, 146, 153, 153, 153, 157, 159, 161, 164, 164, 172, 174, 174, 174, 181, 183, 183, 184, 188, 188, 197, 199, 201, 201, 201, 203, 209, 209, 211, 213, 220, 220, 222, 222, 226, 231, 231, 231, 237, 237, 241, 241, 247, 247, 249, 251, 253, 255, 255, 257, 269, 270, 270, 270, 271, 274, 280, 280, 283, 283, 287, 287, 292, 294, 294, 299, 302, 302, 304, 304, 313, 313, 313, 315, 323, 325, 325, 327, 328, 328, 337, 337, 340, 342, 346, 347, 352, 352, 352, 352, 360, 362, 366, 366, 367, 370, 370, 370, 379, 380, 383, 385, 386, 386, 388, 392, 397, 397, 397, 397, 410, 410, 414, 414, 417, 418, 419, 421, 422, 426, 429, 429, 435, 435, 435, 438, 442, 442, 447, 447, 457, 457, 457, 459, 463, 464, 464, 466, 471, 473, 483, 483, 484, 484, 484, 485, 493, 494, 494, 494, 500, 502, 503, 503, 509, 515, 515, 515, 519, 519, 522, 525, 528, 528, 533, 534, 535, 535, 538, 538, 552, 552, 554, 556, 557, 560, 561, 563, 565, 565, 570, 570, 579, 581, 581, 584, 587, 587, 588, 589, 595, 597, 597, 597, 604, 605, 608, 608, 609, 609, 619, 619, 623, 626, 626, 629, 633, 633, 633, 634, 645, 645, 646, 646, 647, 650, 654, 655, 663, 664, 667, 667, 668, 668, 672, 673, 675, 678, 678, 680, 694]
    y1= [x/80000 for x in magnitudes]

    fig = plt.figure() #绘图初始化
    ax1 = fig.add_subplot(111)
    ax1.plot(buynumbers,computimes3,'m-',linewidth=1,label='改进的宽度优先查表') #绘制一条
    ax1.plot(buynumbers,y1,'b-',linewidth=1,label='根据量级估计时间') #绘制一条
    ax2 = ax1.twinx()#使用ax1相同的x轴
    ax2.plot(buynumbers,solutionsn,'g',linewidth=1,label='解的数量')
    ax1.legend(loc='upper left',frameon=True) #显示图例
    ax2.legend(loc='upper right',frameon=True) #显示图例
    ax1.set_xlabel("鸡翅数量") #增加x轴说明
    ax1.set_ylabel("时间(s)") #增加y轴说明
    ax2.set_ylabel("解的数量") #增加y轴说明
    #plt.xticks(xdtick,ymtick,rotation=40)
    plt.show()
    #'''


    '''
    nwings1,cn1,vn1,vc1=readmenu(4)
    fv=dpint()
    print("fv=",fv)

    
    t1=time.process_time()
    recres1=findxpbfs()
    t2=time.process_time()
    timelapsed=t2-t1
    print('time elapsed',timelapsed)
    outres(recres1)
    '''
    
    '''
    nwings1,cn1,vn1,vc1=readmenu(4)
    fv=dpint()
    print("fv=",fv)
    recres=[]
    t1=time.process_time()
    findxp1(len(cn1),nwings1,[])
    t2=time.process_time()
    timelapsed=t2-t1
    print("len(recres)=",len(recres))
    print("len(recres)=",recres)
    print('time elapsed',timelapsed)
    recres2=recres
    outres(recres2)
    '''
    
    #print(nwings1,cn1,vn1,vc1)

    #sch_emuration_all()

    #implicitenum2()

    '''
    fv=dpint()
    print(fv.shape)

    print('len(cn1)=',len(cn1))
    findxp1(len(cn1),nwings1,[])
    

    for res in recres:
        sumb=0
        for x in res:
            sumb+=vc1[x]
        print("sumb=",sumb)
        print("res=",res)
    '''

    #findxpbfs()

