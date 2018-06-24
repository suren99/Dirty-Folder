import os
import shutil
import sys

to_be_cleaned = "/Users/suren/Downloads/"
Formats = {}

class cleaner:
    def __init__(self):
        self.table={}
        
    def add_formats(self,location,formats):
        for each_format in formats:
            if each_format in self.table:
                continue
            else:
                self.table[each_format] = location

    def clean(self,source_dir):
        moved = []
        for (dirpath, dirnames, filenames) in os.walk(source_dir):
            for filename in filenames:
                fname, extension = os.path.splitext(filename)
                lower = extension.lower() in self.table
                upper = extension.upper() in self.table
                src = dirpath+"/"+filename
                if lower : dstl = self.table[extension.lower()]+"/"+filename
                if upper : dstu = self.table[extension.upper()]+"/"+filename
                if (upper or lower) and not os.path.exists(self.table[extension.lower()]):
                    os.makedirs(self.table[extension.lower()])
                if lower:
                    shutil.move(src, dstl)
                    moved.append((src,dstl))
                    print "Sweeping from " +src+" to "+dstl
                elif upper:
                    shutil.move(src, dstu)
                    moved.append((src,dstu))
                    print "Sweeping from " +src+" to  "+ dstu
        return moved

if __name__ == '__main__':
    arg = ""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    if arg == "--add":
        print "Input the extensions separated by commas: "
        extensions = raw_input()
        print "Input the Destionation folder(Absolute path):"
        Dest = raw_input()
        if Dest[len(Dest)-1] != '/':
            Dest += "/"
        fp = open("map.txt","a")
        extensions = ",".join("."+each for each in extensions.split(","))
        fp.write(Dest+":"+extensions+"\n")
        fp.close()
    elif arg == "--rewind":
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
    else:
        if len(arg) == 0:
            print "Cleaning directory not mentioned, choosing the default directory : " + to_be_cleaned +"\n"
        else:
            to_be_cleaned = arg
            print "Cleaning up the directory : "+to_be_cleaned+"\n"
        fp = open("map.txt", "r")
        for each_line in fp.readlines():
            dir_ext = each_line.split(":")
            if len(dir_ext) != 2:
                continue
            Formats[dir_ext[0]] = dir_ext[1].replace("\n","").split(",")
        fp.close()
        c = cleaner()
        for location,formats in Formats.items():
            c.add_formats(location,formats)
        moved = c.clean(to_be_cleaned)
        fp = open("rewind.txt", "w")
        for each in moved:
            fp.write(each[0]+"$$$"+each[1]+"\n")
        fp.close()
        print "Done"
    




                    





        
