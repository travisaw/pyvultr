from requests import get

class Ipify:

    def get_ip4(self):
        return get('https://api.ipify.org').content.decode('utf8')

    def get_ip6(self):
        return get('https://api64.ipify.org').content.decode('utf8')

    def print_ip(self):
        """
        Prints the IPv4 and IPv6 addresses of the instance.
        
        This method retrieves the IP addresses using the API client and prints them in a formatted manner.
        """
        ip4 = self.get_ip4()
        ip6 = self.get_ip6()
        
        print(f"IPv4 Address: {ip4}")
        print(f"IPv6 Address: {ip6}")
