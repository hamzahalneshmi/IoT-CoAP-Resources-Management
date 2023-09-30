import getopt
import sys

from coapthon.server.coap import CoAP
from plugtest_resources import TestResource, SeparateResource, ObservableResource, LargeResource, LargeUpdateResource, \
    LongResource

__author__ = 'Giacomo Tanganelli'


class CoAPServerPlugTest(CoAP):
    def __init__(self, host, port, multicast=False, starting_mid=None):
        CoAP.__init__(self, (host, port), multicast, starting_mid)
        self.add_resource('test/', TestResource())
        self.add_resource('separate/', SeparateResource())
        self.add_resource('seg1/', TestResource())
        self.add_resource('seg1/seg2/', TestResource())
        self.add_resource('seg1/seg2/seg3/', TestResource())
        self.add_resource('query/', TestResource())
        self.add_resource('obs/', ObservableResource(coap_server=self))
        self.add_resource('large/', LargeResource(coap_server=self))
        self.add_resource('large-update/', LargeUpdateResource(coap_server=self))
        self.add_resource('long/', LongResource())


def usage():  # pragma: no cover
    print("plugtest_coapserver.py -i <ip address> -p <port>")


def main(argv):  # pragma: no cover
    ip = "127.0.0.1"
    port = 5683
    try:
        opts, args = getopt.getopt(argv, "hi:p:", ["ip=", "port="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = int(arg)

    server = CoAPServerPlugTest(ip, port)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        server.close()


if __name__ == "__main__":
    main(sys.argv[1:])
