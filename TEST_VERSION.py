#===========================================================================
#           Software Version String
#===========================================================================

import os.path, time 

class Rev():
    SwVer = "0.0.0.dev"
    Date = '$Date: 2015-11-19 11:40:23 -0600 (Thu, 19 Nov 2015) $'
    Revision = '$Revision: 28574 $'
    Author = '$Author: mbroeske $'
    HeadURL = '$HeadURL: https://ubnt-lt.selfip.net/svn/devbox/branches/af-test/all_test/TEST_VERSION.py $'
    Id = '$Id: TEST_VERSION.py 28574 2015-11-19 17:40:23Z mbroeske $'
     
    def getSwVer(self):
        if self.SwVer.count('dev'):
            return "%s %s" % (self.SwVer, self.getDate())
        else:
            return "%s_%s" % ( self.SwVer, self.getVer())
        
    def getDate(self):
        date = self.Date[7:17]
#        date = self.Date.replace('$Date:','')
#        date = date.strip('$')
#        date = date.strip()
        return date
        
    def getVer(self):
        rev = self.Revision.replace('$Revision: ', '').strip('$')
        return rev
        
    def getDT(self):
        print "last modified: %s" % time.ctime(os.path.getmtime(__file__))
        print "created: %s" % time.ctime(os.path.getctime(__file__))    
    
if __name__== '__main__':
    rev = Rev()
    print rev.getSwVer()
    print rev.getDate()
    print rev.getDT()
    
    