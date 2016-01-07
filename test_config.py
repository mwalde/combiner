from testlib.util.testPlatform import testPlatform
import sys
#from config.x import test_config



#from config.x import test_config  



if __name__ == '__main__':
#    tp = testPlatform()     # initialize sys.path  
    print sys.path
#    from config.x import test_config  
    # before we load the config
    content = open('C:/airfiber/config/x.py', 'r').read()
    print content
    eval(content)
    cfg = test_config()     # before we read the config
    