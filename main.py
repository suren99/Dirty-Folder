import os
import shutil
import sys

to_be_cleaned = "/Users/suren/a"
Formats = {}

class cleaner:
    def __init__(self):
        self.table={}
        self.configs={}

    def add_formats(self,location,formats):
        for each_format in formats:
            if each_format in self.table:
                continue
            else:
                self.table[each_format] = location

    def clean(self):
        moved = []
        black_list = set()
        for (dirpath, dirnames, filenames) in os.walk(self.configs["-name"]):
            if dirpath != to_be_cleaned:
                if dirpath[:dirpath.rfind('/')] in black_list:
                    black_list.add(dirpath)
                    continue
                if '-r' not in self.configs:
                    choice = raw_input('Descend into directory : '+dirpath+" ? ")
                    if choice == 'n':
                        black_list.add(dirpath)
                        continue
            for filename in filenames:
                fname, extension = os.path.splitext(filename)
                lower = extension.lower() in self.table
                upper = extension.upper() in self.table
                src = dirpath+"/"+filename
                if lower : dstl = self.table[extension.lower()]+"/"+filename
                if upper : dstu = self.table[extension.upper()]+"/"+filename
                if lower:
                    if not os.path.exists(self.table[extension.lower()]):
                        os.makedirs(self.table[extension.lower()])
                    shutil.move(src, dstl)
                    moved.append((src,dstl))
                    print "Sweeping from " +src+" to "+dstl
                elif upper:
                    if not os.path.exists(self.table[extension.upper()]):
                        os.makedirs(self.table[extension.upper()])
                    shutil.move(src, dstu)
                    moved.append((src,dstu))
                    print "Sweeping from " +src+" to  "+ dstu
        return moved

def wrong_usage():
        print "Usage : python main.py [-r | -a | -d | -w] [-name] [directory]"

def arg_check(arg):
        options = ['-r', '-a', '-d', '-w']
        if len(arg) == 0:
            return 0
        idx = -1
        if "-name" in arg:
            idx = arg.index("-name")
        if idx != -1:
            if (idx + 1) >= len(arg): return -1
            c.configs["-name"] = arg[idx + 1]
            del arg[idx]
            del arg[idx]
        res = [False if (x[0] != '-' or x not in options) else True for x in arg]
        if False in res: return -1
        s = set()
        for x in arg:
            c.configs[x] = 1
        if idx != -1 and len(c.configs) > 2:
            return -1
        if '-a ' in c.configs and len(arg) > 1:
            return -1
        if '-d' in c.configs and len(arg) > 1:
            return -1
        if '-w' in c.configs and len(arg) > 1:
            return -1

if __name__ == '__main__':
    arg = ""
    c = cleaner()
    c.configs["-name"] = to_be_cleaned
    if arg_check(sys.argv[1:]) == -1:
        wrong_usage()
        sys.exit()
    if '-a' in c.configs:
        extensions = raw_input("Input the extensions separated by commas: ")
        Dest = raw_input("Input the Destionation folder(Absolute path): ")
        if Dest[len(Dest)-1] != '/':
            Dest += "/"
        fp = open("map.txt","a")
        extensions = ",".join("."+each for each in extensions.split(","))
        fp.write(Dest+":"+extensions+"\n")
        fp.close()
    elif '-w' in c.configs:
        print "Rewinding the previous sweepings\n"
        fp = open("rewind.txt", "r")
        lines = fp.readlines()
        if len(lines) == 0:
            print "No previous sweepings found"
        for each_line in lines:
            split = each_line.replace("\n","").split("$$$")
            shutil.move(split[1], split[0])
            print "Rewinding the sweeping "+split[1] +" to "+split[0]
        fp.close()
        open("rewind.txt","w").close()
        print "Done"
    elif '-d' in c.configs:
        fp = open("map.txt", "r")
        lines = fp.readlines()
        fp.close()
        for cnt,line in enumerate(lines):
            print str(cnt + 1)+". "+line
        choices = raw_input("Input the indices separated by commas to delete: ").split(",")
        fp = open("map.txt", "w")
        for cnt, line in enumerate(lines):
            if str(cnt + 1) not in choices:
                fp.write(line)
        fp.close()
    else:
        if c.configs["-name"] == to_be_cleaned:
            print "Cleaning directory not mentioned, choosing the default directory : " + to_be_cleaned +"\n"
        else:
            print "Cleaning up the directory : "+c.configs['-name']+"\n"
        fp = open("map.txt", "r")
        for each_line in fp.readlines():
            dir_ext = each_line.split(":")
            if len(dir_ext) != 2:
                continue
            Formats[dir_ext[0]] = dir_ext[1].replace("\n","").split(",")
        fp.close()
        for location,formats in Formats.items():
            c.add_formats(location,formats)
        moved = c.clean()
        fp = open("rewind.txt", "w")
        for each in moved:
            fp.write(each[0]+"$$$"+each[1]+"\n")
        fp.close()
        print "Done"
