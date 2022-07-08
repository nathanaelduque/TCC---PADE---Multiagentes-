###################  Algoritmo genético para a escolha do episolon ################

#################### Importando as Bibliotecas necessárias #######################

import AG_episolon as ag
import numpy as np
import matplotlib.pyplot as plt

############################ Parâmetros do algoritmo ###############################

popsize=5000
pmut= 10
n_cruz= 15000


############################# Definindo o problema ##############################0


############################ Chamando Função Geração ##############################

epi=ag.genpop(popsize)

################################# Avaliando aptidão #######################################

fitness=ag.fitness_evaluation(epi,popsize)

############################### Selecionando dois pais #######################################
for i in range(0,n_cruz):
    print("Cruzamento número:",i)
    parent1,parent2=ag.selection(fitness,popsize)
    
############################ Performando o cruzamento ###################################

    offspring =ag.crossover(parent1,parent2,epi)
    
################################### Mutação ###############################################

    offspring=ag.mutation(pmut,offspring)
    
########################## Avaliando a aptidão do filho #################################

    fitness_offspring = ag.offspring_evaluation(offspring)
    
######################### Colocando o filho na matriz de soluções #######################

    pop,a,b=ag.replacement(epi, fitness, fitness_offspring, offspring)
#Sai o pior e entra o filho
print("Acabou")
print(fitness)
best= np.argmin(fitness)
print("A solução é:",pop[best])
print("E sua aptidão é:",fitness[best])

a=np.array(a)

b=np.array(b)

plt.plot(a-b,color='red')
plt.title("Convergência")
plt.show()

x=[]
for i in range(0,len(pop)):
    x.append(i)
    
plt.scatter(x,fitness)
plt.title("Dispersão Vetor Final")
plt.show()

x1=[]
for i in range(0,len(a)):
    x1.append(i)

plt.scatter(x1,a)
plt.title("Dispersão Pior solução c.i")
plt.show()

