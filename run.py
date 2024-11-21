import argparse

def main():
    parser = argparse.ArgumentParser(description='A command line tool with optional arguments.')
    
    # Optional arguments
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-o', '--output', type=str, help='Output file name')
    parser.add_argument('-n', '--number', type=int, help='A number input')

    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled")
    
    if args.output:
        print(f"Output file: {args.output}")
    
    if args.number is not None:
        print(f"Number: {args.number}")

if __name__ == "__main__":
    main()