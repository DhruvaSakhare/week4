import sys
import argparse

def main():
    parser = argparse.ArgumentParser(usage='stat.py [-c <positiveinteger>] <filename>')
    parser.add_argument('filename', help='Tab-separated file')
    parser.add_argument('-c', type=int, help='Column index (1-based)')
    args = parser.parse_args()

    data = []
    try:
        with open(args.filename, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if args.c:
                    if args.c <= len(parts):
                        data.append(float(parts[args.c - 1]))
                else:
                    for item in parts:
                        data.append(float(item))
    except FileNotFoundError:
        print("File not found.")
    
    return data, args

if __name__ == "__main__":
    data_list, args = main()