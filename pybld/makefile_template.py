"""Template text for PyMake"""

gccTemplate = """

from PyBld import *
Debug = True # <-- set it to True to enable more debugging messages
# HighlightErrors = True # To enable the highliter
HighlightWarnings = True # To enable the highliter
HighlightNotes = True # To enable the highliter

# Custom Highlighting using regular expressions
hl(regx(r'error:.+'), colors.IRed)
# hl(regx(r'expression'), colors.IGreen, colors.On_Cyan)
# hl('c', colors.IGreen)


CC = 'gcc'
CFLAGS = '-g -O2 -std=c99'
LINKFLAGS = ''

executable = 'a.out'
BUILDdir = './Build/'
src_files = find(root='./', filter='*.c')
obj_files = replace(src_files, '.c', '.o')
obj_files = retarget(obj_files, BUILDdir, '')


@target
def all(Tlink): # depends on Target link
  printcolor('Build Succeeded', colors.IGreen)
  return True

@target
def Tlink(Tcompile): # depends on Target compile
  return link(CC, LINKFLAGS, obj_files, executable)

@target
def Tcompile(src_files): # depends on srource files
  return compile(CC, CFLAGS, src_files, obj_files)


@target
def clean():
  retV = run(eval('rm -r $(BUILDdir)'))
  retV = run(eval('rm $(executable)'))
  return True
"""
