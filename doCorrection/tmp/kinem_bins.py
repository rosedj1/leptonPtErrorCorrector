kinem_bin_dict = {                                                                                      
    # Electrons_ECAL
    'ECAL_barrel_pterrlow_a': {'eta_min':0.0,  'eta_max':0.8,  'rel_pTErr':'< 0.03', 'ecalDriven':'1', 'pterrcorrfactor':1.52153478706 },
    'ECAL_barrel_pterrlow_b': {'eta_min':0.8,  'eta_max':1.0,  'rel_pTErr':'< 0.03', 'ecalDriven':'1', 'pterrcorrfactor':1.44215391169 },
    'ECAL_barrel_pterrhigh' : {'eta_min':0.0,  'eta_max':1.0,  'rel_pTErr':'> 0.03', 'ecalDriven':'1', 'pterrcorrfactor':0.72346430324 },
    'ECAL_endcap_pterrlow_a': {'eta_min':1.0,  'eta_max':1.2,  'rel_pTErr':'< 0.07', 'ecalDriven':'1', 'pterrcorrfactor':1.36207009972 },
    'ECAL_endcap_pterrlow_b': {'eta_min':1.2,  'eta_max':1.44, 'rel_pTErr':'< 0.07', 'ecalDriven':'1', 'pterrcorrfactor':1.46734370524 },
    'ECAL_endcap_pterrlow_c': {'eta_min':1.44, 'eta_max':1.57, 'rel_pTErr':'< 0.07', 'ecalDriven':'1', 'pterrcorrfactor':1.55992023795 },
    'ECAL_endcap_pterrlow_d': {'eta_min':1.57, 'eta_max':2.0,  'rel_pTErr':'< 0.07', 'ecalDriven':'1', 'pterrcorrfactor':1.50433436363 },
    'ECAL_endcap_pterrlow_e': {'eta_min':2.0,  'eta_max':2.5,  'rel_pTErr':'< 0.07', 'ecalDriven':'1', 'pterrcorrfactor':2.08249421695 },
    'ECAL_endcap_pterrhigh' : {'eta_min':1.0,  'eta_max':1.2,  'rel_pTErr':'> 0.07', 'ecalDriven':'1', 'pterrcorrfactor':0.100000000001 },
    # Electrons_Tracker
    'Tracker_barrel'        : {'eta_min':0.0,  'eta_max':1.44, 'rel_pTErr':'> -1.0', 'ecalDriven':'0'},
    'Tracker_endcap_a'      : {'eta_min':1.44, 'eta_max':1.6,  'rel_pTErr':'> -1.0', 'ecalDriven':'0'},
    'Tracker_endcap_b'      : {'eta_min':1.6,  'eta_max':2.0,  'rel_pTErr':'> -1.0', 'ecalDriven':'0'},
    'Tracker_endcap_c'      : {'eta_min':2.0,  'eta_max':2.5,  'rel_pTErr':'> -1.0', 'ecalDriven':'0'},
    # Muons
    'mu_barrel'      : {'eta_min':0.0,  'eta_max':0.9, 'rel_pTErr':None, 'ecalDriven':'0'},
    'mu_endcap_mex23': {'eta_min':0.9,  'eta_max':1.8, 'rel_pTErr':None, 'ecalDriven':'0'},
    'mu_endcap_mex1' : {'eta_min':1.8,  'eta_max':2.4, 'rel_pTErr':None, 'ecalDriven':'0'},
}
