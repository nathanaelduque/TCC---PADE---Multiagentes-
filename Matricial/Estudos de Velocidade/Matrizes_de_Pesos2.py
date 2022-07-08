import numpy as np


def Hasting_Rules(A,epil):
    
    MM=np.zeros([len(A),len(A)])
    
    for i in range(0,len(A)):
        for j in range(0,len(A)):
            if (i!=j):
                if (sum(A[i])*epil[i]>sum(A[j])*epil[j]):
                    mi=A[i,j]*epil[j]/((sum(A[i]))*epil[i]) 
                else:
                    mi=A[i,j]*1/(sum(A[j]))         
            else:
                mi=0
            MM[i,j]=mi
    
    for i in range(0,len(A)):
        MM[i,i]=1-sum(MM[i])
 
    return MM,epil
    
def Averaging_Rule(A,epil):
    
    MM=np.zeros([len(A),len(A)])
        
    for i in range(0,len(A)):
        for j in range(0,len(A)):
            if (i!=j):
                MM[i,j]=A[i,j]*1/(sum(A[i]))
            else:
                MM[i,j]=0
    epil2=np.zeros(len(A))
    for i in range(0,len(A)):
        epil2[i]=epil[i]/(sum(A[i]))
    '''Calculo do epsilon já com o vetor de perron'''
    return MM,epil2
            
def Relative_degree_rule(A,epil):

    MM=np.zeros([len(A),len(A)])
    #Num=sum(A[i])+1
    Den=np.zeros(len(A))
    for i in range(0,len(A)):
        for j in range(0,len(A)):
                Den[i]+= A[i,j]*(sum(A[j]))

    
    for i in range(0,len(A)):
        for j in range(0,len(A)):
            if (i==j):
                MM[i,j]=0
            else:
                MM[i,j]=(A[i,j]*(sum(A[j])))/Den[i]
    nk=np.zeros(len(A))
    for i in range(0,len(A)):
        for j in range(0,len(A)):
            nk[i]+=A[i,j]*(sum(A[j]))
    epil2=np.zeros(len(A))
    for i in range(0,len(A)):
        epil2[i]=epil[i]/((sum(A[i]))*nk[i])
    return MM,epil2

def Mean_Metropolis(A,epil):
    #Matriz de Grau:
    D=np.diag(np.sum(A, axis=1))   
    
    #Matriz Laplaciana:
    L = D - A  
    
    #Matriz Identidade:
    I=np.identity(len(A))

    MM=np.zeros([len(A),len(A)])
    for i in range (0,len(A)):
        for j in range(0,len(A)):
            if(i!=j):
                 MM[i,j] = 2./(D[i,i] + D[j,j] + 1)
    MM=np.multiply(A,MM)
    for i in range(0,len(A)):
        MM[i,i] = 1 - sum(MM[i,:])
    
    for i in range (0,len(A[0])):
        epil2=epil/(len(A[0]))
    return MM,epil2