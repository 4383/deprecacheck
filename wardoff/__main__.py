from wardoff import argparser


def main():
    args = argparser().parse_args()
    analyzer = args.project
    _ = args.output
    analyzer.analyze()


if __name__ == "__main__":
    main()
