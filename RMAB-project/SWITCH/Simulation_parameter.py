import json
sim_dict = {
    'queue_size': 20,
    'u_unit' : 0.05,
    'pool_size': 320000,
    'total_time' : 100010,
    'wittle_update_cycle' : 100000,
    'pcome' : [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ],
    'bstart_tim' : [100],
    'Scheduling_algorithm' : "MAX_QUEUE_LEN",
    'Congestion_handling' : 'FULL_DROP',
    'burst_version':'v1',
    'wf':0.8
}





with open("./TEST/simulation_v2_2.json", "w", encoding='utf-8') as f:
    sim_json = json.dump(sim_dict,f,indent=2, sort_keys=True, ensure_ascii=False)