# Bibliotecas uteis: 
from pade.misc.utility import start_loop
from pade.acl.aid import AID
from agent_posto import AgentPosto
from agent_consensusn import Equipment
import pandas as pd

#pade start-runtime --num 1 --port 20000 pade_startn.py


if __name__ == '__main__': 


    df = pd.read_excel('dadosmicro.xlsx')
    df_GPS = df['GPS'].to_numpy()
    df_tinit = df['hour_in'].to_numpy()
    df_ID=df['ID'].to_numpy()
    df_alpha=df['alpha'].to_numpy()
    df_beta=df['beta'].to_numpy()
    df_epil=df['epil'].to_numpy()
    df_pren=df['pren'].to_numpy()
    df_lim=df['lim'].to_numpy()
    df_w=df['w'].to_numpy()
    df_u=df['u'].to_numpy()
    #Wang:
    #df_Pg=df['Pg'].to_numpy()
    
    

    agents = list()
    port = 20000
    k = 1  
    agent_name = 'Agent_posto_{}@localhost:{}'.format(port, port)
    agent_posto = AgentPosto(AID(name=agent_name))
    agents.append(agent_posto)

    number_agconsensus = 6
    for i in range(number_agconsensus):      
        #Wang:
        #dt_ag = {'GPS':df_GPS[i], 'hour_in': df_tinit[i], 'hour_out': 500000,'ID':df_ID[i], 
        #         'alpha':df_alpha[i],'beta':df_beta[i],'epil':df_epil[i],'pren':df_pren[i],
        #         'lim':df_lim[i],'w':df_w[i],'u':df_u[i],'Pg':df_Pg[i]}
        #Microrrede
        dt_ag = {'GPS':df_GPS[i], 'hour_in': df_tinit[i], 'hour_out': 500000,'ID':df_ID[i], 
                 'alpha':df_alpha[i],'beta':df_beta[i],'epil':df_epil[i],'pren':df_pren[i],
                 'lim':df_lim[i],'w':df_w[i],'u':df_u[i]}
        
        agent_name = 'Agente_{}'.format(i+1)+'_{}@localhost:{}'.format(port + (i+1)*k, port + (i+1)*k)
        agent_sub = Equipment(AID(name=agent_name),agent_posto, dt_ag)
        agents.append(agent_sub)
    

    start_loop(agents)
