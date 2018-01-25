import os
import shutil


Formats = {"/Users/suren/Movies/" : [".webm",".mkv",".flv",".vob",".ogv",".ogg",".drc",".gif","gifv",".mng",".avi",".mov",".qt",".wmv",".yuv",".rm",".rmvb",".asf",".amv",".mp4",".m4p",".m4v",".mpg",".mp2",".mpeg",".mpe",".mpv",".mpg",".mpeg",".m2v",".m4v",".svi",".3gp",".3g2",".mxf",".roq",".nsv",".flv",".f4v",".f4p",".f4a",".f4b"],
       "/Users/suren/Songs/"   : [".mp3",".3gp",".aa",".aac",".aax",".act",".aiff",".amr",".ape",".au",".awb",".dct",".dss",".dvf",".flac",".gsm","iklax",".ivs",".m4a",".m4p",".mmf",".mp3",".mpc",".msv",".off",".oga",".mogg",".opus",".ra",".rm","sln",".tta","vox",".wma",".webm",".8svx"],
       "/Users/suren/Torrents/" : [".torrent"],
       "/Users/suren/Pictures/" : [".tif",".jpg",".png"]
}

to_be_cleaned = "/Users/suren/Downloads/"

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
        for (dirpath, dirnames, filenames) in os.walk(source_dir):
            for filename in filenames:
                fname, extension = os.path.splitext(filename);
                if extension.lower() in self.table:
                    shutil.move(dirpath+"/"+filename, self.table[extension.lower()]+"/"+filename)
                elif extension.upper() in self.table:
                    shutil.move(dirpath+"/"+filename, self.table[extension.upper()]+"/"+filename)


if __name__ == '__main__':
    c = cleaner()
    for location,formats in Formats.items():
        c.add_formats(location,formats)
    c.clean(to_be_cleaned)
    




                    





        
