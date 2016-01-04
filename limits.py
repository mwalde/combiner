import pickle



class testLimits():
    # limit types
    NUM = 0     # numerical     (type, value,plus,minus)
    PF  = 1     # PassFail      (type,)
    HL = 2      # Hi/Lo Range   (type, hi, lo)
    IG = 3      # Ignore        (type,)
    
    Limits = {}
    __errMsgs = []
    
#    limit_entry = { testname : (value,plus,minus) }
    
    def __init__(self, **kwargs):
        self.limitsFile   = kwargs.get('limitsFile','test_limits.pkl')
        self.Limits   = kwargs.get( 'limitsDict', [] )
#        self.loadLimits()
        
        
    
    # load the testLimits pickle file and complain if not found
    def loadLimits(self):
        self.Limits = {}
        try:
            self.Limits = pickle.load( open(self.limitsFile, "rb"))
        except:
            print "Limits file not found! ", self.limitsFile
    
    def writeLimits(self):
        # allow write?
        pickle.dump( self.CAL, open( self.limitsFile, "wb"))
        
    # test limit functions
    
    def testLimit(self, testname, value, msgtag=""):
        try:
            limit = self.Limits[testname]
        except:
            print "Limit not found: %s" % testname
            return (True,"")
            
        type = limit[0]     # get the limit type
        if type == self.NUM:
            return self.__numLimit(limit, testname, value, msgtag)
        if type == self.PF:
            return self.__pfLimit(limit, testname, value, msgtag)
        if type == self.HL:
            return self.__hlLimit(limit, testname, value, msgtag)
        if type == self.IG:
            return (True,"")
            
        print "unknown test limit type: ",type
        return (False,"")
        
    def __numLimit(self, limit, testname, value, msgtag):
        limit_val = limit[1]
        limit_hi = float(limit[1]) + float(limit[2])
        limit_lo = float(limit[1]) - float(limit[3])
        result = self.__hlLimit( (limit[0],str(limit_hi),str(limit_lo)),testname,value, msgtag)
        return result
            
        
    def __hlLimit(self, limit, testname, value, msgtag):
        print limit,value
        if float(value) > float(limit[1]):
            msg = "%s: %s exceeds hi limit %s" % (testname,value,limit[1])
            self.__errMsgs.append(msg)
            return (False,msg)
        if float(value) < float(limit[2]):
            msg = "%s: %s exceeds lo limit %s" % (testname,value,limit[2])
            self.__errMsgs.append(msg)
            return (False,msg)
        return (True,"")
    
    
    def __pfLimit(self, limit, testname, value, msgtag):
        if value.upper() == 'FAIL':
            msg = "%s:FAILED" % (testname)
            self.__errMsgs.append(msg)
            return (False,msg)
        else:
            return (True,"")

    def errMsgs(self):
        str = ""
        for msg in self.__errMsgs:
            str += msg+'\n'
        return str
        

#########################################################################################
#
#   
def test():
    l = testLimits()
    limitsDict = {
                "num_test0" : (l.NUM,'-1.0','.5','.5'),
                "pf_test" :   (l.PF,),
                "hl_test0" :  (l.HL, '-1.046', '-12.1234'),
                "ig_test"  :  (l.IG,)
                }
    l = testLimits(limitsDict=limitsDict)
    
    result = l.testLimit('pf_test', "PASS")
    print result
    result = l.testLimit('pf_test', "fail")
    print result
    result = l.testLimit('pf_test', "PaSs")
    print result
    result = l.testLimit('num_test0', "-.4")
    print result
    result = l.testLimit('hl_test0', "-1.4")
    print result
    result = l.testLimit('hl_test0', "-13.4")
    print result
    result = l.testLimit('bad_test', "-13.4")
    print result
    result = l.testLimit('ig_test', "-13.4")
    print result
    
    print "Error Messages"
    print l.errMsgs()
    
    
    
if __name__ == '__main__':
    test()
        
    
    