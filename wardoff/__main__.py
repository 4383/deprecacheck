from wardoff import cli


def main():
    args = cli.main().parse_args()
    print("Still in development nothing to return for now.")
    analyzer = args.project
    _ = args.output
    analyzer.analyze()


if __name__ == "__main__":
    main()
