from wardoff import argparser


def main():
    args = argparser().parse_args()
    analyzer = args.project
    out_file = args.output
    analyzer.analyze()


if __name__ == "__main__":
    main()
