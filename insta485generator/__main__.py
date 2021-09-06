import click
import os
import json
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
@click.argument('INPUT_DIR', required=True, type=click.Path(exists=True))
@click.option('-o', '--output', 'PATH', help="Output directory")
@click.option('-v', '--verbose', help="Print more output")

def main(PATH, verbose, input_dir):
    """Fetch JSON, URL, & JINJA from input_dir"""
    click.echo(input_dir)
    print(PATH)
    #load the json data:
    jsonFile = open(input_dir + "/" + "config.json", "r")
    data = json.load(jsonFile)
    print(data)
    #load the jinja template:
    env = Environment(
    loader=PackageLoader(input_dir),
    autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template("index.html")
    #print(template.render(the="variables", go="here"))
    #Extract the url from the json dictionary:
    #Not sure when we are suppose to cut off the forward slash..
    url = data[0]["url"]
    #print(url)
    """Serve JSON & JINJA, to ${input_dir}/url """
    target_path = input_dir + '/html' if PATH == None else PATH
    print(target_path)
    #Store the jinja Template in the target_path:
    htmlOutput = template.render(data[0].get("context"))
    #print(htmlOutput)
    os.mkdir(target_path)
    with open(target_path + "/index.html", "w") as file:
        file.write(htmlOutput)

if __name__ == "__main__":
    main()