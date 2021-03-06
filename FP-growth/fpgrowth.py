﻿'''
	fpgrowth算法
	1 对数据进行第一次扫描 得到 每个项的数目
	2 第二次扫描并建立 fp树
	3 对fp树进行分析 得到频繁项集和关联规则
'''

#树节点
class treeNode:
	def __init__(self,nameValue,numOccur,parentNode):
		self.name = nameValue
		self.count = numOccur
		self.nodeLink = None
		self.parent = parentNode
		self.children = {}
	def inc(self,numOccur):
		self.count += numOccur
	def disp(self,ind=1):
		print(' '*ind, self.name, ' ', self.count)
		for child in self.children.values():
			child.disp(ind+1)

#创建树
def createTree(dataSet, minSup=1):
	headerTable = {}
	for trans in dataSet:
		for item in trans:
			headerTable[item] = headerTable.get(item,0) + dataSet[trans]
	
	tmpTable = headerTable.copy()
	for k in tmpTable.keys():
		if headerTable[k] < minSup:
			del(headerTable[k])
	
	freqItemSet = set(headerTable.keys())
	if len(freqItemSet) == 0:
		return None,None
	for k in headerTable:
		headerTable[k] = [headerTable[k], None]
	retTree = treeNode('Null Set', 1, None)
	for tranSet,count in dataSet.items():
		localD = {}
		for item in tranSet:
			if item in freqItemSet:
				localD[item] = headerTable[item][0]
		if len(localD) > 0:
			orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p:p[1], reverse=True)]
			updateTree(orderedItems, retTree, headerTable, count)
	return retTree,headerTable
	
#更新树的结构 
def updateTree(items, inTree, headerTable, count):
	if items[0] in inTree.children:
		inTree.children[items[0]].inc(count)
	else:
		inTree.children[items[0]] = treeNode(items[0],count,inTree)
		if headerTable[items[0]][1] == None:
			headerTable[items[0]][1] = inTree.children[items[0]]
		else:
			updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
	if len(items) > 1:
		updateTree(items[1::],inTree.children[items[0]],headerTable,count)

#更新头部 的nodeLink 		
def updateHeader(nodeToTest,targetNode):
	while (nodeToTest.nodeLink != None):
		nodeToTest = nodeToTest.nodeLink
	nodeToTest.nodeLink = targetNode

#加载数据	
def loadSimpDat():
	simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
			   
	return simpDat

#格式化处理数据	
def createInitSet(dataSet):
	retDict = {}
	for trans in dataSet:
		retDict[frozenset(trans)] = 1
	return retDict
	


def ascendTree(leafNode,prefixPath):
	if leafNode.parent != None:
		prefixPath.append(leafNode.name)
		ascendTree(leafNode.parent,prefixPath)
		
def findPrefixPath(basePat,treeNode):
	condPats = {}
	while treeNode != None:
		prefixPath = []
		ascendTree(treeNode, prefixPath)
		if len(prefixPath) > 1:
			condPats[frozenset(prefixPath[1:])] = treeNode.count
		treeNode = treeNode.nodeLink
	return condPats

#递归查找频繁项集	
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
	bigL = [v[0] for v in sorted(headerTable.items(),key=lambda p:p[0])]
	print('bigL:',bigL)
	for basePat in bigL:
		print('basePat:',basePat)
		newFreqSet = preFix.copy()
		newFreqSet.add(basePat)
		freqItemList.append(newFreqSet)
		condPattBases = findPrefixPath(basePat,headerTable[basePat][1])
		print('condPattBases:',condPattBases)
		myCondTree,myHead = createTree(condPattBases,minSup)
		if myHead != None:
			mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
			
#从文件中加载数据
def loadDataSet(fileName):
	fopen = open(fileName)
	dataArr = []
	for line in fopen.readlines():
		dataArr.append(line.strip().split(','))
	return dataArr

#构建fp树，最小支持度默认为3
def fp(fileName='testSet.txt',minSupport=3):
	simpDat = loadDataSet(fileName)
	initSet = createInitSet(simpDat)

	myFpTree,myHeaderTable = createTree(initSet,minSupport)
	myFpTree.disp()
	
	freqItems = []
	mineTree(myFpTree, myHeaderTable, minSupport, set([]), freqItems)			
	return myFpTree,freqItems

	





	

	

	
	
