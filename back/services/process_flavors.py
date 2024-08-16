from flask import current_app
import os
import openpyxl


def extract_flavors(file):
    file_path = os.path.join(current_app.config.get('UPLOAD_FOLDER','somefile.txt'), file.filename)# type: ignore
    file.save(file_path)
    workbook = openpyxl.load_workbook(os.path.join(current_app.config.get('UPLOAD_FOLDER', 'somefile.txt'), file.filename))# type: ignore
    sheet = workbook.worksheets[0]
    
    flavors = []
    for cell in sheet['B'][1::]:
        if isinstance(cell.value, str) and cell.value.startswith('x86'):
            flavor = cell.value.split(' | ')[2]
            flavors.append({'flavor': flavor, 'row': cell.row})
    return flavors