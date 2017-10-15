import os,sys
import csv
from itertools import *

cntN = []

def readConfig():                                            # read config.csv file
	f = open('config.csv',"rb")
	'''if(!f.open()):
		print 'Error opening config File'
	'''
	reader = csv.reader(f)
	for row in reader:
			
		if row[0] == "input":
			iFile = row[1]
		elif row[0] == "output":
			oFile = row[1]
		elif row[0] == "support":
			mnsup = row[1]
		elif row[0] == "confidence":
			confd = row[1]
		elif row[0] == "flag":
			flag = row[1]


	f.close()		
	return iFile, oFile, mnsup, confd, flag


def readInp(inpFile):                                         #read input.csv file
	transaction = list()
	f = open(inpFile,"rb")
	'''if(!f):
		print 'Error opening input  File'
	'''
	reader = csv.reader(f)
	for row in reader:
		#print 'row is',row
		transaction.append(row)

	f.close()
	return transaction

'''************************************************************************************************************************************'''








'''***********************************************************************************************************************************'''



def create(transactions):                 				#generate single unique elements in transactions
	c1 = []
	for transaction in transactions:
		for item in transaction:
			if not [item] in c1:
				c1.append([item])
	c1.sort()
	return map(frozenset, c1)
	



def scanData(data,candidates, minsup):
	subsetcnt = {}
	#print 'ScanData'
	'''for i in candidates:
		print i
	'''
	'''for i in data:
		print i'''

	cntN.append(len(candidates))	
	for tid in data:
		for can in candidates:
			if can.issubset(tid):
				subsetcnt.setdefault(can,0)
				subsetcnt[can] = subsetcnt[can] + 1
		
	cnt_items = float(len(data))
	retlist = []							#contains groups of candidates satisfying criteria of support
	supdata = {}  							#support data
	i = 1
	for key in subsetcnt:
		supp = subsetcnt[key] / cnt_items
		#print subsetcnt[key], cnt_items, key
		#print key, supp, minsup
		if float(supp) >= float(minsup):
			
			retlist.insert(i,key)
			i = i + 1
		supdata[key] = supp
	
	'''print 'scanData'	
	for k in retlist:
		print k, supdata[k]
	'''
	return retlist, supdata	



def aprioriGen( freqsets , k ):
	retlist = []
	lenlk = len(freqsets)
	for i in range(lenlk):
		for j in range( i+1 , lenlk ):
			l1 = list( freqsets[i] )[ :k-2 ]
			l2 = list( freqsets[j] )[ :k-2 ]
			l1.sort()
			l2.sort()
			
			if l1 == l2:
				retlist.append(freqsets[i] | freqsets[j] )
	return retlist			





def apriori( uniqElements, transData,  minsup, conf):

	list1, supdata = scanData( transData , uniqElements , minsup)
	L = [ list1 ]                                       # list1 -> original list containing single elements
					            # supdata -> support data values corres. to elements in list1
	k = 2  						    # k = 2 for making subsets of size 2
	rules = []

	while ( len( L[ k-2 ] ) > 0 ):
		#print 'k: ',k
		ck = aprioriGen( L[ k-2 ], k )
		
		Lk,Supk = scanData( transData, ck, minsup)  # get list Lk for subsets of size k. Supk crres. to support for them.
	
		
		supdata.update(Supk)
		L.append(Lk)
		k = k + 1

	
	return L,supdata	



'''*************************************************************************************************************************************'''



def powerset( a ):
	xs = list(a)
	return chain.from_iterable(combinations(xs,n) for n in range( len(xs) + 1))










def checker(L1, L2):
	flg1 = 1
	flg2 = 1

	for i in L1:
		if i in L2:
			flg1 = 0
			break
	
	for i in L2:
		if i in L1:
			flg2 = 0
			break

	
	if flg1 == 1 and flg2 == 1:
		return 1
	else:
		return 0



'''*************************************************************************************************************************************'''








if __name__ == "__main__":
	
	inpFile,outFile,minsup,conf,flg = readConfig()
	
	transactions = readInp(inpFile)	
	
	#print transactions

	uniqElements = create(transactions)

	#print uniqElements
	
	transData = map(set,transactions)
	
	#print transData
	

	L,Sd = apriori( uniqElements, transData, minsup, conf )




	NL = []	    #list of frequent itemsets

	
	for i in  L:
		for j in i:
			NL.append( list(j) )
	



	'''for i in NL:
		print i'''
	

	cntR = 0

	assR = []             #association rules


	for i in NL:

		a = list(powerset(i))
		'''print 'i is ',i
		print 'a is ',a'''
		for j in a:
			if len(j) == 0 or list(j) == i:    #empty subset or whole set
				#print 'j is ',j
				continue
			else:
				k1 = list(set(j))
				k2 = list(set(i) - set(j))
				k3 = list(set(i))
				m = Sd[frozenset(k3)]/Sd[frozenset(k1)]
				
				#print k1,k2,m
				
				if m >= float(conf):
					q = []
					for g in k1:
						q.append(g)
					q.append('=>')

					for g in k2:
						q.append(g)
					
					assR.append(q)
					cntR = cntR + 1





				


	#print 'cnt is: ',cntR
	#print len(assR)


	f = open(outFile,"w")
	f.write( str(len(NL)) )
	f.write("\n")
	for i in NL:

		cnt = 0
		s = ','.join(i)	
		#print s		
		f.write(s)
		f.write("\n");
				
	if int(flg) == 0:
	   	f.close()
	else:
		f.write( str( len(assR) ) )
		f.write("\n")

		for i in assR:
			s = ','.join(i)
			#print s	
			f.write(s)
			f.write("\n");

		f.close()
		   



		

















