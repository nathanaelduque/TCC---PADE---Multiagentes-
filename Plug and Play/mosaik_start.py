import mosaik
from time import sleep 

# python mosaik_start.py

if __name__ == '__main__':

    num_agentes=6
    # sleep(2*num_agentes)

    START = 0
    END = 10000
    
    port=20000
    k=1

    sim_config = {'Interface':{'python':'SimuladorInterface:Interfacex'}}

    sim_config.update({'Agent_posto':{'connect':'localhost:{}'.format(port)}})

    for i in range(num_agentes):
        sim_config.update({'Agente_{}'.format(i+1): {'connect':'localhost:{}'.format(port + (i+1)*k)}})

    world = mosaik.World(sim_config, debug=True)


    # inicializar e instanciar agentes e interfaces logo em seguida
    agen = list() 
    for i in range(num_agentes):
        agen.append(world.start('Agente_{}'.format(i+1),eid_prefix='AgEquip',start = START,step_size = 1))
        agen[i] = agen[i].InterfaceAgente()

    agen.append(world.start('Agent_posto',eid_prefix='AgPosto',start = START,step_size = 1))
    agen[i+1] = agen[i+1].InterfaceAgente()

    intf = world.start('Interface', eid_prefix='Interface_', start = START,step_size = 1)
    intf = intf.Interface.create(num_agentes+1)

    for mod0, int0 in zip(agen, intf):
        # world.connect(a, b, 'val_in')
        # world.connect(b, a, 'val_in', time_shifted=True, initial_data={'val_in': 0})
        world.connect(mod0, int0, 'val_in', async_requests=True)

    world.run(until=END)
