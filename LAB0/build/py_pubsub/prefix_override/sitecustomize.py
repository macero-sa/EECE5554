import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/savannahmacero/EECE5554/LAB0/install/py_pubsub'
