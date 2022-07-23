# Simulador da interface do Mosaik

import mosaik_api

MOSAIK_MODELS = {
    'api_version': '2.2',
    'models': {
        
        'Interface': {
            'public': True,
            'params': [],                
            'attrs': ['val_in'],} ,
    },
}


class Interfacex(mosaik_api.Simulator):
    def __init__(self):
        super(Interfacex, self).__init__(MOSAIK_MODELS)
        self.step_size = None
        

    def init(self, sid,eid_prefix,start, step_size):
        self.sid = sid        
        self.eid_prefix = eid_prefix
        self.eid = '{}{}'.format(self.eid_prefix, '0')
        self.start = start
        self.step_size = step_size
        return self.meta


    def create(self, num, model):
        entities_info = list()
        for i in range(num):
            entities_info.append(
                {'eid': '{}.{}'.format(i, i), 'type': model, 'rel': []})
        return entities_info

    def step(self, time, inputs):
        
        if time % 100 == 0 and time != 0:      
            pass#print(time)
        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        return data




# def main():
#     return mosaik_api.start_simulation(Interfacex())