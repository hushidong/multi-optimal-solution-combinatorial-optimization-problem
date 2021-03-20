#!/usr/bin/env python3
#_∗_coding: utf-8 _∗_


"""
在一组数中，找到加和数最接近某个值得一系列数。
比如在：
[8.05, 6.98, 6.19, 5, 22.96,4.71,4.74,4.25,6.34,2.77,7.31,3.59,18.28,19.55]
中找到最接近84.03的一组数
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

data=[8.05, 6.98, 6.19, 5, 22.96,4.71,4.74,4.25,6.34,7.31,3.59,2.77,18.28,19.55] #,18.28



data=[805, 698, 619, 500, 2296,471,474,425,634,277,731,359,1828,1955] 
suma=8403

data=[8.05, 6.98, 6.19, 5, 22.96,4.71,4.74,4.25,6.34,7.31,3.59,2.77,18.28,19.55]
suma=84.03

#data=[3.5, 4.6, 2.8, 3.7] 
#suma=10.0

#分数型背包方法，没法应用到等价值问题中，（组合最优化：理论和算法）


##采用整数规划的隐枚举法-宽度搜索
def implicitenum():
	nsum=suma
	#
	cn=copy.deepcopy(data)
	vn=copy.deepcopy(data)
	#
	#cn=sorted(data)
	#vn=sorted(data)
	#
	#cn=sorted(data,reverse=True)
	#vn=sorted(data,reverse=True)

	print("nsum=",nsum)
	minvrec=1000000
	maxvrec=-1000000
	pathrec=[]
					#目标值，路径信息，阶段，状态
	root=[0,[],0,0] #fv，path，phase，state
	quene=[root]
	nleaf=0
	while quene:
		#print("quene=",quene)
		node=quene[0]
		quene.remove(node)
		phase=node[2]
		state=node[3]
		if phase==(len(cn)-1):
			nleaf+=1

		if abs(state-nsum)<0.00001:
			print('sum(node[1])=',state)
			if node[0]>maxvrec+0.00001:
				maxvrec=node[0]
				pathrec=[node[1]]
			elif abs(node[0]-maxvrec)<0.00001 and node[1] not in pathrec:
				pathrec.append(node[1])
			print("minvrec=",minvrec)
			print("pathrec=",pathrec)
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
	print("nleaf=",nleaf)



#利用遍历的方法-列出附近的所有解
def sch_emuration_all(de):
	lendata=len(data)
	res_data=[]
	res_st=0.0
	res_err=1000.0
	i=0
	for k in range(1,lendata+1):
		for da in itertools.combinations(data,k):
			i=i+1
			sumt=sum(da)
			#print('i=',i,' k=',k)
			#print('data=',da)
			#print('sumt=',sumt)
			ds=abs(sumt-suma)
			if (ds < res_err):
				#print('')
				#print('ds=',ds)
				#print('data=',da)
				#print('sum=',sumt)
				res_err=ds
				res_data[:]=da[:]
				res_st=sumt
			if (ds <= de):
				print('err=%.2f'%ds,' sum=%.2f'%sumt,' data=',sorted(da))

	print("")
	print('res_data=',sorted(res_data))
	print(res_st,res_err)


#利用遍历的方法
def sch_emuration():
	lendata=len(data)
	res_data=[]
	res_st=0.0
	res_err=1000.0
	i=0
	outflag=False
	for k in range(1,lendata+1):
		for da in itertools.combinations(data,k):
			i=i+1
			sumt=sum(da)
			#print('i=',i,' k=',k)
			#print('data=',da)
			#print('sumt=',sumt)
			ds=abs(sumt-suma)
			if (ds < res_err):
				#print('')
				#print('ds=',ds)
				#print('data=',da)
				#print('sum=',sumt)
				res_err=ds
				res_data[:]=da[:]
				res_st=sumt
				if(ds<0.0000001): 
					outflag=True
					break
					#pass
		if outflag: break
	
	print("")
	print('res_data=',sorted(res_data),' sum=',sum(res_data))
	print(res_st,res_err)


#利用组合的蒙特卡洛方法
def MC_combination():

	lendata=len(data)
	data1=[]
	res_data=[]
	res_st=0.02
	data1[:]=data[:]
	res_err=1000.0
	for i in range(10000):
		k=random.randrange(2,lendata+1) 
		data2=random.sample(data1, k)
		#print('i=',i,'k=',k)
		#print('data2=',data2)
		sumt=sum(data2)
		ds=abs(sumt-suma)
		if (ds < res_st):
			#print('')
			#print('ds=',ds)
			print('i=',i,'data2=',data2)
			#print('k=',k)
			print('sum=',sumt)
			res_err=ds
			res_data=data2
			#if( ds < 0.0000001): break
	
	#print("")
	#print('res_data=',sorted(res_data),' sum=',sum(res_data))
	print(res_st,res_err)
	


#利用排列的蒙特卡洛方法
def MC_permutation():
	data1=[]
	res_data=[]
	res_j=0
	res_jp=0
	res_s1=0
	res_s2=0
	res_err=100.0
	outflag=False

	for i in range(200000):
		data1[:]=data[:]
		random.shuffle(data1) 
		#print("data1=",data1)
		sumt=0
		for j in range(len(data1)):
			sumts=sumt
			sumt=sumt+data1[j]
			if(sumt>suma):
				ds1=abs(sumts-suma)
				ds2=abs(sumt-suma)
				ds=min(ds1,ds2)
				if (ds < res_err):
					#print('')
					#print('ds=',ds)
					#print('i=',i,'data1=',data1)
					#print('j=',j,data1[j])
					#print('sum=',sumts,sumt)
					res_err=ds
					res_data[:]=data1[:]
					res_jp=j
					if (ds1 < ds2):
						res_j=j
					else:
						res_j=j+1
					#print(ds1,ds2)
					#print(j,res_j)
					res_s1=sumts
					res_s2=sumt
				if(ds<0.000001): outflag=True
				break
		if outflag: break

	print("")
	print('permutes=',res_data)
	print(res_jp,res_s1,res_s2)
	print('res_data=',sorted(res_data[:res_j]),' sum=',sum(res_data[:res_j]))
	print(res_s1,res_s2,res_err)


				
if __name__ == "__main__":

	if False:
		#遍历的方法
		t1=time.process_time()
		sch_emuration()
		t2=time.process_time()
		print('time elapsed',t2-t1)

		#排列的MC方法
		t1=time.process_time()
		MC_combination()
		t2=time.process_time()
		print('time elapsed',t2-t1)
		

		#组合的MC方法
		t1=time.process_time()
		MC_permutation()
		t2=time.process_time()
		print('time elapsed',t2-t1)

		'''
		datan=sorted([3.59, 6.19, 7.31, 4.25, 18.28, 22.96, 4.71, 6.98, 5, 4.74])
		print(datan)
		print(sum(datan))
		'''

		print("")
		sch_emuration_all(0.05)


	#sch_emuration_all(0.1)

	#sch_emuration()

	#MC_combination()

	implicitenum()



	

	
	



