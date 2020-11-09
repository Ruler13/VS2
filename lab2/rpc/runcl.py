import time
import rpc
from context import lab_logging


def print_result(result):
    print("Result: {}".format(result.value))


def print_error(error):
    print(error)


lab_logging.setup()
cl = rpc.Client()
cl.run()
base_list = rpc.DBList({'foo'})
cl.run_append('bar', base_list,print_result,print_error)
for i in range(20):
    print("Process is running: " + str(i))
    time.sleep(1)
cl.stop()