from pade.drivers.mosaik_driver import MosaikCon
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaSubscribeProtocol, FipaRequestProtocol
import json
from datetime import datetime
import pandas as pd
import math
import numpy as np

"""
Para a microrrede, foram utilizados os seguintes ID's:
    
    *0: Carga (Crítica e Não Crítica)
    *1: Energias Renováveis
    *2: Despachável
    *3: Bateria 
    
"""


#OBS: Tire a váriável diferença, pode ser utilizada a variável Pd para isso

#Ainda tenho que reiniciar o número de interações do consenso 



MOSAIK_MODELS = {
    'api_version': '2.2',
    'models': {   
        'InterfaceAgente': {
            'public': True,
            'params': [],                
            'attrs': ['val_in'],},
    },
}



class MosaikSim(MosaikCon):

    
    def __init__(self, agent):
        super(MosaikSim, self).__init__(MOSAIK_MODELS, agent)
        self.entities = list()

    def init(self, sid, eid_prefix, start, step_size):
        self.eid_prefix = eid_prefix
        self.eid = '{}{}'.format(self.eid_prefix, '0')
        self.start = start
        self.step_size = step_size
        return MOSAIK_MODELS

    def create(self, num, model):
        entities_info = list()
        for i in range(num):
            entities_info.append(
                {'eid': '{}.{}'.format(self.sim_id, i), 'type': model, 'rel': []})
        return entities_info

    def step(self, time, inputs):
        
        if time == self.agent.tinic and time != 0:
            self.agent.launch_subscriber_protocol()
            return
        
        
        if  self.agent.flag_1req == 0 and len(self.agent.vz) > 0  :
            self.agent.protocol.pedir_numerovz()
            self.agent.comece_consenso=1
            return
          
        
    
        #Aqui começa o consenso, é a partir daqui que eu vou adaptar para o consenso da
        #microrrede
        if self.agent.comece_consenso==1:
           self.agent.modifique=1
                     
           
           # Ainda tenho que alterar a matriz de pesos 
           #processo =0 irá calcular a matriz de pesos 
           if self.agent.processo ==0 and self.agent.modifique==1:
                self.agent.calculate_weightMX()
                if self.agent.vez==2:
                    self.agent.processo=1 #Será o próximo passo do consenso
                    self.agent.modifique=0# só rodará no proximo tempo do mosaik
                    
                    
           #processo=1 irá mandar a mensagem de consenso 
           if self.agent.processo ==1 and self.agent.modifique==1:
                 
                 self.agent.answer_request.consensus_message()
                 self.agent.modifique=0
                 return 
        
          #processo=2 irá calcular a variável de consenso 
           if self.agent.processo==2 and self.agent.modifique==1:
                self.agent.answer_request.calculate_consensus()
                self.agent.modifique=0
                    
               
        return time + self.step_size
    

    def get_data(self, outputs):
        response = dict()
        for model, list_values in outputs.items():
            response[model] = dict()
            for value in list_values:
                response[model][value] = 1
        return response

class Request_Consensus(FipaRequestProtocol):
    """FIPA Request Behaviour Responde número de vizinhos
    """
    def __init__(self, agent):
        super(Request_Consensus, self).__init__(agent=agent,
                                          message=None,
                                          is_initiator=False)
        
        self.df = pd.DataFrame({'Agent name': [],'Iter': [],'x0':[],'Convergiu':[],'deviation':[]})



    # Lida com o Request feito no protocolo Subscribe em que cada VE pergunta o número de vz aos seus vz
    def handle_request(self, message):
        super(Request_Consensus, self).handle_request(message)
        
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        reply.set_content(json.dumps(len(self.agent.vz)))
        self.agent.send(reply)




    # Lida com os informes tanto da resposta do número de vz como os informes do consensus
    def handle_inform(self, message):

        #Coloque um if aqui para diferenciar os processos 
        
        content = json.loads(message.content)
        if self.agent.processo == 0:
            if len(self.agent.diag_mx) < len(self.agent.vz) and self.agent.flag_inf == 0:
                self.agent.diag_mx[message.sender.localname] = content # adiciono a quantidade de vizinhos
                if len(self.agent.diag_mx) == len(self.agent.vz):
                    self.agent.mosaik_sim.step_done()
                    
        if self.agent.processo == 1:
            self.agent.vcons[message.sender.localname] = content[0]
            self.agent.vconver[message.sender.localname] = content[1]
            self.agent.deviation[message.sender.localname] = content[2]
            if len(self.agent.vcons) == len(self.agent.vz):
                self.agent.vcons[self.agent.aid.localname] = self.agent.r
                self.agent.vconver[self.agent.aid.localname] = self.agent.Convergiu
                self.agent.deviation[self.agent.aid.localname] = self.agent.Pd
                if self.agent.iter < self.agent.maxiter:
                    new_row = {'Agent name':self.agent.aid.localname, 'Iter': self.agent.iter,'x0':self.agent.r,'Convergiu':self.agent.Convergiu,'deviation':self.agent.deviation}
                    self.df = self.df.append(new_row, ignore_index=True)
                    self.agent.processo=2
                    self.agent.mosaik_sim.step_done() # o step done pode estar com uma identação errada
                
    def consensus_message(self):
        
        #Na difusão precisa de um pré-processamento, aqui n precisa
        
       
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        for vizinho in self.agent.vz:
            message.add_receiver(AID(vizinho))
        resposta = []
        resposta.append(self.agent.r)   
        resposta.append(self.agent.Convergiu) 
        resposta.append(self.agent.Pd)       
        message.set_content(json.dumps(resposta))
        self.agent.send(message)

    def calculate_consensus(self):
        #salvando as variáveis necessárias: 

        self.agent.salve_Pg=self.agent.Pg
        self.agent.salve_r=self.agent.r
        #Processa a informação recebida
        for key in self.agent.vcons:
            self.agent.wc[key] = self.agent.weight[key]*self.agent.vcons[key] 
            self.agent.wd[key] = self.agent.weight[key]*self.agent.deviation[key] 
        self.agent.r = sum(self.agent.wc.values()) + self.agent.epil*self.agent.Pd #Atualizando o r 
        #Atualizando o Pg, para tal,deve-se separar por ID:
        
        if self.agent.ID==0:
            if(abs(self.agent.Pg)>=abs((self.agent.w)/(self.agent.u))):
                self.agent.Pg=(self.agent.w)/(self.agent.u)
            else:
                self.agent.Pg=-(self.agent.r-self.agent.w)/self.agent.u
             
        if self.agent.ID==1:
            self.agent.Pg=0
            
        if self.agent.ID==2:
            if self.agent.ultrapassado == 1:
               self.agent.Pg=self.agent.lim
            else:
                 self.agent.Pg=(self.agent.r - self.agent.bet)/(2*(self.agent.alp))           
        if self.agent.ID==3:
            if self.agent.ultrapassado == 1:
               self.agent.Pg=self.agent.lim
            else:
               self.agent.Pg=(self.agent.r - self.agent.bet)/(2*self.agent.alp) 
        self.agent.Pd= sum(self.agent.wd.values()) - (self.agent.Pg - self.agent.salve_Pg)
        display_message(self.agent.aid.localname, 'Inter:')  
        display_message(self.agent.aid.localname, self.agent.iter)
        if(self.agent.iter%((6/2)+1)==0): # se for =0 irá calcular 
                #diferenca=abs(self.agent.Pd) #Pode ser aqui? creio que n
                diferenca=abs(self.agent.r-self.agent.salve_r)
                if diferenca<self.agent.diff_min:
                    self.agent.Convergiu=1
                else:
                    self.agent.Convergiu=0
                    
        elif(self.agent.iter%((6/2)+1)==((6/2))):
            display_message(self.agent.aid.localname, self.agent.r)
            display_message(self.agent.aid.localname, 'Convergiu:')    
            display_message(self.agent.aid.localname, self.agent.Convergiu)
            if self.agent.Convergiu==1:
                if abs(self.agent.Pg) >= abs(self.agent.lim):
                    self.agent.ultrapassado=1
                    

                    display_message(self.agent.aid.localname, "Passei o meu limite!")
                else:
                    self.agent.ultrapassado+=0 # += está aqui, pois caso um agente já tiver 
                                               # ultrapassado, temos que seu limite já está
                                               # setado no máx, porém ele vai entrar aqui
                                               # e se tiver = 0 vai reiniciar a variável.
                
                
                if self.agent.n_algorit == 0:
                    display_message(self.agent.aid.localname,"Rodou sem limites")
                    display_message(self.agent.aid.localname, "Número de interações:")
                    display_message(self.agent.aid.localname, self.agent.iter)
                    display_message(self.agent.aid.localname, "Custo Incremental")
                    display_message(self.agent.aid.localname, self.agent.r)
                    display_message(self.agent.aid.localname, "Potência no agente")
                    display_message(self.agent.aid.localname, self.agent.Pg)
                    
                    self.agent.iter=0
                    
                    #Reiniciando as variáveis necessárias
                    self.agent.salve_Pg=0
                    self.agent.Convergiu=0
                    self.agent.vconver=dict()
                    self.agent.w=self.agent.guarde_w
                    self.agent.u=self.agent.guarde_u
                    self.agent.Pg=self.agent.guarde_Pg
                    self.agent.Pd=self.agent.guarde_Pd
                    if self.agent.ID == 0:
                        self.agent.r=self.agent.w
                    elif self.agent.ID == 1:
                        self.agent.r = 0
                    elif self.agent.ID == 2 or self.agent.ID == 3:
                        self.agent.r = 2*self.agent.alp*self.agent.Pg +self.agent.bet
                        
                    self.agent.comece_consenso=0
                elif self.agent.n_algorit ==1:
                    #Reiniciando as variáveis necessárias
                    display_message(self.agent.aid.localname,"Rodou pela segunda vez")
                    display_message(self.agent.aid.localname, "Número de interações:")
                    display_message(self.agent.aid.localname, self.agent.iter)
                    display_message(self.agent.aid.localname, "Custo Incremental")
                    display_message(self.agent.aid.localname, self.agent.r)
                    display_message(self.agent.aid.localname, "Potência no agente")
                    display_message(self.agent.aid.localname, self.agent.Pg)



                    self.agent.salve_Pg=0
                    self.agent.Convergiu=0
                    self.agent.vconver=dict()
                    self.agent.w=self.agent.guarde_w
                    self.agent.u=self.agent.guarde_u
                    self.agent.Pg=self.agent.guarde_Pg
                    self.agent.Pd=self.agent.guarde_Pd
                    self.agent.iter=0
                    

                    
                    if self.agent.ID == 0:
                        self.agent.r=self.agent.w
                    elif self.agent.ID == 1:
                        self.agent.r = 0
                    elif self.agent.ID == 2 or self.agent.ID == 3:
                        self.agent.r = 2*self.agent.alp*self.agent.Pg +self.agent.bet
                    
                elif self.agent.n_algorit == 2:
                    display_message(self.agent.aid.localname,"Acabou :)")
                    display_message(self.agent.aid.localname, "Número de interações:")
                    display_message(self.agent.aid.localname, self.agent.iter)
                    display_message(self.agent.aid.localname, "Custo Incremental")
                    display_message(self.agent.aid.localname, self.agent.r)
                    display_message(self.agent.aid.localname, "Potência no agente")
                    display_message(self.agent.aid.localname, self.agent.Pg)
                    self.agent.iter=self.agent.maxiter
                    # O comece consenso estava na mesma identação que o else
                    # mas agr que o código tem limites, ele  ficará aqui 
                    self.agent.comece_consenso=0
                self.agent.n_algorit+=1
                
                        
            
                
        else:
            for key in self.agent.vconver:
              self.agent.Convergiu = self.agent.Convergiu*self.agent.vconver[key] 
                  
        self.agent.iter = self.agent.iter + 1
        self.agent.vcons = dict()
        self.agent.wc = dict()
        self.agent.wd=dict()
        self.agent.vconver=dict()
        self.agent.deviation=dict()
        self.agent.processo=1


class SubscriberProtocol(FipaSubscribeProtocol):

    def __init__(self, agent, message):
        super(SubscriberProtocol, self).__init__(agent,
                                                 message,
                                                 is_initiator=True)

    def on_start(self):
        super(SubscriberProtocol, self).on_start()

    def handle_agree(self, message):
        self.agent.mosaik_sim.step_done()

    def handle_inform(self, message):

        if message.sender.localname == 'Agent_posto_20000':    
            print('Aqui')
            content = json.loads(message.content)
            ag_ativos = content 
            nAG_ativos = len(content)
            num_maxVZ = 2
            
            # responsável por verificar a quantidade de agentes podem ser meus vizinhos
            if nAG_ativos <= num_maxVZ:
                nVz = nAG_ativos - 1  #N: Creio que é por causa do for mais a frente 
                                      #N: Ex: for i in range(0,2): 0,1,2 [seriam 3]
            else:
                nVz = num_maxVZ

            myindex = ag_ativos.index(self.agent.aid.localname)
            ag_ativos.pop(myindex) # a partir daqui só tenho possíveis vizinhos

            '''Houve alteração na topologia, vou zerar minha lista de vizinhos,
             consequentemente, também irei zerar a matriz diagonal'''

            # Essas variaveis estão sendo zeradas por causa da alteração topológica da rede
            # Importante lembrar que também terei que fazer um "esquema" parecido para quando
            # os VEs saírem do estacionamento. Mas, por enquanto, isso não está sendo feito.
            # Então irei deixar dessa maneira. 
            self.agent.vz = None
            self.agent.flag_inf = 0
            self.agent.diag_mx = dict()
            self.agent.weight = dict()
            self.agent.vcons=dict()
            self.agent.deviation=dict()
            self.agent.vconver=dict()
            
            
            self.agent.vez=0
            self.agent.processo=0 
            self.agent.modifique=1
            self.agent.comece_consenso=0
            self.agent.iter=0
            
            
            self.agent.processo=0
            
            

            self.agent.vz = self.gerar_numVZ(nVz,myindex,ag_ativos)
            self.agent.flag_1req = 0
            
            

            
            # essa parte do código tem de melhorar, porque a entrada de carros é aleatoria
            # dessa forma, se os VE entrarem um próximo ao outro vai dar incompatibilidade de tempos
    def pedir_numerovz(self):
        if self.agent.vz != []:
            #pedindo o meu número de vizinhos
            msg = ACLMessage(ACLMessage.REQUEST)
            msg.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
            msg.set_content("Number of Neighboor?")
            for vizinho in self.agent.vz:
                msg.add_receiver(AID(vizinho))
            self.agent.flag_1req =1
            self.agent.send(msg)
            self.agent.comece_consenso=0 
        return #Coloquei tbm





    def gerar_numVZ(self,nVz,myindex,ag_ativos):
        vz = list()
        for i in range(nVz):
            x = myindex + math.ceil(i/2)*(-1)**i
            if x >= len(ag_ativos):
                x = x - len(ag_ativos)
            vz.append(ag_ativos[x])
        return vz




class Equipment(Agent):

    def __init__(self, aid, ag_pub, dts):
        super(Equipment, self).__init__(aid=aid, debug=False)
        self.mosaik_sim = MosaikSim(self)
        display_message(self.aid.localname, 'Agente sendo executado!')

        # entradas
        self.tinic = dts['hour_in']
        self.tcanc = dts['hour_out']
        self.GPS = dts['GPS']
        self.ID=dts['ID']
        self.alp=dts['alpha']
        self.bet=dts['beta']
        self.epil=dts['epil']
        self.pren=dts['pren']
        self.lim=dts['lim']
        self.w=dts['w']
        self.u=dts['u']
        self.Pg=0
        #self.Pg=0
        self.n_algorit=0  
        
        #entradas 'calculadas'

        if self.ID == 0:
            self.r=self.w
        elif self.ID == 1:
            self.r = 0
        elif self.ID == 2 or self.ID == 3:
            self.r = 2*self.alp*self.Pg +self.bet
        self.Pd=self.pren #Power Deviation = Power Mismatch 
        
        #entradas guardadas para serem utilizadas na segunda vez que o consenso rodar
        self.guarde_Pg=self.Pg
        self.guarde_Pd=self.Pd
        self.guarde_w=self.w
        self.guarde_u=self.u        
            
        #outras entradas
        self.ag_pub = ag_pub.aid
        self.weight = dict()
        self.iter = 0
        self.maxiter = 5000
        self.wc = dict()
        self.wd=dict()
        self.vcons = dict()
        self.deviation=dict()


        
        
        #Variáveis utilizadas no critério de parada  
        self.Convergiu=0
        self.diff_min=0.0001 
        self.vconver=dict()


        # internas
        self.flag_1req = 1
        self.flag_inf = 1
        self.diag_mx = dict()
        self.comece_consenso=0# Estava 0 # flag utilizada para se começar o consenso 
        self.processo=0 # flag utilizada para identificar em qual processo está 
        self.modifique=1 # flag utilizada para modificar um processo por time do mosaik
        self.vez=0 # só calcula a matriz de pesos na segunda vez que pega os  vizinhos
        self.ultrapassado = 0 # Vai igualar o limite do consenso ao limite de potência, se 
                              # o agente tiver ultrapassado o seu limite final 



        self.answer_request = Request_Consensus(self)
        self.behaviours.append(self.answer_request)
        
        if self.n_algorit == 0:
            display_message(self.aid.name, "Vai rodar sem limites")
            

    def launch_subscriber_protocol(self):
        msg = ACLMessage(ACLMessage.SUBSCRIBE)
        msg.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        msg.set_content(self.GPS)
        msg.add_receiver(self.ag_pub)
        self.protocol = SubscriberProtocol(self,msg)
        self.behaviours.append(self.protocol)
        self.protocol.on_start()
        
    def calculate_weightMX(self):
        self.vez+=1
        if self.vez == 2: #Dois vizinhos,mas eu ainda n automatizei isso 
            for key in self.diag_mx:
                self.weight[key] = (2/(self.diag_mx[key] + len(self.vz) + 1))
            # lembrar que o ultimo elemento da lista se refere ao aii
            self.weight[self.aid.localname] = round((1-sum(self.weight.values())),4) #aqui eu tou calculando o peso do agente a_ii (ele sempre será o ultimo)
        display_message(self.aid.name,self.weight) 
