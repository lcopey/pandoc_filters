import os
import re
import sys
from typing import Callable

import click


@click.command()
@click.argument(
    "file",
)
def main(file):
    return sys.stdout.write(
        Str.from_file(file).pipe(replace_wikilinks_with_markdown_links)
    )


def pandoc_exec(
    _in: str, _f: str, _t: str, _filter: str, _out: str, _resource: str = None
):
    os.system(
        f"pandoc {_in} -f {_f} -t {_t} --filter={_filter} --resource-path={_resource} -s -o {_out}.{_t}"
    )


class Str(str):
    @classmethod
    def from_file(cls, filepath: str) -> "Str":
        with open(filepath, mode="r") as f:
            text = f.read()
        return Str(text)

    def pipe(self, func: Callable[[str], str]) -> "Str":
        return Str(func(self))


def replace_wikilinks_with_markdown_links(text: str) -> str:
    pattern = r"!\[\[(?P<text>.*?)]]"
    return re.sub(pattern, lambda x: f"![]({x.group('text')})", text)


if __name__ == "__main__":
    main()
