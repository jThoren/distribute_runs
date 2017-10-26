import distribute_runs

# Testing the parser
def test_number_of_events():
    args = distribute_runs.get_args(['-N','15067'])
    assert args.nevents == 15067

def test_p1_to_p5():
    ### p1 ###
    args = distribute_runs.get_args(['--p1','/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on'])
    assert args.p1 == ['/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on']
    args = distribute_runs.get_args(['--p1','/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3'])
    assert args.p1 == ['/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3']
        ### p2 ###
    args = distribute_runs.get_args(['--p2','/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on'])
    assert args.p2 == ['/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on']
    args = distribute_runs.get_args(['--p2','/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3'])
    assert args.p2 == ['/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3']
    ### p3 ###
    args = distribute_runs.get_args(['--p3','/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on'])
    assert args.p3 == ['/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on']
    args = distribute_runs.get_args(['--p3','/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3'])
    assert args.p3 == ['/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3']
    ### p4 ###
    args = distribute_runs.get_args(['--p4','/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on'])
    assert args.p4 == ['/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on']
    args = distribute_runs.get_args(['--p4','/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3'])
    assert args.p4 == ['/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3']
    ### p5 ###
    args = distribute_runs.get_args(['--p5','/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on'])
    assert args.p5 == ['/Herwig/DipoleShower/DipoleShowerHandler:DoSubleadingNc','on']
    args = distribute_runs.get_args(['--p5','/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3'])
    assert args.p5 == ['/Herwig/DipoleShower/DipoleShowerHandler:SubleadingNcEmissionLimit','1','2','3']

def test_test_nodes():
    args = distribute_runs.get_args(['-T','True'])
    assert args.test_nodes == True
    args = distribute_runs.get_args([])
    assert args.test_nodes == False
    
#def test_events_per_node():
#    args = distribute_runs.get_args(['-N','246','-E','123'])
#    assert args.nnode == 123
