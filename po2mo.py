import os
from loguru import logger
import polib
import PySimpleGUI as sg


layout = [
    [sg.Text('Path to .po directory:')],
    [sg.InputText(do_not_clear=True, key='_PATH_'), sg.FolderBrowse()],
    [sg.Button('Convert'), sg.Button('Exit')]
]

def get_all_po_paths(dirpath):
    """recursively search for po file in directory"""
    for (dirpath, dirname, filename) in os.walk(dirpath):
        if dirpath and filename:
            for po_name in filename:
                if po_name.endswith(".po"):
                    po_path = os.path.join(dirpath, po_name)
                    yield po_path

def convert_po_to_mo(po_path):
    try:
        po = polib.pofile(po_path)
    except Exception as err:
        msg = f"Error on converting {po_path} to mo file: {err}"
        logger.info(msg)
        sg.Print(msg)
    else:
        po.save_as_mofile('.'.join((po_path[:-3], 'mo')))
        msg = f"Successfully converting {po_path} into mo file"
        logger.info(msg)
        sg.Print(msg)


def main_window():
    window = sg.Window('po2mo converter').Layout(layout)

    while True:                 # Event Loop
        event, values = window.Read()
        print(event, values)
        if event is None or event == 'Exit':
            break
        if event == 'Convert':
            dirpath = values.get('_PATH_')
            logger.info(dirpath)
            po_paths = get_all_po_paths(dirpath)
            counter = 1
            # max_value = len(po_paths)
            for po_path in po_paths:
                convert_po_to_mo(po_path)
                # sg.OneLineProgressMeter('Convertion progress', counter+1, max_value, 'key', f'Convert to binary')
            logger.info("DONE!")
            sg.Print("DONE!")

    window.Close()

if __name__ == "__main__":
    main_window()

