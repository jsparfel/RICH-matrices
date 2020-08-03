#!/bin/csh

# - Script to run fit_table fit
# Usage: qsub -V fit_table_fit.csh
# - Arguments are passed as env. variables
#    - fit_table_EXEDIR
#    - fit_table_INPATH
#    - fit_table_OUTPATH
#    - fit_table_EXEOPTION
# - Works in combination w/ "./submitJobs.py".

##### CHECK ARG. ENV. VARIABLES fit_table_...
##### INSTALL LOCALLY I/O DIRS AND FILES AS REQUIRED BY fit_table fit
##### EXECUTE fit_table W/ OPTION fit
##### COPY OUTPUTS TO OUTPATH

printf '+++++++++++++++++++++++++++++++\n'
printf ' * fit_table: Run fit_table fit\n'
printf '+++++++++++++++++++++++++++++++\n'

##### WORKING DIR = $TMPDIR
if ( $?TMPDIR == 0 ) then
    printf '\n** fit_table: Inconsistency: No $TMPDIR\n'
else
    cd $TMPDIR
endif

##### CHECK ARG. ENV. VARIABLES fit_table_...
set exeName = fit_table
if ( $?fit_table_EXEDIR == 0 ) then
    printf '\n** fit_table: Inconsistency: No $fit_table_EXEDIR\n'
    exit 2
else
    set exeDir = $fit_table_EXEDIR
    set exePath = $exeDir/$exeName
    if ( !( -e  $exePath ) ) then
	printf '\n** fit_table: Inconsistency: No "%s" in EXEDIR "%s"\n' $exeName $exeDir
	exit 2
    endif
endif
if ( $?fit_table_INPATH == 0 ) then
    printf '\n** fit_table: Inconsistency: No $fit_table_INPATH\n'
    exit 2
else
    set inPath = $fit_table_INPATH
endif
if ( $?fit_table_OUTPATH == 0 ) then
    printf '\n** fit_table: Inconsistency: No $fit_table_OUTPATH\n'
    exit 2
else
    set outPath = $fit_table_OUTPATH
endif

##### INSTALL LOCALLY I/O DIRS AND FILES AS REQUIRED BY fit_table
# INPUT DIR

mkdir table
cd table
mkdir k 
mkdir p 
mkdir pi 
cd ..
\cp $inPath/options_fit.dat .
\cp $inPath/plots_K0L/hist_*.root .
\cp $inPath/plots_Phi/hist_*.root .

##### EXECUTE fit_table W/ OPTION fit
printf '\n~~~~~~~~~~~~~~~~~~~~~\n'
printf ' * Execute "%s"\n' $exePath
printf   '~~~~~~~~~~~~~~~~~~~~~\n'
$exePath fit
set exeStatus = $status
printf   '~~~~~~~~~~~~~~~~~~~~~\n'
if ( $exeStatus != 0 ) then
    printf ' * fit_table: Execution returns %d\n' $exeStatus
printf   '~~~~~~~~~~~~~~~~~~~~~\n'
endif
    
##### COPY OUTPUTS TO OUTPATH
set copyStatus = 0
set files = `\ls`
printf ' * Copying to "%s":' $outPath; echo $files
foreach file ( $files )
    \cp -r $file $outPath
    if ( $status != 0 ) then
	set copyStatus = 1
    	printf '** Error copying "%s" to "%s"\n' $file $outPath
    endif
end

##### ERROR
set error = `expr $exeStatus \* 2 + $copyStatus`
printf '+++++++++++++++++++++++++++++++\n'
printf '\ * fit_table: Script execution status = %d\n' $error
printf '+++++++++++++++++++++++++++++++\n'
exit $copyStatus
