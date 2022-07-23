from pade.drivers.mosaik_driver import MosaikCon
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaSubscribeProtocol
import json

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
               
        if time%10 == 0 and self.agent.flag_compTemp == 0 and time != 0:
            display_message(self.agent.aid.localname,'Vai rodar periodicamente')
            display_message(self.agent.aid.localname,time) 
            self.agent.protocol.enviar_inform()
            return
        else:
            pass
        
        return time + self.step_size
    

    def get_data(self, outputs):

        response = dict()
        for model, list_values in outputs.items():
            response[model] = dict()
            for value in list_values:
                response[model][value] = 0 
        return response

class PublisherProtocol(FipaSubscribeProtocol):

    def __init__(self, agent):
        super(PublisherProtocol, self).__init__(agent,
                                                   message=None,
                                                   is_initiator=False)
        # self.agent.agt_ativo = list()
        self.gps = list()
        self.agt_gps = list()

    def handle_subscribe(self, message):
        
        
        self.register(message.sender)
        display_message(self.agent.aid.localname, '{} from {}'.format(message.content,message.sender.name))
        
        resposta = message.create_reply()
        resposta.set_performative(ACLMessage.AGREE)
        resposta.set_content('Subscribe message accepted')
        
        
        self.agt_gps.append((message.sender.localname,message.content)) # coloca as posições fisicas em ordem 
        self.agt_gps.sort(key=lambda x: x[1])
        self.agent.agt_ativo,self.gps = zip(*self.agt_gps)
        self.agent.flag_compTemp = 0
        self.agent.send(resposta)
       

        # print(self.agent.agt_ativo)
    def enviar_inform(self):
        print("Chegou aqui")
        not_mudanca = ACLMessage(ACLMessage.INFORM)
        not_mudanca.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        not_mudanca.set_content(json.dumps(list(self.agent.agt_ativo))) # não preciso enviar as localizações, pois a lista já está em ordem
        self.notify(not_mudanca)
        self.agent.flag_compTemp = 1
        self.agent.mosaik_sim.step_done()


        

    def notify(self, message):
        super(PublisherProtocol, self).notify(message)



class AgentPosto(Agent):

    def __init__(self, aid):
        super(AgentPosto, self).__init__(aid=aid, debug=False)
        self.mosaik_sim = MosaikSim(self)

        self.agt_ativo = list()
        self.flag_compTemp = 1

        self.protocol = PublisherProtocol(self)
        self.behaviours.append(self.protocol)
        display_message(self.aid.localname, 'Agente sendo executado!')
        # self.timed = Time(self)
        # self.behaviours.append(self.timed)