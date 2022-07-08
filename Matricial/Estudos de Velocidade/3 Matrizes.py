# Comparação entre 3 matrizes de pesos left-stochastic's e a matriz
# de pesos colocada no caso base
'''
Obs: Além de ter implementado a matriz left-stochastic,também foi 
rodado p kda um, um AG para obter o episolon ótimo de cada uma das
matrizes de pesos 
'''

#Importando Bibliotecas:
    
import numpy as np
import matplotlib.pyplot as plt 
import time

#Dados Comuns a Todas as Matrizes:
    
alp = np.array([0.094,0.078,0.105,0.082,0.074])
bet = np.array([1.22,2.53, 3.41,4.02,3.17])
#Número de agentes
nDG = len(alp) 
#Limites de potência:
Plim=np.array([80,60,40,45,18])

##################################### Matriz 01 ############################################
#Averaging Rule:
'''
Falta terminar pro caso com restrições a Averaging Rule

''' 

#Matriz de Pesos:
MM = np.array([[ 1/3 , 1/3 ,  0 ,  0 ,  1/3 ],
               [ 1/4 , 1/4 , 1/4 , 0 ,  1/4 ],
               [  0  , 1/3 , 1/3 , 1/3 , 0 ],
               [  0  ,  0  , 1/3 , 1/3 , 1/3],
               [  1/4, 1/4 ,  0 ,  1/4 , 1/4 ]])
#Matriz de Identidades:
I=np.identity(len(MM))

#MMi é usado na Difusão Exata: 
MMi=(I+ MM)/2
print("\n ########################### Averaging Rule ########################")
print("\n ############################# Difusão ########################")

N_max=500
N_max+=1

#Diferença inicial:
diff=10      
#Diferença minima para dizer que convergiu:                         
diff_min=0.00001                           

#Episolon:
epil =np.array([0.0379594,0.02703334,0.00500433,0.00597867,0.00108661])

Pg=np.zeros([N_max,nDG])                   # Potência em kda um dos geradores 
Pg[0,:]=np.array([35,20,25,30,10])       # Inicialização
Pl=sum(Pg[0])

#Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:               
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variavel de Difusão:
var=np.zeros([N_max,nDG])

# Difusão sem restrições:
tempo3=time.time()
i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil*(Pl-sum(Pg[i]))
    r[i+1] = MM@var[i+1] 
    Pg[i+1] = np.divide((r[i+1] - bet),(2*alp)) 
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]


#Geradores que ultrapassaram a Potência Máxima:
P_u=[]    

#Geradores que não ultrapassaram a Potência Máxima :
P_n=[]    

for i in range(0,nDG):
    if(Pg[-1,i]>Plim[i]):
        print("\n Potência ultrapassada no gerador:",i+1)
        P_u.append(i)
    else:
        P_n.append(i)

#############Reinicializando as variaveis que necessitam ser reinicializadas ##########

N_max=500
N_max+=1

# Diferença inicial:
diff=10                              

#Episolon:
epil =np.array([0.09566478,0.01236559,0.00350501,0.01521083,0.04761036])

# Potência em kda um dos geradores:
Pg=np.zeros([N_max,nDG])            
# Inicialização:       
Pg[0,:]=np.array([35,20,25,30,10])       
Pl=sum(Pg[0])

# Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:              
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variável de Difusão:
var=np.zeros([N_max,nDG])

################################## Difusão com restrições ######################################

i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil*(Pl-sum(Pg[i]))
    r[i+1] = MM@var[i+1] #Se der errado tire o +1
    for j in P_n:                   #Se j pertencer a P_n,roda normalmente
        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
    for j in P_u:
            Pg[i+1,j]=Plim[j]       #Se j pertencer a P_u iguala-se ao limite
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1
tempo4=time.time()
print("\n Parou na interação:",i)

print("\n Tempo Difusão:",tempo4-tempo3)

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

######################## Exibindo os Dados Finais na tela ###########################

print("\n O custo incremental final será:",round(max(r[-1]),2))

print("\n a potência final de cada gerador será:",Pg[-1])




# Inicialização dos parâmetros da Difusão Exata:  

print("\n ########################### Difusão Exata ########################")

#Número máximo de interações:
N_max=500
N_max+=1

#Diferença inicial:
diff=10                          

# Novo episolon p o método Nugget:
    
epil =np.array([0.0379594,0.02703334,0.00500433,0.00597867,0.00108661]) #episolon sem restrições
n=np.array([3,4,3,3,4]) #número de vizinhos em kda um dos Agentes
epil2=np.zeros(len(epil))

for i in range(0,len(epil)):
    epil2[i]=epil[i]/n[i]
# Potência em kda um dos geradores :    
Pg=np.zeros([N_max,nDG])    
#Inicialização:              
Pg[0,:]=np.array([35,20,25,30,10])      
Pl=sum(Pg[0])

#Custo Incremental:
r = np.zeros([N_max,nDG])    
#Inicialização:            
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variavel de Difusão
var=np.zeros([N_max,nDG])
var[0]=r[0]

#Variavel de correção da difusão,para ela corrigir p o valor ótimo exato:
var1=np.zeros([N_max,nDG])
var1[0]=r[0] #Depois Teste sem essa inicialização

# Difusão Exata sem Restrições:

#Medindo o tempo da Difusão Exata :
tempo5=time.time()
i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil2*(Pl-sum(Pg[i]))
    var1[i+1]=var[i+1] + r[i] - var[i]
    r[i+1] = MMi@var1[i+1]
    Pg[i+1] = np.divide((r[i+1] - bet),(2*alp)) 
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

#Separando a lista de potências finais em dois subconjuntos:

#Geradores que ultrapassaram a Potência Máxima:
P_u=[]    

#Geradores que não ultrapassaram a Potência Máxima :
P_n=[]    

for i in range(0,nDG):
    if(Pg[-1,i]>Plim[i]):
        print("\n Potência ultrapassada no gerador:",i+1)
        P_u.append(i)
    else:
        P_n.append(i)

#Reinicializando as variaveis que necessitam ser reinicializadas:

N_max=500
N_max+=1

# Diferença inicial:
diff=10 

#Episolon da Difusão Exata:
#Episolon:
epil =np.array([0.09566478,0.01236559,0.00350501,0.01521083,0.04761036])
n=np.array([3,4,3,3,4]) #número de vizinhos em kda um dos Agentes
epil2=np.zeros(len(epil))

for i in range(0,len(epil)):
    epil2[i]=epil[i]/n[i]

# Potência em kda um dos geradores:
Pg=np.zeros([N_max,nDG])            
# Inicialização:       
Pg[0,:]=np.array([35,20,25,30,10])       
Pl=sum(Pg[0])

# Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:              
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variável de Difusão:
var=np.zeros([N_max,nDG])
var[0]=r[0]

#Variavel de correção da difusão,para ela corrigir p o valor ótimo exato:
var1=np.zeros([N_max,nDG])
#var1[0]=r[0] #Depois Teste sem essa inicialização

########################### Difusão Exata com restrições ###############################

i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil2*(Pl-sum(Pg[i]))
    var1[i+1]=var[i+1] + r[i] - var[i]
    r[i+1] = MMi@var1[i+1]
    for j in P_n:                   #Se j pertencer a P_n,roda normalmente
        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
    for j in P_u:
        Pg[i+1,j]=Plim[j]       #Se j pertencer a P_u iguala-se ao limite
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1
tempo6=time.time()  
 
print("\n Parou na interação:",i)

print("Tempo Método Difusão Exata:",tempo6-tempo5) 

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

########################### Exibindo os Dados Finais na tela ###########################

print("\n A potência final de cada gerador é:",Pg[-1])
print("\n O custo incremental final será:",round(max(r[-1]),2))


###################################### Matriz 02 ##########################################
#Relative-degree Rule:
    
MM= np.array([[ 3/11,  4/11,  0,      0,    4/11],
              [ 3/14,  4/14,  3/14,   0,    4/14],
              [ 0,     4/10,  3/10,   3/10, 0   ],
              [ 0,     0,     3/10,   3/10, 4/10],
              [ 3/14,  4/14,  0,      3/14, 4/14]])

#Matriz de Identidades:
I=np.identity(len(MM))

#MMi é usado na Difusão Exata: 
MMi=(I+ MM)/2
print("\n ###################### Relative-degree Rule #######################")

print("\n ############################# Difusão ########################")

N_max=500
N_max+=1

#Diferença inicial:
diff=10                             
#Episolon:
epil =np.array([0.07336773,0.03171697,0.00379566,0.01028573,0.01386893])

Pg=np.zeros([N_max,nDG])                   # Potência em kda um dos geradores 
Pg[0,:]=np.array([35,20,25,30,10])       # Inicialização
Pl=sum(Pg[0])

#Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:               
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variavel de Difusão:
var=np.zeros([N_max,nDG])

# Difusão sem restrições:
tempo3=time.time()
i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil*(Pl-sum(Pg[i]))
    r[i+1] = MM@var[i+1] #Se der errado tire o +1
    Pg[i+1] = np.divide((r[i+1] - bet),(2*alp)) 
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]


# Separando a lista de potências finais em dois subconjuntos:

#Geradores que ultrapassaram a Potência Máxima:
P_u=[]    

#Geradores que não ultrapassaram a Potência Máxima :
P_n=[]    

for i in range(0,nDG):
    if(Pg[-1,i]>Plim[i]):
        print("\n Potência ultrapassada no gerador:",i+1)
        P_u.append(i)
    else:
        P_n.append(i)

#############Reinicializando as variaveis que necessitam ser reinicializadas ##########

N_max=500
N_max+=1

# Diferença inicial:
diff=10                              

#Episolon:
epil =np.array([0.08158893,0.05793766,0.0017157,0.01420214,0.05050288])

# Potência em kda um dos geradores:
Pg=np.zeros([N_max,nDG])            
# Inicialização:       
Pg[0,:]=np.array([35,20,25,30,10])       
Pl=sum(Pg[0])

# Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:              
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variável de Difusão:
var=np.zeros([N_max,nDG])

################################## Difusão com restrições ######################################

i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil*(Pl-sum(Pg[i]))
    r[i+1] = MM@var[i+1] 
    for j in P_n:               
        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
    for j in P_u:
            Pg[i+1,j]=Plim[j]       #Se j pertencer a P_u iguala-se ao limite
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1
tempo4=time.time()

print("\n Parou na interação:",i)

print("\n Tempo Difusão:",tempo4-tempo3)

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

######################## Exibindo os Dados Finais na tela ###########################

print("\n O custo incremental final será:",round(max(r[-1]),2))

print("\n a potência final de cada gerador será:",Pg[-1])

print("\n ########################### Difusão Exata ########################")

#Número máximo de interações:
N_max=500
N_max+=1

#Diferença inicial:
diff=10                          

# Novo episolon p o método Nugget:

epil2=np.array([0.06433633,0.07393551,0.03850329,0.05743911,0.07056379])
  
# Potência em kda um dos geradores :    
Pg=np.zeros([N_max,nDG])    
#Inicialização:              
Pg[0,:]=np.array([35,20,25,30,10])      
Pl=sum(Pg[0])

#Custo Incremental:
r = np.zeros([N_max,nDG])    
#Inicialização:            
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variavel de Difusão
var=np.zeros([N_max,nDG])
var[0]=r[0]

#Variavel de correção da difusão,para ela corrigir p o valor ótimo exato:
var1=np.zeros([N_max,nDG])
var1[0]=r[0] #Depois Teste sem essa inicialização

# Difusão Exata sem Restrições:

#Medindo o tempo da Difusão Exata 
tempo5=time.time()
i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil*(Pl-sum(Pg[i]))
    var1[i+1]=var[i+1] + r[i] - var[i]
    r[i+1] = MMi@var1[i+1]
    Pg[i+1] = np.divide((r[i+1] - bet),(2*alp)) 
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

#Geradores que ultrapassaram a Potência Máxima:
P_u=[]    

#Geradores que não ultrapassaram a Potência Máxima :
P_n=[]    

for i in range(0,nDG):
    if(Pg[-1,i]>Plim[i]):
        print("\n Potência ultrapassada no gerador:",i+1)
        P_u.append(i)
    else:
        P_n.append(i)

#############Reinicializando as variaveis que necessitam ser reinicializadas ##########

N_max=500
N_max+=1

# Diferença inicial:
diff=10 

# Potência em kda um dos geradores:
Pg=np.zeros([N_max,nDG])            
# Inicialização:       
Pg[0,:]=np.array([35,20,25,30,10])       
Pl=sum(Pg[0])

# Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:              
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variável de Difusão:
var=np.zeros([N_max,nDG])
var[0]=r[0]

#Variavel de correção da difusão,para ela corrigir p o valor ótimo exato:
var1=np.zeros([N_max,nDG])
#var1[0]=r[0] #Depois Teste sem essa inicialização

epil2=np.array([0.09665329,0.08861908,0.02573071,0.0384279,0.08674599])

########################### Difusão Exata com restrições ###############################

i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil2*(Pl-sum(Pg[i]))
    var1[i+1]=var[i+1] + r[i] - var[i]
    r[i+1] = MMi@var1[i+1]
    for j in P_n:                   #Se j pertencer a P_n,roda normalmente
        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
    for j in P_u:
        Pg[i+1,j]=Plim[j]       #Se j pertencer a P_u iguala-se ao limite
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1
tempo6=time.time()   
print("\n Parou na interação:",i)

print("\n Tempo Método Difusão Exata:",tempo6-tempo5)

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

########################### Exibindo os Dados Finais na tela ###########################

print("\n A potência final de cada gerador é:",Pg[-1])
print("\n O custo incremental final será:",round(max(r[-1]),2))

################################## Matriz 03 ###################################
#Hastings rule:
    
#Vai ser usado o Mi da difusão do de cima,caso sem restrições para montar a matriz 

MM= np.array([[0.33333333, 0.33333333, 0.,         0.,         0.33333333],
              [0.14667795, 0.21453526, 0.30545346, 0.,         0.33333333],
              [0.,         0.33333333, 0.23370401, 0.43296266, 0.        ],
              [0.,         0.,         0.5,        0.16666667, 0.33333333],
              [0.12533462, 0.28482951, 0.,         0.22601212, 0.36382375]])

#Matriz de Identidades:
I=np.identity(len(MM))

#MMi é usado na Difusão Exata: 
MMi=(I+ MM)/2

print("\n ########################### Hastings rule ########################")
print("\n ############################# Difusão ########################")

N_max=500
N_max+=1

#Diferença inicial:
diff=10                           

#Episolon:
epil =np.array([0.01965141,0.04465886,0.04092361,0.03543679,0.05226385])

Pg=np.zeros([N_max,nDG])                   # Potência em kda um dos geradores 
Pg[0,:]=np.array([35,20,25,30,10])       # Inicialização
Pl=sum(Pg[0])

#Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:               
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variavel de Difusão:
var=np.zeros([N_max,nDG])

# Difusão sem restrições:
tempo3=time.time()
i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil*(Pl-sum(Pg[i]))
    r[i+1] = MM@var[i+1] 
    Pg[i+1] = np.divide((r[i+1] - bet),(2*alp)) 
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

#Separando a lista de potências finais em dois subconjuntos:

#Geradores que ultrapassaram a Potência Máxima:
P_u=[]    

#Geradores que não ultrapassaram a Potência Máxima :
P_n=[]    

for i in range(0,nDG):
    if(Pg[-1,i]>Plim[i]):
        print("\n Potência ultrapassada no gerador:",i+1)
        P_u.append(i)
    else:
        P_n.append(i)

#############Reinicializando as variaveis que necessitam ser reinicializadas ##########

N_max=500
N_max+=1

# Diferença inicial:
diff=10                              

#Episolon:
epil =np.array([0.01965141,0.04465886,0.04092361,0.03543679,0.05226385])

# Potência em kda um dos geradores:
Pg=np.zeros([N_max,nDG])            
# Inicialização:       
Pg[0,:]=np.array([35,20,25,30,10])       
Pl=sum(Pg[0])

# Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:              
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variável de Difusão:
var=np.zeros([N_max,nDG])

################################## Difusão com restrições ######################################

i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil*(Pl-sum(Pg[i]))
    r[i+1] = MM@var[i+1] #Se der errado tire o +1
    for j in P_n:                   #Se j pertencer a P_n,roda normalmente
        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
    for j in P_u:
            Pg[i+1,j]=Plim[j]       #Se j pertencer a P_u iguala-se ao limite
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1
tempo4=time.time()

print("\n Parou na interação:",i)

print("Tempo Difusão:",tempo4-tempo3)

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

######################## Exibindo os Dados Finais na tela ###########################

print("\n O custo incremental final será:",round(max(r[-1]),2))

print("\n a potência final de cada gerador será:",Pg[-1])



################################ Difusão Exata HR #################################

print("\n ########################### Difusão Exata ########################")

#Número máximo de interações:
N_max=500
N_max+=1

#Diferença inicial:
diff=10                          

# Novo episolon p o método Nugget:

epil =np.array([0.01965141,0.04465886,0.04092361,0.03543679,0.05226385])

for i in range(0,len(epil)):
    epil2[i]=epil[i]/n[i]
    
    
# Potência em kda um dos geradores :    
Pg=np.zeros([N_max,nDG])    
#Inicialização:              
Pg[0,:]=np.array([35,20,25,30,10])      
Pl=sum(Pg[0])

#Custo Incremental:
r = np.zeros([N_max,nDG])    
#Inicialização:            
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variavel de Difusão
var=np.zeros([N_max,nDG])
var[0]=r[0]

#Variavel de correção da difusão,para ela corrigir p o valor ótimo exato:
var1=np.zeros([N_max,nDG])
var1[0]=r[0] #Depois Teste sem essa inicialização

# Difusão Exata sem Restrições:

#Medindo o tempo da Difusão Exata 
tempo5=time.time()
i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil2*(Pl-sum(Pg[i]))
    var1[i+1]=var[i+1] + r[i] - var[i]
    r[i+1] = MMi@var1[i+1]
    Pg[i+1] = np.divide((r[i+1] - bet),(2*alp)) 
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

#Geradores que ultrapassaram a Potência Máxima:
P_u=[]    

#Geradores que não ultrapassaram a Potência Máxima :
P_n=[]    

for i in range(0,nDG):
    if(Pg[-1,i]>Plim[i]):
        print("\n Potência ultrapassada no gerador:",i+1)
        P_u.append(i)
    else:
        P_n.append(i)

#############Reinicializando as variaveis que necessitam ser reinicializadas ##########

N_max=5000
N_max+=1

# Diferença inicial:
diff=10 

# Potência em kda um dos geradores:
Pg=np.zeros([N_max,nDG])            
# Inicialização:       
Pg[0,:]=np.array([35,20,25,30,10])       
Pl=sum(Pg[0])

# Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:              
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variável de Difusão:
var=np.zeros([N_max,nDG])
var[0]=r[0]

#Variavel de correção da difusão,para ela corrigir p o valor ótimo exato:
var1=np.zeros([N_max,nDG])
#var1[0]=r[0] #Depois Teste sem essa inicialização

########################### Difusão Exata com restrições ###############################

i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil2*(Pl-sum(Pg[i]))
    var1[i+1]=var[i+1] + r[i] - var[i]
    r[i+1] = MMi@var1[i+1]
    for j in P_n:                   #Se j pertencer a P_n,roda normalmente
        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
    for j in P_u:
        Pg[i+1,j]=Plim[j]       #Se j pertencer a P_u iguala-se ao limite
    d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1
tempo6=time.time()   
print("\n Parou na interação:",i)

print("\n Tempo Método Difusão Exata:",tempo6-tempo5)

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

########################### Exibindo os Dados Finais na tela ###########################

print("\n A potência final de cada gerador é:",Pg[-1])
print("\n O custo incremental final será:",round(max(r[-1]),2))