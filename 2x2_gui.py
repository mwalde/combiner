from testlib.util.db import Db
from combiner import combiner
from testlib.GUI.gui import GUI

def test_hardware():
    from testlib.equip.nrpz11 import nrpz11
    from testlib.equip.hp11713A import hp11713A
    from testlib.equip.sg6000l import SG6000L
    from config import test_config
    
    cfg = test_config()
   
    swt = hp11713A( host=cfg.get('SWTIP'))
    
    pmLoss = nrpz11(cfg.get('PMLOSS'), timeout=10)
    pmIso  = nrpz11(cfg.get('PMISO' ), timeout=10)
    sg = SG6000L(port=cfg.get('SGPORT'))
#    pmLoss.calibrate()
#    pmIso.calibrate()
    pmLoss.setoffset(0)
    pmIso.setoffset(0)
    
    tdata = Db(cfg.get('DBFILE'), cfg.get('DBTBL'))
    tdata.de_debug = 1
    
    c = combiner(pmPwrLoss=pmLoss.avgPower,
                        pmFreqLoss=pmLoss.setfreq,
                        pmPwrIso=pmIso.avgPower,
                        pmFreqIso=pmIso.setfreq,
                        sgFreq=sg.setFreq,
                        swtOn=swt.SwitchOn,
                        swtOff=swt.SwitchOff,
                        dbWrite=tdata.Entry)
    c.initialize()
    c.printCAL()
    c.testSequence( testSeq=c.Seq2X2)
    tdata.Close()


def guitest():

    
if __name__ == '__main__':
    test_hardware()

 

 