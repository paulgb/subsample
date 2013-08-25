
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=1000)

    args = parser.parse_args()

    for i in xrange(args.n):
        print i

if __name__ == '__main__':
    main()

