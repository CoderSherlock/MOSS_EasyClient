#!/usr/bin/python


#######################################################
#   FileManager.py
#   Creator: Pengzhan Hao
#   
#   Used for manage all students files, including
#       names, major langaues, all detectable file
#       names, and other infomations
#######################################################




import os
import sys
import glob


def remove_undetectable_files(files):                                       # Unit test passed: 2017-09-18
    """ 
    Remove undetectable files using suffix
    (list files)
    none
    """
    detectable_type = ['h','c','cpp','hpp','java','py','cs','vb','js']      # TODO: need to update
    for i in files:
        if i.split('.')[-1] not in detectable_type:
            files.remove(i)

class student:
    sname = ""              # Student name
    lang  = ""              # Student preferred language
    grade = 100             # Student's grade
    rootd = ""              # Root directory of the student
    files = []              # Student's project files

    def __init__(self, name, rootd):
        """
        Init a student
        (str name, str rootd)
        none
        """
        self.sname = name
        self.rootd = rootd
        self.lang = ""
        self.files = []
        
        # add all files
        for filename in glob.glob(os.path.join(os.path.abspath(self.rootd), '**/*.*'), recursive=True):
            self.files.append(filename[len(os.path.abspath(self.rootd))+1:])

        # remove undetectable files
        remove_undetectable_files(self.files)

        # guess the preferred languages
        tempRes = {}
        for f in self.files:
            suffix = f.split('.')[-1]
            if suffix in tempRes:
                tempRes[suffix] += 1
            else:
                tempRes[suffix] = 1

        tempLang = ""
        if len(tempRes) != 0:
            tempLang = max(tempRes, key=tempRes.get)

        
        if tempLang == "h":
            tempLang = "c"
        if tempLang == "hpp":
            tempLang = "cpp"
        self.lang = tempLang

    def __str__(self):
        """
        Return string of class
        ()
        string
        """
        return "{0:<9.9} {1:5s} {2:3d}".format(self.sname, self.lang, self.grade)

    def getFiles_by_name(self, keyword):
        """
        Return file list by filtering keyword
        (str keyword)
        List files
        """
        tmpFileList = []
        for i in self.files:
            if keyword == i:
                tmpFileList.append(os.path.join(self.rootd, i))
        return tmpFileList 




class aclass:
    students = []           # Student of the class
    lang_ratio = {}         # Ratio of language usage
    root = ""              # Root directory of this class

    def __init__(self, root):
        """
        Init the class with the root name
        (str root)
        none
        """
        self.students = []
        self.lang_ratio = {}
        self.root = root

        # statstic all students
        for root, dirs, files in os.walk(self.root):
            for sname in dirs:
                tmpStudent = student(sname, os.path.join(os.path.abspath(root), sname))
                self.students.append(tmpStudent)

                # get first-preferred language ratio 
                if tmpStudent.lang in self.lang_ratio:
                    self.lang_ratio[tmpStudent.lang] += 1
                else:
                    self.lang_ratio[tmpStudent.lang] = 1
            break

    def getFiles_by_name(self, keyword, lang):
        """
        Return all file list in same languae of all students
        (str keyword, str lang)
        List files
        """

        tmpFileList = []
        for s in self.students:
            if s.lang == lang:
                tmpFileList += s.getFiles_by_name(keyword)
        return tmpFileList






if __name__ == "__main__":
    #  s = student("ab","../../CS550-Grading/solutions/avelank1")
    #  print(s)

    c = aclass("../../CS550-Grading/solutions")
    #  print(c.lang_ratio)
    print(len(c.getFiles_by_name("proc.c", "c")))
    for i in c.students:
        print(i)
