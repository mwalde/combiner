from testlib.util.db import Db
from combiner import combiner_runtime
from testlib.equip.nrpz11 import nrpz11
from testlib.equip.hp11713A import hp11713A
from testlib.equip.sg6000l import SG6000L
from config import test_config
from limits import testLimits
from testlimits import  limits4x4, limits2x2
from TEST_VERSION import Rev


from testlib.GUI.gui import GUI
from testlib.GUI.status_frame import StatusWindow
from testlib.GUI.entry_frame import PromptWindow, InfoWindow, EntryWindow

def combiner_test():
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
    
if __name__ == '__main__':
    gui = GUI("airFiber Combiner Test", 'Combiner')
    rev = Rev()
    cfg = test_config()
    gui.cfgframe.SetswVer( rev.getSwVer() )
    gui.bar.setMaxSeconds( 60 )
    gui.cfgframe.SetDescription(cfg.get('STATIONID'))

    c = combiner_runtime(cfg=None)
    c.progress = gui.updProgressBar
    
    c.printCAL()
    opid = gui.EnterOperatorID()
    while 1:
            pw = PromptWindow( gui,"**** Ready UUT for test ****",
                               "1) Place board in test fixture\n" + \
                               "2) Connect the cables\n\n",
                               yestxt = "Start Test", notxt = "Exit Program")
            response =  pw.answer.get()
            print response 
            if response =='0':
                break

            gui.elapsedTime(0)

            part_number, hwrev, ccode, model = gui.scan_part_number()
            gui.set_ssid(model)
            pw = EntryWindow( gui, "Scan Serial Number ", 'Enter UUT serial number', '')
            serialnumber = pw.answer.get()
       
            db = Db(cfg.get('DBFILE'), cfg.get('DBTBL'))
            c.dbWrite=db.Entry
            db.Entry(model,"model")
            db.Entry(serialnumber,'serial')
            db.Entry(opid,'operator_id')
            db.Entry(rev.getSwVer(),'test_swver')
            if model == '2x2':
                l = testLimits(limitsDict=limits2x2)
                testSeq = c.Seq2X2
            else:
                l = testLimits(limitsDict=limits4x4)
                testSeq = c.Seq4X4
            c.testLimit = l.testLimit
            c.testSequence( testSeq=testSeq )
            test_time = gui.elapsedTime(1)
            db.Entry(str(int(test_time)), 'test_time')
            gui.completeProgressBar()
            gui.BumpOdometer()
            ErrMsgs = l.errMsgs()
            if len(ErrMsgs) > 2:
                db.Entry(ErrMsgs,'failures')
                db.Entry('FAIL','pass_fail')
                StatusWindow( gui, "Test Status -- %s" % serialnumber, "FAIL", ErrMsgs )
            else:
                db.Entry('PASS','pass_fail')
                StatusWindow( gui, "Test Status -- %s" % serialnumber, "PASS", ErrMsgs )
            
            
            
            db.Close()
            
        

 
