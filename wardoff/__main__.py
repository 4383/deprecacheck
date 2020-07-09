from wardoff import cli
from wardoff import tokenizer as tok


def main():
    args = cli.main().parse_args()
    print("Still in development nothing to return for now.")
    module_analyzer = args.project
    _ = args.output
    module_analyzer.analyze()


def tokenizer():
    args = cli.tokenizer().parse_args()
    for el in tok.tokenizer(args.code, args.trim):
        print(el)


if __name__ == "__main__":
    main()
