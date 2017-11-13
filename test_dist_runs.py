import distribute_runs
import random

# Testing the parser
def test_number_of_runs():
    args = distribute_runs.get_args(['-R','31'])
    assert args.nruns == 31

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
    args = distribute_runs.get_args(['-T'])
    assert args.test_nodes
    args = distribute_runs.get_args([])
    assert not args.test_nodes

def test_randomList():
    # Check that the seed is giving the expected
    # list of random numbers
    random.seed(1)
    r1list = [2, 9, 8, 3, 5, 5, 7, 8, 1]
    r2list = [random.randint(1,10) for i in range(9)]
    assert r1list == r2list

    runique = [2, 9, 8, 3, 5, 7, 1]
    random.seed(1)
    assert runique == distribute_runs.randomList(7,1,10)

def test_parameter_combinations():
    args = distribute_runs.get_args(['--p1','/DipoleShower::A','1','2','--p2','/DipoleShower::B','2.5','--p3','/DipoleShower::Q','a','b','c'])
    par = [args.p1,args.p2,args.p3,args.p4,args.p5]
    paraComb = distribute_runs.parameterCombinations(par)
    res = [('set /DipoleShower::A 1','set /DipoleShower::B 2.5','set /DipoleShower::Q a'),('set /DipoleShower::A 1','set /DipoleShower::B 2.5','set /DipoleShower::Q b'),('set /DipoleShower::A 1','set /DipoleShower::B 2.5','set /DipoleShower::Q c'),('set /DipoleShower::A 2','set /DipoleShower::B 2.5','set /DipoleShower::Q a'),('set /DipoleShower::A 2','set /DipoleShower::B 2.5','set /DipoleShower::Q b'),('set /DipoleShower::A 2','set /DipoleShower::B 2.5','set /DipoleShower::Q c')]
    assert paraComb == res

def test_load():
    args = distribute_runs.get_args(['-L','low'])
    assert args.load == 'low'
    args = distribute_runs.get_args(['-L','1'])
    assert args.load == '1'
    args = distribute_runs.get_args(['-L','2'])
    assert args.load == '2'
    args = distribute_runs.get_args(['-L','3'])
    assert args.load == '3'

def test_clean_up():
    args = distribute_runs.get_args([])
    assert not args.clean_up
    args = distribute_runs.get_args(['-c'])
    assert args.clean_up

def test_subsequent_shower_off():
    args = distribute_runs.get_args([])
    assert args.subsequent_shower
    args = distribute_runs.get_args(['--subsequent-shower'])
    assert not args.subsequent_shower

def test_rerun():
    args = distribute_runs.get_args([])
    assert not args.rerun
    args = distribute_runs.get_args(['-r'])
    assert args.rerun

def test_overwrite():
    args = distribute_runs.get_args([])
    assert not args.overwrite
    args = distribute_runs.get_args(['-O'])
    assert args.overwrite

