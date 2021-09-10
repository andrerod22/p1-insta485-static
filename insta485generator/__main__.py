"""Title: p1-insta485-static."""

import sys
import json
from pathlib import Path
from distutils.dir_util import copy_tree
import click
from jinja2 import Environment, select_autoescape, FileSystemLoader
# Build static HTML site from directory of HTML templates and plain files.


@click.command()
@click.option('-o', '--output', help="Output directory.", type=Path)
@click.option(
    '-v', '--verbose', help="Print more output.",
    is_flag=True, type=bool)
@click.argument('INPUT_DIR', required=True, type=click.Path(exists=True))
def main(output, verbose, input_dir):
    """Templated static website generator."""
    input_path = Path(input_dir)
    # ERROR HANDLING
    output_root = None if output is None else output
    if output_root and Path.exists(output_root):
        click.echo("Path already exists")
        sys.exit(1)
    # input_dir error handled by click
    # Check if output_dir exists:
    # Valid Json File:
    # Valid Jinja Template:
    # Fetch JSON, URL, & JINJA from input_dir
    # templates_dir = input_path/"templates"
    env = Environment(
        loader=FileSystemLoader(str(input_path/"templates")),
        autoescape=select_autoescape(['html', 'xml']),)
    # json_dir = input_path/"config.json"
    with open(input_path/"config.json") as json_file:
        data = json.load(json_file)
        output_html = input_path/"html" if output_root is None else output_root
        Path.mkdir(output_html, parents=True)
        # css_path = input_path/"static"
        if Path.exists(input_path/"static"):
            copy_tree(str(input_path/"static"), str(output_html))
            if verbose:
                click.echo(
                    "Copied" + " " +
                    input_dir + "/" + "static" + " -> "
                    + str(output_html))

        # Serve JSON & JINJA, to ${input_dir}/url or output_dir"""
        for key in data:
            url = key["url"]
            url = url.lstrip("/")
            template = env.get_template(key["template"].lstrip("/"))
            generated_html = template.render(key["context"])
            target = output_html/url/"index.html"
            if not Path.exists(output_html/url):
                Path.mkdir(output_html/url, parents=True)
            with target.open("w") as file:
                file.write(generated_html)
                if verbose:
                    click.echo(
                        "Rendered " +
                        key["template"] + " -> "
                        + str(target))


if __name__ == "__main__":
    main()
