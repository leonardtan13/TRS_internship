
import re
from docx import Document

def generate_doc(inputf, project):
        doc = Document(inputf) 
        for p in doc.paragraphs:
            txt = p.text
            pattern = re.compile(r'.*\{\{(\w+)\}\}.*')
            matches = pattern.finditer(txt)
            modded = 0
            for m in pattern.finditer(txt):
                key = m.group(1)
                if key in project and isinstance(project[key],str):
                    txt = txt.replace('{{{{{}}}}}'.format(key), project[key])
                    modded = 1
            if modded == 1:
                p.text = txt
        return doc