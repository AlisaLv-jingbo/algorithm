#���ֵ��
def zeroMean(dataMat):      
    meanVal=np.mean(dataMat,axis=0)     #�������ֵ��������������ľ�ֵ
    newData=dataMat-meanVal
    return newData,meanVal

#��һ��pca��ȡǰ���n������ֵ
def pca(dataMat,n):
    newData,meanVal=zeroMean(dataMat)
    covMat=np.cov(newData,rowvar=0)    #��Э�������,return ndarray����rowvar��0��һ�д���һ��������Ϊ0��һ�д���һ������
    
    eigVals,eigVects=np.linalg.eig(np.mat(covMat))#������ֵ����������,���������ǰ��зŵģ���һ�д���һ����������
    eigValIndice=np.argsort(eigVals)            #������ֵ��С��������
    n_eigValIndice=eigValIndice[-1:-(n+1):-1]   #����n������ֵ���±�
    n_eigVect=eigVects[:,n_eigValIndice]        #����n������ֵ��Ӧ����������
    lowDDataMat=newData*n_eigVect               #��ά�����ռ������
    reconMat=(lowDDataMat*n_eigVect.T)+meanVal  #�ع�����
    return lowDDataMat,reconMat
	
#��������ٷֱȵ� ���k
def percentage2n(eigVals,percentage):  
    sortArray=np.sort(eigVals)   #����  
    sortArray=sortArray[-1::-1]  #��ת��������  
    arraySum=sum(sortArray)  
    tmpSum=0  
    num=0  
    for i in sortArray:  
        tmpSum+=i  
        num+=1  
        if tmpSum>=arraySum*percentage:  
            return num 	
		
#�ڶ���pca��ȡ�ٷֱȵ�  k������
def pca(dataMat,percentage=0.99):  
    newData,meanVal=zeroMean(dataMat)  
    covMat=np.cov(newData,rowvar=0)    #��Э�������,return ndarray����rowvar��0��һ�д���һ��������Ϊ0��һ�д���һ������  
    eigVals,eigVects=np.linalg.eig(np.mat(covMat))#������ֵ����������,���������ǰ��зŵģ���һ�д���һ����������  
    n=percentage2n(eigVals,percentage)                 #Ҫ�ﵽpercent�ķ���ٷֱȣ���Ҫǰn����������  
    eigValIndice=np.argsort(eigVals)            #������ֵ��С��������  
    n_eigValIndice=eigValIndice[-1:-(n+1):-1]   #����n������ֵ���±�  
    n_eigVect=eigVects[:,n_eigValIndice]        #����n������ֵ��Ӧ����������  
    lowDDataMat=newData*n_eigVect               #��ά�����ռ������  
    reconMat=(lowDDataMat*n_eigVect.T)+meanVal  #�ع�����  
    return lowDDataMat,reconMat
	
