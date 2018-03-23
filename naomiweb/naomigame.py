import io
import os

class NAOMIGame(object):

    def __get_names(self):
        'Get game names from NAOMI rom file.'
        try:
            fp = open(self.filename, 'rb')
            fp.seek(16, 0)
            company = fp.read(32).decode('utf-8').strip(' ').upper()
            if "DARKSOFT" in company or company == "WWW.ARCADEMODBIOS.COM":
                self.isAtomiswave = True
                fp.seek(65328, 0)
                name = fp.read(32).decode('utf-8').strip(' ');
            else:
                fp.seek(48, 0)
                name = fp.read(32).decode('utf-8').strip(' ')
            
            # cleanup name
            name = name.replace('-', '')
            name = name.replace('#', '')
            print(name)

            # remove potential "JAPAN VERSION" suffix
            fields = name.split('JAPAN')
            name = fields[0].strip()
            
            # TODO remove region option ?           
            for key in self.name.keys():
                self.name[key] = name

            fp.close()
        except Exception as e:
            print("__get_names(): Error reading names from" + self.filename)
            print(e) 

    def __init__(self, filename):
        self.name = {'japan': '',
                'usa': '',
                'euro': '',
                'asia': '',
                'australia': ''}
        self.filename = filename
        self.isAtomiswave = False
        self.__get_names()
        self.screenshots = list()
        
        # main screenshot
        basename = "./static/screenshots/" + self.name['japan']
        file = basename + ".png"
        if not os.path.exists(file):
            file = "./static/screenshots/no_screenshot.png"
        self.screenshots.append(file.replace(' ', '%20'))
        
        # additional screenshots
        for i in range(2):
            file = basename + "_" + str(i) + ".png"
            if os.path.exists(file):
                self.screenshots.append(file.replace(' ', '%20'))
        
        # rom size
        try:
            self.size = os.stat(filename).st_size
        except Exception:
            self.size = 0

    def __hash__(self):
        return hash((self.name['japan'], self.filename, self.size)) & 0xffffffff

def is_naomi_game(filename):
    'Determine (loosely) if a file is a valid NAOMI netboot game'
    try:
        fp = open(filename, 'rb')
        header_magic = fp.read(5).decode('utf-8')
        fp.close()
        return header_magic == 'NAOMI'

    except Exception:
        print("is_naomi_game(): Could not open " + filename)
        return False

def get_game_name(filename):
    'Read game name from NAOMI rom file.'
    try:
        fp = open(filename, 'rb')
        fp.seek(0x30, os.SEEK_SET)
        filename = fp.read(32).decode('utf-8').rstrip(' ')
        fp.close()
        return filename

    except Exception:
        print("get_game_name(): Error reading game name.")
        return ''
