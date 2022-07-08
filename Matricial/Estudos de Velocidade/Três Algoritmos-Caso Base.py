################ Algoritmo com Caso simples usando Consenso/Difusão/Difusão Exata ############################

########################### Importando Bibliotecas #################################

import numpy as np
import matplotlib.pyplot as plt 
import time
import Matrizes_de_Pesos2 as mp

############## Dando os modelos das funções de custo dos cinco agentes ####################

#Dados Tirados do artigo wang.2018 
alp = np.array([0.094,0.078,0.105,0.082,0.074])
bet = np.array([1.22,2.53, 3.41,4.02,3.17])
#Número de agentes
nDG = len(alp) 
#Limites de potência:
Plim=np.array([80,60,40,45,18])


############################## Defindo as matrizes ##################################

# Matriz de Adjacências:
A = np.array([[0,1,0,0,1],
              [1,0,1,0,0],
              [0,1,0,1,0],
              [0,0,1,0,1],
              [1,0,0,1,0]])
#Matriz de Grau:         
D=np.diag(np.sum(A, axis=1))  
#Matriz Laplaciana:                   
L = D - A                                        
I=np.identity(len(A))


epil =np.array([0.14373008, 0.14465435, 0.12670465, 0.17392393, 0.01847044])
### Matriz Metropolis ####

MM,epil2=mp.Mean_Metropolis(A,epil)


#MMi é usado na Difusão Exata: 
MMi=(I+ MM)/2


##################### Inicialização dos parâmetros do Consenso ###################################

print("################### Consenso ################################")

N_max=500
N_max+=1

#Diferença inicial:
diff=10     
#Diferença minima para dizer que convergiu:                         
diff_min=0.01                  

#Potência em kda um dos geradores: 
Pg=np.zeros([N_max,nDG])        
 #Inicialização:         
Pg[0,:]=np.array([35,20,25,30,10])      

#Custo Incremental:
r = np.zeros([N_max,nDG]) 
#Inicialização:                
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

# Mismatch:
Pd=np.zeros([N_max,nDG])                   

################################## Consenso ######################################
print(MM)
tempo1=time.time()
i=0
while(i!=N_max-1 and diff>diff_min):      
    d=np.zeros(nDG)                       # O d é usado como critério de parada
    for j in range(0,len(MM)):
        r[i+1] = MM@r[i] + np.multiply(epil[j],Pd[i])  
        Pg[i+1] = np.divide((r[i+1] - bet),(2*alp)) 
        Pd[i+1] = Pd[i]@MM - (Pg[i+1] - Pg[i])
        d=abs(r[i+1]-r[i])
    if(i==0):
        diff=1
    else:
        diff=max(d)
    i+=1
    
#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
sem_limites=i
salver=r
Pg=Pg[:i,:]
salvePg=Pg
Pd=Pd[:i,:]
salvePd=Pd

############# Separando a lista de potências finais em dois subconjuntos #################

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

################# Reinicializando as variaveis que há necessidade ###############
 
#Diferença inicial: 
diff=10                             

N_max=500
N_max+=1                                  
#Potência em kda um dos geradores: 
Pg=np.zeros([N_max,nDG])       
#Inicialização:            
Pg[0,:]=np.array([35,20,25,30,10])         

#Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização                
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet      

# Mismatch:
Pd=np.zeros([N_max,nDG])                   

################ Algoritmo de Consenso com restrições ##########################

i=0
while(i!=N_max-1 and diff>diff_min):
    for j in range(0,len(MM)):
        r[i+1] = MM@r[i] +np.multiply(epil[j],Pd[i])
        for j in P_n:              #Se j pertencer a P_n,roda normalmente
            Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
        for j in P_u:
            Pg[i+1,j]=Plim[j]       #Se j pertencer a P_u iguala-se ao limite 
        Pd[i+1] = Pd[i]@MM - (Pg[i+1] - Pg[i])
    if(i==0):
        diff=1
    else:
        diff=max(abs(Pd[i]))  #sum(Pd[i])
    i+=1

#Medindo o Tempo de simulação :
tempo2=time.time()

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]    
Pg=Pg[:i,:]
Pd=Pd[:i,:]

print("\n Parou na interação:",i)

#Printando o tempo da simulação:
print("\nTempo Consenso:",tempo2-tempo1)

######################## Exibindo os Dados Finais na tela ###########################

print("\n O custo incremental final será:",round(max(r[-1]),2))

print("\n a potência final de cada gerador será:",Pg[-1])

############################# Plotando os gráficos ##############################

for i in range(0,nDG):
    plt.plot(r[:,i],label=i+1)
plt.legend()
plt.title("Custo Incremental Final")
plt.xlabel("Interação")
plt.ylabel("Custo Incremental")
plt.show()

for i in range(0,nDG):
    plt.plot(Pg[:,i],label=i+1)
plt.legend()
plt.title("Potência em cada gerador final")
plt.xlabel("Interação")
plt.ylabel("Potência em cada gerador")
plt.show()

for i in range(0,nDG):
    plt.plot(Pd[:,i],label=i+1)
plt.legend()
plt.title("Power Mismatch Final")
plt.xlabel("Interação")
plt.ylabel("Power Mismatch")
plt.show()

##################### Inicialização dos parâmetros da Difusão ###################################

print("############################# Difusão ########################")

N_max=500
N_max+=1

#Diferença inicial:
diff=10                              

#Episolon:
epil =np.array([0.0257544,  0.04004497, 0.04619938, 0.07913124, 0.02197946])

Pg=np.zeros([N_max,nDG])                   # Potência em kda um dos geradores 
Pg[0,:]=np.array([35,20,25,30,10])       # Inicialização
Pl=sum(Pg[0])

#Custo Incremental:
r = np.zeros([N_max,nDG])
#Inicialização:               
r[0,:]=2*np.multiply(alp,Pg[0,:])+bet    

#Variavel de Difusão:
var=np.zeros([N_max,nDG])

################################## Difusão sem restrições ######################################

#Tempo Inicial da Difusão:
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

############# Separando a lista de potências finais em dois subconjuntos #################

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

############################# Plotando os gráficos ##############################

for i in range(0,nDG):
    plt.plot(r[:,i],label=i+1)
plt.legend()
plt.title("Custo Incremental Final Difusão")
plt.xlabel("Interação")
plt.ylabel("Custo Incremental")
plt.show()

for i in range(0,nDG):
    plt.plot(Pg[:,i],label=i+1)
plt.legend()
plt.title("Potência em cada gerador final Difusão")
plt.xlabel("Interação")
plt.ylabel("Potência em cada gerador")
plt.show()


##################### Inicialização dos parâmetros da Difusão Exata  ###################################

print("########################### Difusão Exata ########################")

#Número máximo de interações:
N_max=500
N_max+=1

#Diferença inicial:
diff=10                              

# Novo episolon p o método Nugget:
'''
Divide-se o episolon encontrado na Difusão pelo Autovetor de Perron
No caso de matrizes duplamente  estocasticas, o Autovertor de Perron é
1/(N° de Agentes) p tds os seus elementos.

P/outros tipos de matrizes de pesos,consulte o artigo 2018_Part1

'''

epil=np.array([0.04395529, 0.06220131, 0.06972939, 0.04806724, 0.05110734])
MM,epil2=mp.Mean_Metropolis(A,epil)
 
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

################################## Difusão Exata sem Restrições  ######################################

#Medindo o tempo da Difusão Exata 
quero=list()
tb=list()
tempo5=time.time()
i=0
while(i!=N_max-1 and diff>diff_min):     
    d=np.zeros(nDG)
    var[i+1]=r[i]+epil2*(Pl-sum(Pg[i]))
    var1[i+1]=var[i+1] + r[i] - var[i]
    r[i+1] = MMi@var1[i+1]
    Pg[i+1] = np.divide((r[i+1] - bet),(2*alp)) 
    d=abs(r[i+1]-r[i])
    quero.append(d)
    tb.append(Pg[i+1])
    if(i==0):
        diff=1
    else:
        diff=max(d) 
    i+=1

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  

Pg=Pg[:i,:]

print("Custo Incrementral sem restrições",r[-1])
print("Potência em cada gerador sem restrições",Pg[-1])


############# Separando a lista de potências finais em dois subconjuntos #################

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
    
print("\n Parou na interação:",i)

tempo6=time.time()
print("Tempo Método Difusão Exata:",tempo6-tempo5)

#Vai cortar a matriz até a parte útil,se parar por diferença:
r=r[:i,:]  
Pg=Pg[:i,:]

########################### Exibindo os Dados Finais na tela ###########################

print("\n A potência final de cada gerador é:",Pg[-1])
print("\n O custo incremental final será:",round(max(r[-1]),2))

############################# Plotando os gráficos ##############################

for i in range(0,5):
    plt.plot(r[:,i],label=i)
plt.legend()
plt.title("Custo Incremental Difusão Exata ")
plt.xlabel("Interação")
plt.ylabel("Custo Incremental")
plt.show()

for i in range(0,5):
    plt.plot(Pg[:,i],label=i)
plt.legend()
plt.title("Potência em cada gerador Difusão Exata ")
plt.xlabel("Interação")
plt.ylabel("Potência em cada gerador")
plt.show()

''' Obs: Normalmente a Difusão Exata é mais rápida que a Difusão,pois ela aceita
matrizes de peso left-stochastic,que tendem a ser mais rápidas, porém, no código, 
foi usada para os três algoritmos uma matriz doubly-stochastic'''
