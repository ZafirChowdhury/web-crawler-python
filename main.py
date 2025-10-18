import sys

from crawl import get_html, extract_page_data

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {sys.argv[1]}")

    try:
        html = get_html(sys.argv[1])
        print(html)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
