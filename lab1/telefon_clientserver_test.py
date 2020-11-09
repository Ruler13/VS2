import os
import unittest
import telefon_clientserver
from multiprocessing import Process


class TestEchoService(unittest.TestCase):
    def setUp(self):
        super().setUp()
        server = telefon_clientserver.Server()
        # pid = os.fork()
        # if pid == 0:
        #    server.serve()
        #    os._exit(0)
        Process(target=server.serve).start()
        # server.serve()
        self.client = telefon_clientserver.Client()


    def test_srv_get_1(self):
        msg = self.client.call("GET AAA")
        self.assertEqual(msg, " Telefonnummer von AAA : 123123")


    def test_srv_get_2(self):
        msg = self.client.call("GET BBB")
        self.assertEqual(msg, " Telefonnummer von BBB : 321321")


    def test_srv_get_all(self):
        msg = self.client.call("GETALL")
        self.assertEqual(msg, ' Alle Telefonnummern: \nName: AAA Tel: 123123\nName: BBB Tel: 321321\nName: CCC Tel: 123245\n')

if __name__ == '__main__':
    unittest.main()
