from genericpath import isdir
from pathlib import Path
from glob import glob
import shutil
import os
import re
from bs4 import BeautifulSoup

def get_file_content(filename: str):
  f = open(filename,'r')
  content = f.read()
  f.close()
  return content

def put_file_content(filename: str, output: str):

  # leggiamo il nome del file di destinazione.
  # estraiamo la directory target richiesta
  # se non esiste, la creiamo
  dir_name = os.path.dirname(os.path.abspath(filename))
  if not os.path.exists(dir_name): 
    os.makedirs(dir_name)

  f = open(filename, 'w')
  f.write(output)
  f.close()

def load_template():
  template = get_file_content('src' + os.path.sep +'template.html')
  return template

def load_part(part_name: str):
  
  filename =  str.join(os.path.sep,["src", "parts", part_name.lower() + '.html'])
  if os.path.exists(filename):
    template = get_file_content(filename)
    return template
  return ''

def get_placeholders(template: str):
  ph = re.findall("\{[A-Za-z0-9\_]+\}", template)
  return ph

def process_navbar(navbar: str, page: str):
  soup = BeautifulSoup(navbar, 'html.parser')

  page = str.replace(page, os.path.sep,'/')

  element = soup.find("a", attrs={"href": "/"+page})

  if element:
    element["class"] = element.get('class', []) + ['active']
    #if page.count("/") == 1:
    #  parent = element.find_parent('li')
    #  parent["class"] = parent.get('class', []) + ['active']
    #else:
    #  element["class"] = element.get('class', []) + ['active']
    
    return soup.prettify()
  
  return navbar

def process_file(template: str, filename: str, placeholders=[]):
  print (f"> {filename}")
  if not filename.startswith('src'+os.path.sep):
    print(f">> Skipping {filename}")
    return  
  target_file = filename[4:]
  
  html = template
  # leggere il contenuto del file "filename"
  content = get_file_content(filename)
  
  # per ciascun placeholder stabilire se leggere il file da "parts"
  # assemblare il contenuto finale
  for itm in placeholders:
    if itm == '{CONTENT}':
      html = html.replace(itm, content)
    else:
      ph = str(itm).removeprefix('{').removesuffix('}').lower()
      part = load_part(ph)
      if itm == '{NAVBAR}':
        part = process_navbar(part, target_file)

      html = html.replace(itm, part)
  
  # scrivere il contenuto finale nel target file
  target_file = "dist" + os.path.sep + target_file
  put_file_content(target_file, html)

def build():
  template = load_template()
  placeholders = get_placeholders(template)
  #print(repr(placeholders))

  search_pattern = str.join(os.path.sep,['src','**','*.html'])
  # 'src' + os.path.sep+ '**' + os.path.sep+ '*.html'
  for filename in glob(search_pattern, recursive=True):
    
    print(f"{filename}")
    base_name = os.path.basename(filename)
    if base_name == 'template.html': continue
    if filename.startswith('src'+os.path.sep+'parts'): continue
    print("Processing ", filename)
    process_file(template, filename, placeholders)
    
    assets = ['css','imgs','scripts','fonts']
    for asset in assets:
      if os.path.isdir(asset):
        target_asset = str.join(os.path.sep,["dist",asset])
        if os.path.isdir(target_asset):
          shutil.rmtree(target_asset)

        shutil.copytree(asset, target_asset)

if __name__ == "__main__":
  build()  
