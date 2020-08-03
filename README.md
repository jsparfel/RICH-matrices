# RICH matrices calculation


## [C++] fit_table plots<a name="fit_table plots" />

**Description:**
Takes .root files and creates/plots histograms of invariant mass distributions for K0, Lambda and inclusive Phi samples. `fit_table plots` should be launched first on mDST treated with Phast User Event 13010 for K0 and Lambda samples and a second time on mDST treated with Phast User Event 13060 for inclusive Phi sample.

**Requires:**
 - **ROOT TTree from Phast User Event 13010 or 13060 (13010 for K0 and Lambda, 13060 for inclusive Phi)**

**Directories/files to be created before execution:**
 - **`[data_file]/` is the directory containing .root files previously treated with Phast User Event 13010 or 13060 and `[data_file]` is defined in `options_fit.dat` (see below)**
 - **`./options_fit.dat` where `.` denotes the directory from which the execution of `fit_table` is launched and `options_fit.dat` is a text file with the following structure (in this example we treat inclusive Phi sample and input .root files should be in `/sps/compass/julien/RICH/Phi_8910/h-273666` to `/sps/compass/julien/RICH/Phi_8910/h-276318`):** 

```
# type of analysis (K0L or iPhi)
analysis: iPhi

# data file containing the reconstructed informations
data_file: /sps/compass/julien/RICH/Phi_8910

# data file template name
data_template: h

# data file numbers
data_firstfile_nb: 273666
data_lastfile_nb: 276318

# Fit type
fit_type: all

# data file containing the histograms
hist_file_phi: ./hist_incl_phi2.root
hist_file_k0: ./hist_k0.root
hist_file_lam: ./hist_lambda.root

# data file containing the final results
out_file: rich.root

# remove the rich pipe from the sample
remove_richpipe: true

# difference allowed between proton threshold and real value
thr_diff: 5

# Options for LH cuts for identifying pions
LH_pi_K: 1.0
LH_pi_p: 1.0
# LH_pi_e:
# LH_pi_mu:
LH_pi_bg: 2.0


# Options for LH cuts for identifying kaons
LH_K_pi: 1.06
LH_K_p: 1.06
# LH_K_e:
# LH_K_mu:
LH_K_bg: 2.0


# Options for LH cuts for identifying protons below threshold ( comparing with bg )
LH_bthr_p_pi: 1.
LH_bthr_p_K: 1.
# LH_bthr_p_p:
# LH_bthr_p_e:
# LH_bthr_p_mu:

# Options for LH cuts for identifying protons above threshold
LH_bthr_p_pi_bg: 2.3
LH_bthr_p_K_bg: 3.0
LH_bthr_m_pi_bg: 2.2
LH_bthr_m_K_bg: 2.9

# Options for LH cuts for identifying protons above threshold
LH_athr_p_pi: 1.
LH_athr_p_K: 1.
# LH_athr_p_e:
# LH_athr_p_mu:
LH_athr_p_bg: 1.

# Change the maximum number of fit attempts when results for the fractions are at the limit of their range
max_retry: 100

# Line width of the fit in the fit results
line_width: 2

sidebins: false
```

**Call:**
```Bash
[exe_path]/fit_table plots
```
where `[exe_path]` is a directory containing the executable `fit_table`.

See `submitJobs.py` to submit `fit_table plots` jobs to the batch (necessary when treating massive data).

**Outputs:**
 - **Histograms in .root files: `./hist_incl_phi2.root` or `./hist_k0.root` and `./hist_lambda.root`**
 - **Files `test.C` and `test.pdf`**

## [C++] fit_table fit<a name="fit_table fit" />

**Description:**
Takes outputs of `fit_table plots`, makes fits of mass distributions and calculates/plots identification probabilities of hadrons.

**Requires:**
 - **Output .root files of `fit_table plots`**

**Directories/files to be created before execution:**
 - **`./options_fit.dat` where `.` denotes the directory from which the execution of `fit_table` is launched and `options_fit.dat` is a text file with structure defined above**
 - **`./table/pi/`, `./table/k/` and `./table/p/` are directories into which some .pdf output files will be created**
 - **`./hist_k0.root`, `./hist_lambda.root` and `./hist_incl_phi2.root`: outputs of `fit_table plots`**

**Call:**
```Bash
[exe_path]/fit_table fit
```
where `[exe_path]` is a directory containing the executable `fit_table`.

**Outputs:**
 - **Several .root and .pdf files containing fits and identification probabilities**
 - **Files `rich_mat.txt` and `rich_err.txt` which can then be used by the multiplicities analysis framework (in analySIDIS_split)**

## [Python] submitJobs.py<a name="submitJobs.py" />


**Description:**
Submit `fit_table plots` jobs to the batch.

**Requires:**
 - **Same as `fit_table plots`**
 - **Script `fit_table_plots.csh`**

**User Dependence:**
 - **Same as `fit_table plots`**

**In File Flags**
 - **Same as `fit_table plots`**

**Directories/files to be created before execution:**
 - **Same as `fit_table plots`**
 - **Script `fit_table_plots.csh` should be put in the same directory as executable `fit_table`**

**Call:**
```Bash
python [path]/submitJobs.py -e [exe_path] -s fit_table_plots.csh -i [input_path] -o [output_path] -f
```
where `[path]` is a directory containing `submitJobs.py`, `[exe_path]` is a directory containing the executable `fit_table`, `[input_path]` is the directory into which there are .root files previously treated with Phast User Event 13010 or 13060 and `[output_path]` is the directory into which output files will be written. Option `-f` forces the writing of outputs even if files already exist.

**Outputs:**
 - **Same as `fit_table_plots`**
 - **`[output_path]/plots.log`: .log file of the job**
