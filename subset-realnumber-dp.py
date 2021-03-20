#!/usr/bin/env python3
#_∗_coding: utf-8 _∗_

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
import numpy as np
import decimal 

decimal.getcontext().prec=7
decimal.getcontext().rounding=decimal.ROUND_HALF_DOWN 
print("context=",decimal.getcontext())



'''======================================================
整数表示的-多最优解算法
'''

cn =[1,2,3,4,5,6,7] 
nsum=14
vn=cn

cn =[1,2,3,4]
vn =[3,5,6,4]
vn =[1,2,3,4]
xr=[0,1]
nsum=7
print('cn=',cn)
print('vn=',vn)

# 顺序循环方式
# 指标递推：f(s_k+1)=max(v_k*x_k+f(s_k))
# 状态递推：定义状态为放入后的重量
# 则：s_0=0，s_1=s_0+c_1*x_1，s_2=s_1+c_2*x_2，即s_k=s_k-1+c_k*x_k
# 后面的程序实现中cn[0]表示c_1，cn[1]表示c_2
# 由于要放满，所以s_4=7是必须要达到的限制条件
#
#
infp=-1000
nphase=len(cn)
nstate=nsum
fv=np.zeros((nphase+1,nstate+1))
fv[:][:]=infp


def dpint():
    statest=0
    stateed=7
    phasest=1
    phaseed=4
    phase=0
    fv[phase][statest]=0

    #必须装满
    #建表
    for phase in range(phasest,phaseed+1):
        if(phase!=phaseed):
            for state in range(statest,stateed+1): #通过结构来递推了状态，因此不用把状态单独拿出来计算一遍
                #print('state=',state)
                if(state-cn[phase-1]>=statest):
                    fv[phase][state]=max(vn[phase-1]+fv[phase-1][state-cn[phase-1]],fv[phase-1][state])
                else:
                    fv[phase][state]=fv[phase-1][state]
        else:
            state=stateed
            #print('phase=',phase)
            #print('state=',state)
            fv[phase][state]=max(vn[phase-1]+fv[phase-1][state-cn[phase-1]],fv[phase-1][state])

    for x in fv:
        print(x)

    #循环查单个解，查表，结果输出
    state=stateed
    for phase in range(phaseed,phasest-1,-1):
        #print("phase=",phase," state=",state)
        if (fv[phase][state] !=fv[phase-1][state]):
            print("need:",phase," cn=",cn[phase-1]," vn=",vn[phase-1])
            state=state-cn[phase-1]

#dpint()


##递归查单个解
def findxp(phase,state,res):
    print("res=",res,"phase=",phase,"state=",state)
    print("fv[phase][state]=",fv[phase][state],"fv[phase-1][state]=",fv[phase-1][state])
    if phase==0:return 0
    if fv[phase][state] !=fv[phase-1][state]:
        res.append(phase)
        phase1=phase-1
        state1=state-cn[phase-1]
        print("res=",res,"phase=",phase1,"state=",state1)
        findxp(phase1,state1,res)
    else:
        phase1=phase-1
        state1=state
        print("res=",res,"phase=",phase1,"state=",state1)
        findxp(phase1,state1,res)
        
        


#递归查所有解
def findxp1(phase,state,res):
    #print("res=",res,"phase=",phase,"state=",state)
    #print("fv[phase][state]=",fv[phase][state],"fv[phase-1][state]=",fv[phase-1][state])
    if phase==0:
        print("res=",res)
        return 0
    if fv[phase][state] ==fv[phase-1][state-cn[phase-1]]+vn[phase-1]:
        res1=copy.deepcopy(res)
        res1.append(phase)
        phase1=phase-1
        state1=state-cn[phase-1]
        #print("res=",res,"phase=",phase1,"state=",state1)
        findxp1(phase1,state1,res1)
    if fv[phase][state] ==fv[phase-1][state]:
        phase1=phase-1
        state1=state
        #print("res=",res,"phase=",phase1,"state=",state1)
        findxp1(phase1,state1,res)
        



'''======================================================
实数表示的-多最优解算法
'''


# 顺序循环方式
# 指标递推：f(s_k+1)=max(v_k*x_k+f(s_k))
# 状态递推：定义状态为放入后的重量
# 则：s_0=0，s_1=s_0+c_1*x_1，s_2=s_1+c_2*x_2，即s_k=s_k-1+c_k*x_k
# 后面的程序实现中cn[0]表示c_1，cn[1]表示c_2
# 由于要放满，所以s_4=7是必须要达到的限制条件

cn=[805, 698, 619, 500, 2296,471,474,425,634,277,731,359,1828,1955] 
vn=cn
nsum=8403


cn =[decimal.Decimal(1.01),decimal.Decimal(2.00),decimal.Decimal(3.01),decimal.Decimal(4.00)]
vn =[decimal.Decimal(1.01),decimal.Decimal(2.00),decimal.Decimal(3.01),decimal.Decimal(4.00)]
nsum=decimal.Decimal(7.01)


vn=[decimal.Decimal(x) for x in [8.05, 6.98, 6.19, 5.00, 22.96,4.71,4.74,4.25,6.34,2.77,7.31,3.59,18.28,19.55]]
cn=[decimal.Decimal(x) for x in [8.05, 6.98, 6.19, 5.00, 22.96,4.71,4.74,4.25,6.34,2.77,7.31,3.59,18.28,19.55]]
nsum=decimal.Decimal(84.03)


xr=[0,1]
fv=[]
phasest=1
phaseed=len(cn)
stateed=nsum
def dpreal():

    phase=0
    fv.append({})
    fv[phase][decimal.Decimal(0.00)]=decimal.Decimal(0.00)

    #必须装满
    #建表
    for phase in range(phasest,phaseed+1):
        fv.append({})
        for i in range(len(fv[phase-1])): #通过字典来表示状态
            state=list(fv[phase-1].keys())[i]
            for x in xr:
                state1=state+cn[phase-1]*x+decimal.Decimal(0.00)
                if abs(state1<=0.0000001): state1=decimal.Decimal(0.00)
                f=fv[phase-1][state]+vn[phase-1]*x+decimal.Decimal(0.00)
                if state1 <= stateed+decimal.Decimal(0.000001):
                    if state1 not in fv[phase]:
                        fv[phase][state1]=f
                    else:
                        fv[phase][state1]=max(fv[phase][state1],f)

    for x in fv:
        print(x)

    #循环查单个解，查表，结果输出
    state=stateed
    for phase in range(phaseed,phasest-1,-1):
        #print("phase=",phase," state=",state)
        if (state not in fv[phase-1]):
            print("need:",phase," cn=",cn[phase-1]+decimal.Decimal(0.00)," vn=",vn[phase-1]+decimal.Decimal(0.00))
            state=state-cn[phase-1]
        else:
            if (fv[phase][state] !=fv[phase-1][state]):
                print("need:",phase," cn=",cn[phase-1]+decimal.Decimal(0.00)," vn=",vn[phase-1]+decimal.Decimal(0.00))
                state=state-cn[phase-1]

dpreal()

#print("cn=",cn)
print()
for x in fv:
    print(x)


print(nsum+decimal.Decimal(0.00) in fv[4])


#递归查所有解
def findxp2(phase,state,res):
    state=state+decimal.Decimal(0.00)
    #print("res=",res,"phase=",phase,"state=",state)
    #print("fv[phase][state]=",fv[phase][state])
    if phase==0:
        print("res=",res)
        suma=0
        stra=""
        for x in res:
            suma+=cn[x-1]
            stra+="+"+str(cn[x-1]+decimal.Decimal(0.00))
        print("sum=",suma)
        print("str=",stra)
        return 0
    state1=state-cn[phase-1]
    if abs(state1<=0.0000001): state1=decimal.Decimal(0.00)
    #print("state1=",state1)
    if state1 in fv[phase-1]:
        if abs(fv[phase][state] - (fv[phase-1][state1]+vn[phase-1]))<0.00001:
            res1=copy.deepcopy(res)
            res1.append(phase)
            phase1=phase-1
            #print("res=",res,"phase=",phase1,"state=",state1)
            findxp2(phase1,state1,res1)
    if state in fv[phase-1]:
        #print("state=",state)
        if abs(fv[phase][state]-fv[phase-1][state])<0.00001:
            phase1=phase-1
            state1=state
            #print("res=",res,"phase=",phase1,"state=",state1)
            findxp2(phase1,state1,res)
    return 0

findxp2(len(cn),nsum,[])