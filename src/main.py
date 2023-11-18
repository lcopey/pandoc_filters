import panflute as pf
import re


def action(item: pf.Element, doc: pf.Doc):
    if isinstance(item, pf.Str):
        if match := re.match(r'\[\[(.*?)]]', item.text):
            return pf.Str(f'[]({match.group(1)})')


def main(doc: pf.Doc = None):
    pf.run_filter(action, doc=doc)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
