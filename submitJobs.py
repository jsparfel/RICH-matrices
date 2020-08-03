#!/usr/bin/python

# SUBMIT SEVERAL RICH MATRICES JOBS TO BATCH

# usage: submitJobs.py [-h] [-e EXEDIR] [-s EXESCRIPT] [-i INDIR] [-o OUTDIR]
#                      [-f] [-N] [-H] [-q]
#                      [periodFile]

# Submit several Rich matrices jobs to batch

# positional arguments:
#   periodFile    D = "periods.dat"

# optional arguments:
#   -h, --help    show this help message and exit
#   -e EXEDIR     Exe dir name. D = "~/analyse/nicolas"
#   -s EXESCRIPT  Batch script "(analySIDIS|acceptance).csh". D =
#                 "analySIDIS.csh"
#   -i INDIR      Input dir name. D = "(trees|MCs)"
#   -o OUTDIR     Output dir name. D = "(rawmult|acceptance)"
#   -f, --force   Force even if output already exists
#   -N, --NOP     No OPeration
#   -H, --HELP    More help
#   -q, --quiet   Less verbosity

# NOTES:
# This is limited at present limited to:
# - fit_table plots ; fit_table fit

from __future__ import print_function
import sys, os, argparse, re

exeScripts =   [ "fit_table_plots.csh",   "fit_table_fit.csh" ]
exeNames =     [ "fit_table", "fit_table" ]
exeOptions =   [ "plots", "fit" ]
inDirs =       [ "RICH", "plots"]
outDirs =      [ "plots",          "fit" ]
# Defaults
DExeDir = "~/rich_matrices/normal"
DExeScript = exeScripts[0]
DInDir = inDirs[0]
DOutDir = outDirs[0]
# Lists of outputs
# outList1 = ["DIS", "hadron", "hadron_theta", "xcheck", "DIS_zvtx", "hadron_pT", "hadron_zvtx", "count"]
# outList2 = ["DIS/DIS", "DIS/DIS_zvtx", "hadron/hadron_pt", "hadron/hadron_theta", "hadron/hadron_zvtx", "electron/electron_pt", "electron/electron_theta", "electron/electron_zvtx"]
# outLists = [ outList1, outList2 ]

##### PARSE COMMAND LINE
##### EXESCRIPT
##### INIT: INPUT-DIR, OUTPUT-DIR BASED ON EXESCRIPT
##### UPDATE INPUT-DIR, OUTPUT-DIR BASED ON ARGUMENTS
##### EXE-DIR: Check it contains exeName, exeScript, data
##### IN-DIR: Relative path ? prepend <EXEDIR>. Check it exists.
##### OUT-DIR: Relative path ? prepend <EXEDIR>. Check it exists.
##### PARSE PERIOD FILE
#####   CHECK INPUT EXISTS
##### LOOP ON ACTIVE PERIODS AND SUBMIT
#####   CHECK OUTPUT DOES NOT ALREADY EXIST (unless force option)
#####   PASS ARG.S TO BATCH AS ENV. VAR.S

def printMoreHelp():
    print(' * submitJobs.py: Submit several RICH matrices jobs to batch\n')
    i = 0
    while i < len(exeScripts):
        print(' "%s"(%s)' % (exeScripts[i],exeNames[i]),end='')
        i += 1
    print()

def main():

    ##### PARSE COMMAND LINE
    # Option MORE HELP
    if len(sys.argv) > 1 and (sys.argv[1] == '-H' or sys.argv[1] == '--HELP'):
        printMoreHelp()
        sys.exit(2)
    # "argparse" PARSER
    parser = argparse.ArgumentParser(description='Submit several RICH matrices jobs to batch')
    parser.add_argument('-e',dest='exeDir',default=DExeDir,help="Exe dir name. D = \"%s\"" % DExeDir)
    parser.add_argument('-s',dest='exeScript',default=DExeScript,help="Batch script \"(fit_table_plots|fit_table_fit).csh\". D = \"%s\"" % DExeScript)
    parser.add_argument('-i',dest='inDir',default=DInDir,help='Input  dir name. D = \"(%s|%s)\"' % (inDirs[0],inDirs[1]))
    parser.add_argument('-o',dest='outDir',default=DOutDir,help='Output dir name. D = \"(%s|%s)\"' % (outDirs[0],outDirs[1]))
    parser.add_argument('-f','--force',dest='force',action='store_true',help='Force even if output already exists')
    parser.add_argument('-N','--NOP',dest='nop',action='store_true',help='No OPeration')
    parser.add_argument('-H','--HELP',dest='moreHelp',action='store_true',help="More help")
    parser.add_argument('-q','--quiet',dest='quiet',action='store_true',help='Less verbosity')
    args = parser.parse_args()
    verbose = args.quiet == False
    force = args.force
    nop = args.nop

    ##### EXESCRIPT
    exeScript = args.exeScript
    ##### INIT: INPUT-DIR, OUTPUT-DIR BASED ON EXESCRIPT
    exeName = ""
    exeOption = ""
    inDir = ""
    outDir = ""
    i = 0
    match = False
    while i < len(exeScripts):
        if exeScript == exeScripts[i]:
            exeName = exeNames[i]
            exeOption = exeOptions[i]
            inDir = inDirs[i]
            outDir = outDirs[i]
            match = True
            break
        i += 1
    if not match:
        sys.stderr.write('** submitJobs: Invalid <EXESCRIPT>(="%s") arg.\n   => Exiting...\n' % (exeScript))
        sys.exit(2)
    ##### UPDATE INPUT-DIR, OUTPUT-DIR BASED ON ARGUMENTS
    inDir = args.inDir
    outDir = args.outDir
    inconsistent = False
    if args.inDir == DInDir and exeScript != DExeScript:
        if exeScript == exeScripts[1]:
            inDir = inDirs[1]
        else:
            inconsistent = True
    if args.outDir == DOutDir and exeScript != DExeScript:
        if exeScript == exeScripts[1]:
            outDir = outDirs[1]
        else:
            inconsistent = True
    if inconsistent:
        sys.stderr.write('** submitJobs: Internal inconsistency.\n   => Exiting...\n')
        sys.exit(2)
        
    ##### EXE DIRECTORY: Check it contains exeScript, exeName, data
    m = re.match(r'^/',args.exeDir)
    if m:
        exeDir = args.exeDir
    else:
        exeDir = '%s/%s' % (os.environ['PWD'],args.exeDir)
    exeDir = os.path.expanduser(args.exeDir)
    exeScriptPath = "%s/%s" % (exeDir,exeScript)
    if not os.path.isfile(exeScriptPath):
        sys.stderr.write('** submitJobs: No "%s" file in <EXEDIR> = "%s"\n   => Exiting...\n' % (exeScript,exeDir))
        sys.exit(2)
    exePath = "%s/%s" % (exeDir,exeName)
    if not os.path.isfile(exePath):
        sys.stderr.write('** submitJobs: No "%s" file in <EXEDIR> = "%s"\n   => Exiting...\n' % (exeName,exeDir))
        sys.exit(2)

    ##### IN-DIR: Relative path ? prepend <EXEDIR>. Check it exists.
    inDir = os.path.expanduser(inDir)
    m = re.match(r'^/',inDir)
    if m:
        inDirPath = inDir
        if not os.path.isdir(inDirPath):
            sys.stderr.write('** submitJobs: <INDIR> "%s" is not a directory\n   => Exiting...\n' % inDirPath)
            sys.exit(2)
    else:
        inDirPath = '%s/%s' % (exeDir,inDir)
        if not os.path.isdir(inDirPath):
            sys.stderr.write('** submitJobs: No <INDIR> "%s" sub-directory in <EXEDIR> = "%s"\n   => Exiting...\n' % (inDir,exeDir))
            sys.exit(2)
        
    ##### OUT-DIR: Relative path ? prepend <EXEDIR>. Check it exists.
    # Note: would be better to check output directory is writable
    outDir = os.path.expanduser(outDir)
    m = re.match(r'^/',outDir)
    if m:
        outDirPath = outDir
        if not os.path.isdir(outDirPath):
            sys.stderr.write('** submitJobs: <OUTDIR> "%s" is not a directory\n   => Exiting...\n' % outDirPath)
            sys.exit(2)
    else:
        outDirPath = "%s/%s" % (exeDir,outDir)
        if not os.path.isdir(outDirPath):
            sys.stderr.write('** submitJobs: No <OUTDIR> "%s" sub-directory in <EXEDIR> = "%s"\n   => Exiting...\n' % (outDir,exeDir))
            sys.exit(2)
        
    ##### SUBMIT
    print(' * submitJobs: Submitting \"%s\" jobs < \"%s\" > \"%s\"' % (exeScript,inDirPath,outDirPath))
    command = 'qsub -P P_compass'
    command += ' -V' # Submission shell env. passed to batch shell
    command += ' -l os=cl7'           # OS = CENTOS7
    # * Requested                                                          *
    # *   CPU cores:                    1 core(s)                          *
    # *   CPU time:                     02:46:40 (10000 seconds) (1)       *
    # * Consumed                                                           *
    # *   wallclock:                    00:15:56 (956 seconds)             *
    # *   CPU time:                     00:06:21 (381 seconds)             *
    # *   CPU scaling factor:           11.10                              *
    # *   normalized CPU time:          01:10:38 (4238 HS06 seconds)       *
    # *   CPU efficiency:               39 % (2)                           *
    command += ' -q long -l ct=10000' # CPU requested (see above)
    command += ' -l fsize=4G'         # Disk size requested
    # Book I/O on "/sps".
    # - Needed only if input TTree there.
    # - Could else be "-l xrootd=1" or "-l hpss=1"
    command += ' -l sps=1'
    command += ' -N fttbles%s' % exeOption # Job name: a(naly)S(IDIS_)s(split)
    # Log file: <exeOption>.log in outDir. Mixes stdout and stderr
    logFileName = '%s/%s.log' % (outDirPath,exeOption)
    command += ' -o %s -j yes' % logFileName
    command += ' -V %s' % exeScriptPath
    if nop:   # NOP: Print submit command to stdout
        print('"%s"\n' % command)
        sys.exit(0)
    ##### PASS ARG.S TO BATCH AS ENV. VAR.S
    os.environ["fit_table_EXEDIR"] = exeDir
    os.environ["fit_table_INPATH"] = inDirPath
    os.environ["fit_table_OUTPATH"] = outDirPath
    os.environ["fit_table_EXEOPTION"] = exeOption
    if verbose:
        print('"%s"\n' % command)
    status = os.system(command)
    if status:
        status = os.system(command)
        print(' * submitJobs: Try again submitting ')
        if status:
            print('** submitJobs: Persistent submission error\n   => Exiting...\n')
            sys.exit(2)

    ##### SUMMARY
    sys.exit(0)

if __name__ == "__main__":
  main()
