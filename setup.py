import argparse

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("installation_mode", help="An integer that.", type=int)
args = parser.parse_args()
print(args.counter + 1)