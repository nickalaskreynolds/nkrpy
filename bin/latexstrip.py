r"""
This is a script to format and package a scientific paper written in latex for
upload to the journal (using aastex) and the arXiv (assuming emulateapj).

It will make numbered copies of all the figures, strip out latex comments,
copy in the compiled BibTex biliography, and combine any \input latex sources
into a single tex file.

Run this script from inside a directory with a compiled paper with the syntax:
python NESsubmit.py myfile.tex outputdir

The outputdir is the directory where the program output will be written.
If the directory already exists, it will be overwritten.

----

Written by Nathan Sanders, 2012
https://www.cfa.harvard.edu/~nsanders/index.htm

If you have comments or questions about this script, please leave comments at:

http://astrobites.com/2012/08/05/how-to-submit-a-paper/

or submit bug reports at:

https://github.com/nesanders/NESsubmit/issues

"""
from __future__ import print_function

import re
import os
import sys

print(sys.argv)
if len(sys.argv) > 1:
    mainfile = sys.argv[1]
else:
    print("You must specify a main tex file")
if len(sys.argv) > 2:
    outdir = sys.argv[2]
else:
    outdir = 'submit'

# Clean directory
os.system('rm -rf '+outdir)
os.system('mkdir '+outdir)

# start figure numbering at 1
global fnum
fnum = 0


def ostrip(thefile):
    """
    Function to open a tex file and strip it of comments
    """
    outlines = []
    with open(thefile, 'r') as f:
        for line in f:
            if line[0] != '%':
                if '%' in line:
                    if r'\%' in line or line[-1] == '%':
                        outlines.append(line)  # these are not real comments
                    else:
                        outlines.append(line.split(' %')[0]+'\n')
                else:
                    outlines.append(line)
    return outlines


def isfigure(line):
    """True if this looks like a figure line.
    """
    return re.search("(includegraphics|plotone|plottwo)", line)


def findfigure(name):
    """Return name of image file in current working directory with
    this root"""
    found = None
    if "." in name:
        if os.path.exists(name):
            found = name
    elif "." not in name:
        for suffix in (".pdf", ".eps", ".ps", ".JPG", ".jpg", ".png"):
            testfile = name + suffix
            if os.path.exists(testfile):
                found = testfile
    if found is None:
        raise RuntimeError("Could not find image file {}".format(name))
    return found, os.path.splitext(found)[-1]


def outfigname(num, ext, char=""):
    """Form output file name."""
    return "f{}{}{}".format(num, char, ext)


def dofigure(line):
    """
    Function to take care of figures
    """
    global fnum
    if 'onlineonlycolor' not in line:
        fnum += 1
    print('Line:', line)
    locate = re.search(r"\{([\w\-\.\/]+)\}", line)
    if not locate:
        raise RuntimeError("Could not find image in line '{}'".format(line))
    imagetext = locate.group(1)
    imname, ftype = findfigure(imagetext)
    if 'plottwo' in line:
        imname2 = line.split('{')[2].split('}')[0]
        # print name and number
        print(fnum+'a', imname)
        print(fnum+'b', imname2)
        _, subname = os.path.split(imname)
        _, subname2 = os.path.split(imname2)
        ftype = os.path.splitext(subname)
        # rename with number if desired
        subname = outfigname(fnum, ftype, char="a")
        outname = os.path.join(outdir, subname)
        subname2 = outfigname(fnum, ftype, char="b")
        outname2 = os.path.join(outdir, subname2)
        # copy over
        os.system("cp "+imname+" "+outname)
        os.system("cp "+imname2+" "+outname2)
        # write out plot string
        newline = line.replace(imagetext, subname)
        newline = newline.replace(imname2, subname2)
    else:
        # print name and number
        print(fnum, imname)
        _, subname = os.path.split(imname)
        # rename with number if desired
        subname = outfigname(fnum, ftype)
        outname = os.path.join(outdir, subname)
        # copy over
        os.system("cp "+imname+" "+outname)
        # write out plot string
        newline = line.replace(imagetext, subname)
    return(newline)


# do includes - only goes one level in
mainlines = ostrip(mainfile)
outlines = []
for line in mainlines:
    if r'\input' in line or r'\include' in line:
        includestr = r'\input'
        if r'\include' in line:
            includestr = r'\include'
        incfile = line.split('{')[1].split('}')[0]
        # if there is no extension, assume it is a .tex
        if len(incfile.split('.')) == 1:
            incfile_e = incfile+'.tex'
        else:
            incfile_e = incfile
        # Append any text before the include
        outlines.append(line.split(includestr+'{'+incfile+'}')[0])
        # Append each line from the input file
        for subline in ostrip(incfile_e):
            # rotate long tables
            # if 'scriptsize' in subline: outlines.append(r'\rotate'+'\n')
            if isfigure(subline):
                outlines.append(dofigure(subline))
            else:
                outlines.append(subline)
        # Append any text after the include
        outlines.append(line.split(includestr+'{'+incfile+'}')[1])
    # don't emulateapj
    elif '{emulateapj}' in line:
        outlines.append(r'\documentclass[manuscript]{aastex62}'+'\n')
    elif r'\LongTables' in line:
        outlines.append('')
    # input bibliography
    elif r'\bibliography{' in line:
        bibname = line.split('{')[1].split('}')[0].replace('.bib', '')+'.bbl'
        biblines = ostrip(bibname)
        for subline in biblines:
            outlines.append(subline)
    # figures
    elif isfigure(line):
        outlines.append(dofigure(line))
    else:
        outlines.append(line)


# Write out ApJ version
outfile = os.path.join(outdir, 'apj.tex')
with open(outfile, 'w') as f:
    for line in outlines:
        # don't need two-column deluxetables for apJ
        line = line.replace('deluxetable*', 'deluxetable')
        if 'aas_macros' not in line:
            print(line, file=f, end='')

# Write out arXiv version
outfile = os.path.join(outdir, 'arxiv.tex')
with open(outfile, 'w') as f:
    for line in outlines:
        if '{aastex}' in line:
            newline = r'\documentclass{emulateapj}'+'\n'
        else:
            newline = line
        print(newline, file=f, end='')

# tar up
os.chdir(outdir)
os.system('tar --exclude arxiv.tex -czf '+'ApJ.tar.gz *.tex f[1-9]*.*')
# readme
with open("README", "w") as r:
    print("For ApJ, simply upload the tarball.  For the arXiv, upload "
          "all the figures plus the arxiv.tex file, NOT the apj.tex", file=r)
os.chdir('..')
