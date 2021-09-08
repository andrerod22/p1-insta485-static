import sys
import json
from pathlib import Path
from distutils.dir_util import copy_tree
import click
from jinja2 import Environment, PackageLoader, select_autoescape, Template


"""Build static HTML site from directory of HTML templates and plain files."""
#    Implement the following in main:
# 1. Handle command line arguments using the click library
# 2. Render the provided templates and write them to output 
#    files and create all the necessary directories and files needed to do this
# 3. Copy over a static directory if it is provided
# 4. Handle errors
#@click.command(context_settings=dict(help_option_names=['-h', '--help']))

@click.command()
@click.option('-o', '--output', help="Output directory.", type=Path)
@click.option('-v', '--verbose', help="Print more output.", is_flag=True, type=bool)
@click.argument('INPUT_DIR', required=True, type=click.Path(exists=True))
def main(output, verbose, input_dir):
    """Templated static website generator."""
    #ASK: Do we need to lstrip path object types?
    #Path(output.lstrip("/"))
    input_path = Path(input_dir)
    output_root = None if output == None else output
    """ERROR HANDLING"""
    #input_dir error handled by click
    #Check if output_dir exists:
    if output_root and Path.exists(output_root):
        click.echo("Path already exists")
        sys.exit(1)

    #Valid Json File:

    #Valid Jinja Template:

    #Valid URL:

    """Fetch JSON, URL, & JINJA from input_dir"""
    #load the json data:
    #mkae sure to loop through each dictionary!
    json_dir = input_path/"config.json"
    jsonFile = open(json_dir)
    data = json.load(jsonFile)
    env = Environment(
    loader=PackageLoader(input_dir),
    autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template("index.html")
    #Extract the url from the json dictionary:
    #Not sure when we are suppose to cut off the forward slash..
    """Serve JSON & JINJA, to ${input_dir}/url or output_dir"""
    url = data[0]["url"]
    url = url.lstrip("/")
    output_html = input_path/"html" if output_root == None else output_root
    target = output_html/url/"index.html"
    #Store the jinja Template in the target_path:
    generatedHTML = template.render(data[0].get("context"))
    #get an error if I don't put in mode='w'
    #ASK PIAZZA OR OH
    #Generate HTML File:
    #breakpoint()
    Path.mkdir(output_html)
    with target.open("w") as file:
        file.write(generatedHTML)
    #Check if INPUT_DIR has a static folder:
    cssPath = input_path/"static"/"css"
    if Path.exists(cssPath):
        Path.mkdir(output_html/"css")
        if Path.exists(cssPath/"style.css"):
            Path(output_html/"css"/"style.css").touch()
            copy_tree(str(cssPath), str(output_html/"css"))
    
    #If verbose enabled print state of index & static:
    if verbose:
        click.echo("Copied" + " " + input_dir + "/" + "static" + " -> " + str(output_html))
        click.echo("Rendered index.html -> " + str(target))


if __name__ == "__main__":
    main()