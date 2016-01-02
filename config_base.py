# Factory Combiner Board Test Configuration 
class test_config():
    CONFIG = {
        'PMLOSS' : "RSNRP::0x000c::102973::INSTR",
        'PMISO'  : "RSNRP::0x000c::100759::INSTR",
        'SWTIP'  : "10.8.9.22",
        'SGPORT' : 16,
        'DBFILE' : 'nxntest.db',
        'DBTBL'  : 'NXN_DB',
        }

    def get(self, key):
        try:
            val = self.CONFIG[key]
        except:
            print "Config value: %s not found" % key
            pass
        return val
        
    def disp_entry(self, key):
        print "%8s : " % key,
        print self.get(key)
        
        
def test():
    cfg = test_config()
    cfg.disp_entry("PMLOSS")
    cfg.disp_entry("PMISO")
    cfg.disp_entry("SWTIP")
    cfg.disp_entry("SGPORT")
    cfg.disp_entry("DBFILE")
    cfg.disp_entry("DBTBL")
    
        
if __name__ == '__main__':
    test()


    