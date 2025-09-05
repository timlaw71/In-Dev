# divide_networks.py
import ipaddress

def divide_networks(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            line = line.strip()
            try:
                network = ipaddress.ip_network(line, strict=False)
                if network.prefixlen == 24:
                    subnets = list(network.subnets(new_prefix=28))
                else:
                    subnets = [network]
                for subnet in subnets:
                    outfile.write(str(subnet) + "\n")
            except ValueError:
                print(f"Invalid network: {line}")

if __name__ == "__main__":
    input_file = "asn_prefixes.txt"
    output_file = "divided_prefixes.txt"
    divide_networks(input_file, output_file)
    print(f"Divided prefixes written to {output_file}")

