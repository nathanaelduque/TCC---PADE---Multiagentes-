import numpy as np
import matplotlib.pyplot as plt
import time

Carga=[0,1]
Ren=[2]
Desp=[3]
Bat=[4]


pmaxess = 40
alp_ess = 2
beta = 8

'''
#Carga Baixa:
soc=0.2
P_ren=np.array([0,0,10,0,0])
Carga_lim=[18.6,30] 
w=[-36.33,-44.46,0,0,0 ] 
u=[w[0]/Carga_lim[0],w[1]/Carga_lim[1],0,0,0]
epil=np.array([0.09620941, 0.09279018, 0.09277552, 0.09121696, 0.07829946])
'''

'''
#Carga Média:
soc=0.4
P_ren=np.array([0,0,8.5,0,0])
Carga_lim=[31.34,32.15]  
w=[-36.33,-44.46,0,0,0 ] 
u=[w[0]/Carga_lim[0],w[1]/Carga_lim[1],0,0,0]
epil= np.array([0.09729889, 0.09739181, 0.07982797, 0.09873122, 0.08240919])
'''

   
#Carga Alta:
soc=0.1
P_ren=np.array([0,0,13.15,0,0])
Carga_lim=[30,42.9]
w=[-200.25059791, -900.44001645]
u=[w[0]/30,w[1]/44.9,0,0,0]
epil = np.array([0.09253438, 0.09307257, 0.08087597, 0.09236009, 0.09631662])


bet_ess = alp_ess*pmaxess*(1-soc) + beta
alp = np.array([0,0,0,0.18,2]) 
bet = np.array([1,1,1,97,bet_ess])
nDG=2 

nG = len(alp)

A = np.array([[0,1,0,0,1],
              [1,0,1,0,0],
              [0,1,0,1,0],
              [0,0,1,0,1],
              [1,0,0,1,0]])

D=np.diag(np.sum(A, axis=1))   


L = D - A  

I=np.identity(len(A))

MM=np.zeros([nG,nG])
for i in range (0,nG):
    for j in range(0,nG):
        if(i!=j):
             MM[i,j] = 2./(D[i,i] + D[j,j] + 1)
MM=np.multiply(A,MM)
for i in range(0,nG):
    MM[i,i] = 1 - sum(MM[i,:])

N_max=15000
N_max+=1 
  
#Parâmetro de Parada:
diff=10                           # Diferença inicial
diff_min=0.0001                   # Diferença mínima de convergência


n_algorit=0
flag=np.zeros(nG)

Plim_inf = np.array([0,0,0,-50,-(soc*pmaxess)])
Plim_sup = np.array([0,0,0,0,(1-soc)*pmaxess])

#Agentes que ultrapassaram a Potência Máxima:
P_u_max=[]    

#Agentes que ultrapassaram a Potência Mínima:
P_u_min=[]

#Agentes que não ultrapassaram os limites de potência :
P_n=[]

############################ Algoritmo de Difusão sem Restrições ##################################
tempo1=time.time()
while(sum(flag)!=0 or n_algorit==0):
    #Inicializando as Potências dos Agente:
            
    #Número Máximo de Iterações:
    N_max=15000
    N_max+=1 
    Pg=np.zeros([N_max,nG])
    
    #Custo Incremental:
    r = np.zeros([N_max,nG]) 
    
    #Inicializando o Custo Incremental dos Agente:
        
    #Agente Renovável:   
    for i in Ren:
        r[0,i]=0
        
    #Agente Carga:
    for i in Carga:
        r[0,i]=w[i]
        
    #Agente Despachável:
    for i in Desp:
        r[0,i]=bet[i]
    
    #Agente Bateria:
    for i in Bat:
        r[0,i]=bet[i]
    #Inicializando o Power Mismatch:
    Pd=np.zeros([N_max,nG])
    Pd[0]=sum(P_ren)/nG

    #Flag para rodar o while
    flag=np.zeros(nG)
    #Critério de Parada:
    diff=10  
    i=0   
    #Flag de qual tipo de algortimo se deve rodar:(Explicado melhor logo abaixo)
    flag_sem_limites = 1
    flag_limite_superior = 0
        #Consenso em si:
    while(i!=N_max-1 and diff>diff_min):     
        d=np.zeros(nG)
        for j in range(0,len(MM)):  
            r[i+1,j] = MM[j,:]@r[i,:] + epil[j]*Pd[i,j]
            '''
            Quando não há problemas nos limites dos agentes despachavéis, 
            roda-se esse caso
            '''
            if flag_sem_limites ==1: 
                if j in Ren:
                    Pg[i+1,j]=0
                if j in Carga:
                    if(abs(Pg[i,j])>=abs(Carga_lim[j])):
                        Pg[i+1,j]=Carga_lim[j]
                    else:
                        Pg[i+1,j] = -(r[i+1,j]-w[j])/(u[j])
                if j in Bat:
                    if j in P_n or n_algorit==0:
                        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j])
                    elif j in P_u_max:
                        Pg[i+1,j]=Plim_sup[j]
                    elif j in P_u_min:
                        Pg[i+1,j]=Plim_inf[j]
                if j in Desp:
                    if j in P_n or n_algorit==0:
                        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
                    elif j in P_u_max:
                        Pg[i+1,j]=Plim_sup[j]
                    elif j in P_u_min:
                        Pg[i+1,j]=Plim_inf[j]
    
                        
                '''
                Logica implementada logo abaixo desse comentário:
                    
                    
                Possivel Problema: O número agentes despachaveis que rodaram 
                acionaram sua flag é muito grande, sendo todos postos na geração 
                máxima, tem-se que a soma do limite superior de tds eles é maior
                que a carga. 
                
                Solução irá ser realizado um consenso sem restrições entre esses 
                agentes que ultrapassaram o limite máximo, mantendo os que estão
                no limite mínimo em 0. No fim, o consenso irá resolver o despacho
                econômico.
                '''  
            elif flag_limite_superior == 1:
                if j in Ren:
                    Pg[i+1,j]=0
                if j in Carga:
                    if(abs(Pg[i,j])>=abs(Carga_lim[j])):
                        Pg[i+1,j]=Carga_lim[j]
                    else:
                        Pg[i+1,j] = -(r[i+1,j]-w[j])/(u[j])
                if j in Bat:
                    if j in P_n or n_algorit==0:
                        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j])
                    elif j in P_u_max:
                        Pg[i+1,j]=(r[i+1,j] - bet[j])/(2*alp[j])
                    elif j in P_u_min:
                        Pg[i+1,j]=Plim_inf[j]
                if j in Desp:
                    if j in P_n or n_algorit==0:
                        Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
                    elif j in P_u_max:
                        Pg[i+1,j]= (r[i+1,j] - bet[j])/(2*alp[j]) 
                    elif j in P_u_min:
                        Pg[i+1,j]=Plim_inf[j]
                    
            Pd[i+1,j]=Pd[i,:]@MM[j,:] - (Pg[i+1,j] - Pg[i,j])
        d=abs(r[i+1]-r[i])
        if(i==0):
            diff=1
        else:
            diff=max(d) 
        i+=1
    #Corte do i:
    r=r[:i,:]  
    Pg=Pg[:i,:]
    inter=i
    print("Pg:",Pg[-1])
    #Limites de Potência
    for i in range(0,nG):
        if(Pg[-1,i]>=Plim_sup[i]):
            if i in Desp:
                if n_algorit==0:
                    P_u_max.append(i)
                    flag[j]=1
                else:
                    if i in P_n:
                        P_n.remove(i)
                        P_u_max.append(i)
                        flag[i]=1
                    elif i in P_u_min:
                        P_u_min.remove(i)
                        P_u_max.append(i)
                        flag[i]=1
            if i in Bat:
                if n_algorit==0:
                    P_u_max.append(i)
                    flag[i]=1
                else:
                    if i in P_n:
                        P_n.remove(i)
                        P_u_max.append(i)
                        flag[i]=1
                    elif i in P_u_min:
                        P_u_min.remove(i)
                        P_u_max.append(i)
                        flag[i]=1
        elif(Pg[-1,i]<=Plim_inf[i]):
            if i in Desp:
                if n_algorit==0:
                    P_u_min.append(i)
                    flag[i]=1
                else:
                    if i in P_n:
                        P_n.remove(i)
                        P_u_min.append(i)
                        flag[i]=1
                    elif i in P_u_max:
                        P_u_max.remove(i)
                        P_u_min.append(i)
                        flag[i]=1
            if i in Bat:
                if n_algorit==0:
                    P_u_min.append(i)
                    flag[i]=1
                else:
                    if i in P_n:
                        P_n.remove(i)
                        P_u_min.append(i)
                        flag[i]=1
                    elif i in P_u_max:
                        P_u_max.remove(i)
                        P_u_min.append(i)
                        flag[i]=1
        else:
            if i in P_n:
                pass #Faz nada
            elif i in P_u_max:
                P_u_max.remove(i)    
                P_n.append(i)
            elif i in P_u_min:
                P_u_min.remove(i)
                P_n.append(i)
            else:
                P_n.append(i)  # Se n_algorit==0 , cai nessa condicional
# Vai pegar a soma das potências dos agentes despacháveis 
    P_sup=0
    for  a in P_u_max:
        P_sup += Plim_sup[a]
#Vai pegar a soma dos complementares da lista P_u_min e verificar se seus 
#limites máximos realmente irão obedecer a restrição de potência.
    P_inf=0
    for a in P_u_min:
        P_inf += Plim_sup[a]
    if P_sup > sum(Carga_lim):
        flag_sem_limites=0
        flag_limite_superior =1
    n_algorit+=1
    print("flag:",flag)
tempo2=time.time()
print("\nTempo Consenso com restrição:",tempo2-tempo1)    
print("\n Parou na interação:",inter) 
#Colocar isso dentro do algoritmo         
r=r[:inter,:]  #Vai cortar a matriz até a parte útil,se parar por diferença
Pg=Pg[:inter,:]
soc = (soc*40 + Pg[-1, 4])/40


######################## Exibindo os Dados sem restrições na tela ###########################

print("\n A potência de cada agente quando há restrições:",Pg[-1])
print("\n O custo incremental quando não há restrições será:",round(max(r[-1]),2))
print("\n ###################### ")

############################# Plotando os gráficos ##############################

for i in range(0,nG):
    plt.plot(r[:,i],label=i+1)
plt.legend()
plt.title("Custo Incremental por Interação - Algoritmo de Consenso")
plt.xlabel("Interação")
plt.ylabel("Custo incrementação [₩]")
plt.show()

for i in range(0,nG):
    plt.plot((Pg[:,i])*-1,label=i+1)
plt.legend()
plt.title("Potência por Interação - Algoritmo de Consenso")
plt.xlabel("Interação")
plt.ylabel("Potência")
plt.show()

