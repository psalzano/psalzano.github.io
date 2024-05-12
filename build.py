from pathlib import Path
from glob import glob
import os
import re

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
  template = get_file_content('src/template.html')
  return template

def load_part(part_name: str):
  filename = 'src/parts/' + part_name.lower() + '.html'
  if os.path.exists(filename):
    template = get_file_content(filename)
    return template
  return ''

def get_placeholders(template: str):
  ph = re.findall("\{[A-Za-z0-9\_]+\}", template)
  return ph

def process_file(template: str, filename: str, placeholders=[]):
  if not filename.startswith('src/'):
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
      html = html.replace(itm, part)
  
  # scrivere il contenuto finale nel target file
  put_file_content(target_file, html)

def build():
  template = load_template()
  placeholders = get_placeholders(template)
  #print(repr(placeholders))

  for filename in glob('src/**/*.html', recursive=True):
    base_name = os.path.basename(filename)
    if base_name == 'template.html': continue
    if filename.startswith('src/parts'): continue
    print("Processing ", filename)
    process_file(template, filename, placeholders)
  pass

if __name__ == "__main__":
  build()  
