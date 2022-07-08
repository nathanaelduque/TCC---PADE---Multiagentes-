############################ Corte de Carga sem Restrições ################################

''' 
Dados do Problema:
    
   Agente 01: Carga não crítica
   Agente 02: Carga crítica
   Agente 03: Renováveis
   Agente 04: Geração Classica
   
   Todos os Parâmetros dos Agentes Foram retirados do artigo do IEEE  
'''

################################# Importando Bibliotecas ##########################################

import numpy as np
import matplotlib.pyplot as plt
import Matrizes_de_Pesos2 as mp
import time

################################# Modelando os quatros agentes ###########################

''' 
Primeiramente eu implementei a Difusão Clássica,obti o episolon ótimo,depois dividi 
o episolon ótimo de cada agente dividindo pelo Autovetor de Perron

lembrando que:
 
1)No caso de matrizes duplamente  estocasticas, o Autovertor de Perron é
1/(N° de Agentes) p tds os seus elementos.

2)P/outros tipos de matrizes de pesos,consulte o artigo 2018_Part1

3)A Difusão Exata aceita matrizes de peso left-stochastic,que tendem a ser mais
rápidas, porém, no código,foi usada uma matriz doubly-stochastic    
'''

'''
O que antes era feito com umm vetor de identificação,agora é feito através de listas
Isso é necessário p se rodar a Difusão Exata apropriadamente
'''

Carga=[0,1]
Ren=[2]
Desp=[3]
Bat=[4]

#Bateria:
pmaxess = 40

'''
#Carga Baixa:
soc=0.2
P_ren=np.array([0,0,10,0,0])
Carga_lim=[18.6,30] 
w=[-36.33,-44.46,0,0,0 ] 
u=[w[0]/Carga_lim[0],w[1]/Carga_lim[1],0,0,0]  
epil=np.array([0.07652637, 0.03359369, 0.126386,   0.39709159, 0.14086643])  
'''

'''
#Carga Média:
soc = 0.4
P_ren=np.array([0,0,8.5,0,0]) 
Carga_lim=[31.34,32.15] 
w=[-36.33,-44.46,0,0,0 ] 
u=[w[0]/Carga_lim[0],w[1]/Carga_lim[1],0,0,0]
epil=np.array([0.73779529, 0.67929289, 0.7216009 , 0.79982353, 0.65343889])
'''


#Carga Alta:   
soc=0.1
P_ren=np.array([0,0,13.15,0,0])
Carga_lim=[30,42.9]
w=[-200.25059791, -900.44001645]
u=[w[0]/30,w[1]/44.9,0,0,0]
epil=np.array([0.98542669, 0.96636851, 0.94530173, 0.95202156, 0.96353537])




alp_ess = 2
beta = 8
bet_ess = alp_ess*pmaxess*(1-soc) + beta

#Parâmetros da Geração:
alp = np.array([0,0,0,0.18,2]) 
bet = np.array([1,1,1,97,bet_ess])

#Número de agentes despacháveis:
nDG=2 

#Número de Agentes:
nG = len(alp) 

################## Inicialização dos Parâmetros do Consenso sem restrições #############


#Episolon:
   
############################# Carga Baixa #####################################
  
'''
#Episolon ótimo usando a Averaging_Rule:
epil=np.array([0.07652637, 0.03359369, 0.126386,   0.39709159, 0.14086643])
'''

'''
#Episolon ótimo usando a Relative_degree_rule:
epil=np.array([0.48097173,0.51033248, 0.51941568,0.50298528, 0.49401778]) 
'''

'''
#Episolon ótimo usando a Mean Metropolis:
epil=np.array([0.13510579, 0.13915606, 0.29702075, 0.53912501, 0.53799006])
'''

'''
#Episolon ótimo usando a Hasting_Rules::
epil=np.array([0.05794438, 0.05442595, 0.06264365, 0.06446718, 0.06641587]) 
'''   

############################### Carga Média  ##################################

'''
#Episolon ótimo usando a Averaging_Rule:
epil=np.array([0.73779529, 0.67929289, 0.7216009 , 0.79982353, 0.65343889])
'''

'''
#Episolon ótimo usando a Relative_degree_rule:
epil=np.array([0.65100018, 0.60363398, 0.77965685, 0.7122446,  0.78299704]) 
'''

'''
#Episolon ótimo usando a Mean Metropolis:
epil=np.array([0.87716255, 0.86036471, 0.93955563, 0.95596623 ,0.97728897]) 
'''

'''
#Episolon ótimo usando a Hasting_Rules:
epil=np.array([0.02333147, 0.01933355, 0.0535341,  0.05938317, 0.06229497]) #
'''




########################## Carga Alta #######################################



'''
#Episolon ótimo usando a Averaging_Rule:
epil=np.array([0.98542669, 0.96636851, 0.94530173, 0.95202156, 0.96353537])
'''

'''
#Episolon ótimo usando a Relative_degree_rule:
epil=np.array([0.66156639, 0.97063861, 0.94145571, 0.98955311, 0.96984753]) 
'''

'''
#Episolon ótimo usando a Mean Metropolis:
epil=np.array([0.93488094, 0.81422132, 0.99436041, 0.82336146, 0.88289196]) 
'''

'''
#Episolon ótimo usando a Hasting_Rules:
epil=np.array([0.07826813, 0.0092311,  0.05636776, 0.04958781, 0.06634793]) 
'''

#Matriz de Adjacências:
A = np.array([[0,1,0,0,1],
              [1,0,1,0,0],
              [0,1,0,1,0],
              [0,0,1,0,1],
              [1,0,0,1,0]])
#Matriz Identidade:
I=np.identity(len(A))

### Matriz de pesos utilizada ####
MM,epil2=mp.Averaging_Rule(A,epil)
MMi=(MM+I)/2

#Número Máximo de Interações:
N_max=15000
N_max+=1 
  
#Dando o Parâmetro de Parada:
diff=10                           # Diferença inicial
diff_min=0.0001                  # Diferença minima para dizer que convergiu


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

#Não é esse consenso que tem que rodar
#Não colocou a Flag
############################ Algoritmo de Difusão sem Restrições ##################################
tempo1=time.time()
while(sum(flag)!=0 or n_algorit==0):
    #Inicializando as Potências em kda Agente:
            
    #Número Máximo de Interações:
    N_max=15000
    N_max+=1 
    Pg=np.zeros([N_max,nG])
    
    #Custo Incremental:
    r = np.zeros([N_max,nG]) 
    
    #Inicializando o Custo Incremental em kda Agente:
        
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
    #Flag para rodar o while
        flag=np.zeros(nG)
        #Critério de Parada:
        diff=10  
        #Váriaveis de difusão
        var=np.zeros([N_max,nG])
        var[0]=r[0]
        var1=np.zeros([N_max,nG])
    i=0
    #Flag de qual tipo de algortimo se deve rodar:(EXplicado melhor logo abaixo)
    flag_sem_limites = 1
    flag_limite_superior = 0    
        #Consenso em si:
    while(i!=N_max-1 and diff>diff_min):     
        d=np.zeros(nG)
        var[i+1]=r[i]-epil2*(sum(Pg[i])-sum(P_ren))
        var1[i+1]=var[i+1] + r[i] - var[i]
        r[i+1] = MMi@var1[i+1]
        if flag_sem_limites ==1:
            for j in Ren:
                Pg[i+1,j]=0
            for j in Carga:
                if(abs(Pg[i,j])>=abs(Carga_lim[j])):
                    Pg[i+1,j]=Carga_lim[j]
                else:
                    Pg[i+1,j] = -(r[i+1,j]-w[j])/(u[j])
            for j in Bat:
                if j in P_n or n_algorit==0:
                    Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j])
                elif j in P_u_max:
                    Pg[i+1,j]=Plim_sup[j]
                elif j in P_u_min:
                    Pg[i+1,j]=Plim_inf[j]
            for j in Desp:
                if j in P_n or n_algorit==0:
                    Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
                elif j in P_u_max:
                    Pg[i+1,j]=Plim_sup[j]
                elif j in P_u_min:
                    Pg[i+1,j]=Plim_inf[j]
        elif flag_limite_superior == 1:
            for j in Ren:
                Pg[i+1,j]=0
            for j in Carga:
                if(abs(Pg[i,j])>=abs(Carga_lim[j])):
                    Pg[i+1,j]=Carga_lim[j]
                else:
                    Pg[i+1,j] = -(r[i+1,j]-w[j])/(u[j])
            for j in Bat:
                if j in P_n or n_algorit==0:
                    Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j])
                elif j in P_u_max:
                    Pg[i+1,j]=(r[i+1,j] - bet[j])/(2*alp[j])
                elif j in P_u_min:
                    Pg[i+1,j]=Plim_inf[j]
            for j in Desp:
                if j in P_n or n_algorit==0:
                    Pg[i+1,j] = (r[i+1,j] - bet[j])/(2*alp[j]) 
                elif j in P_u_max:
                    Pg[i+1,j]= (r[i+1,j] - bet[j])/(2*alp[j]) 
                elif j in P_u_min:
                    Pg[i+1,j]=Plim_inf[j]
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
                pass #Não fazer nd
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
tempo2=time.time()

print("\nTempo Difusão com restrição:",tempo2-tempo1)    
print("\n Parou na interação:",inter) 

#Colocar isso dentro do algoritmo         
r=r[:inter,:]  #Vai cortar a matriz até a parte útil,se parar por diferença
Pg=Pg[:inter,:]


######################## Exibindo os Dados sem restrições na tela ###########################

print("\n A potência de cada agente quando não há restrições:",Pg[-1])
print("\n O custo incremental quando não há restrições será:",round(max(r[-1]),2))
print("\n ###################### ")
############################# Plotando os gráficos ##############################

for i in range(0,nG):
    plt.plot(r[:,i],label=i+1)
plt.legend()
plt.title("Custo Incremental por Interação - Algoritmo de Difusão Exata ")
plt.xlabel("Interação")
plt.xlim(right=2709)
plt.ylabel("Custo Incremental [₩]")
plt.show()

for i in range(0,nG):
    plt.plot(Pg[:,i],label=i+1)
plt.legend()
plt.title("Potência por Interação - Algoritmo de Difusão Exata")
plt.xlabel("Interação")
plt.xlim(right=2709)
plt.ylabel("Potência em cada agente")
plt.show()
