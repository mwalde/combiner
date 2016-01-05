import pickle



class testLimits():
    
#    limit_entry = { testname : (value,plus,minus) }
    
    def __init__(self, **kwargs):
        self.limitsFile   = kwargs.get('limitsFile','test_limits.pkl')
        self.Limits   = kwargs.get( 'limitsDict', [] )
        # initialize LimitType lookup table
        self.LimitType = {
            "HighLow"   : self.__HighLow,
            "PlusMinus" : self.__PlusMinus,
            "PassFail"  : self.__PassFail,
            "Ignore"    : self.__Ignore
            }
        # initialize local data
        self.__errMsgs = []
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
        pickle.dump( self.Limits, open( self.limitsFile, "wb"))
        
    # test limit functions
            
    def testLimit(self, testname, value, msgtag=""):
        try:
            limit = self.Limits[testname]
        except:
            print "Limit not found: %s" % testname
            return (True,"")
        try:
            return self.LimitType[limit[0]](limit, testname, value, msgtag)
        except:
            print "unknown test limit type: ",limit[0]
            return (False,"")
        
    def __PlusMinus(self, limit, testname, value, msgtag):
        limit_val = limit[1]
        limit_hi = float(limit[1]) + float(limit[2])
        limit_lo = float(limit[1]) - float(limit[3])
        result = self.__HighLow( (limit[0],str(limit_hi),str(limit_lo)),testname,value, msgtag)
        return result


    def __HighLow(self, limit, testname, value, msgtag):
        print limit,value
        if float(value) > float(limit[1]):
            msg = "%s: %s exceeds hi limit %s" % (testname,str(value),str(limit[1]))
            self.__errMsgs.append(msg)
            return (False,msg)
        if float(value) < float(limit[2]):
            msg = "%s: %s exceeds lo limit %s" % (testname,str(value),str(limit[2]))
            self.__errMsgs.append(msg)
            return (False,msg)
        return (True,"")
    
    
    def __PassFail(self, limit, testname, value, msgtag):
        if value.upper() == 'FAIL':
            msg = "%s:FAILED" % (testname)
            self.__errMsgs.append(msg)
            return (False,msg)
        else:
            return (True,"")

    def __Ignore(self, limit, testname, value, msgtag):
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
#    limitsDict = {
#                "num_test0" : (l.NUM,'-1.0','.5','.5'),
#                "pf_test" :   (l.PF,),
#                "hl_test0" :  (l.HL, '-1.046', '-12.1234'),
#                "ig_test"  :  (l.IG,)
#                }
    limitsDict = {
                "num_test0" : ("PlusMinus",-1.0,.5,.5),
                "pf_test" :   ("PassFail",),
                "hl_test0" :  ("HighLow", -1.046, -12.1234),
                "ig_test"  :  ("Ignore",)
                }
    l = testLimits(limitsDict=limitsDict)
    l.writeLimits()
    print limitsDict
    print
    
        
        
    result = l.testLimit('pf_test', "PASS")
    print 1,result
    result = l.testLimit('pf_test', "fail")
    print 2,result
    result = l.testLimit('pf_test', "PaSs")
    print 3,result
    result = l.testLimit('num_test0', "-.4")
    print 4,result
    result = l.testLimit('hl_test0', "-1.4")
    print 5,result
    result = l.testLimit('hl_test0', "-13.4")
    print 6,result
    result = l.testLimit('bad_test', "-13.4")
    print 7,result
    result = l.testLimit('ig_test', "-13.4")
    print 8,result
    
    print "Error Messages"
    print l.errMsgs()
    
    
    
if __name__ == '__main__':
    test()
        
    
    