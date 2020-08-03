#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>

#include <TROOT.h>

#include <TCanvas.h>
#include <TColor.h>
#include <TGaxis.h>
#include <TFile.h>
#include <TGraphErrors.h>
#include <TH1.h>
#include <TH2.h>
#include <TH2D.h>
#include <TH1D.h>
#include <TLegend.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include <TMatrixD.h>
#include <TPaveText.h>
#include <TStyle.h>
#include <TTree.h>

#include <RooGlobalFunc.h>
#include <RooAbsReal.h>
#include <RooAddPdf.h>
#include <RooAddition.h>
#include <RooCategory.h>
#include <RooChebychev.h>
#include <RooConstVar.h>
#include <RooDataHist.h>
#include <RooFFTConvPdf.h>
#include <RooFitResult.h>
#include <RooGaussian.h>
#include <RooGenericPdf.h>
#include <RooGlobalFunc.h>
#include <RooMinuit.h>
//#include <RooMy.h>
#include <RooPlot.h>
#include <RooPolynomial.h>
#include <RooRealVar.h>
#include <RooBreitWigner.h>
#include <RooRelBreitWigner.hh>
#include <RooSimultaneous.h>
#include <RooVoigtian.h>


/*
 *
 *	const TMatrixDSym& cor = r->correlationMatrix() ;
 *	const TMatrixDSym& cov = r->covarianceMatrix() ;
 *	// Print correlation, covariance matrix
 *	cor.Print() ;
 *	cov.Print() ;
 *
 *
 *	// Make list of model parameters
 *	RooArgSet* params = model.getParameters(x) ;
 *	// Write LaTex table to file
 *	params->printLatex(Sibling(*initParams),OutputFile("rf407_latextables.tex")) ;
 *
 *
 *
 */



// ******************************************************************************************

using namespace std;

using std::cout;
using std::cerr;
using std::endl;
using std::map;
using std::stringstream;
using std::vector;
using std::pair;
using std::string;
using std::make_pair;
using std::ios;
using std::setw;
using std::setprecision;


using namespace RooFit ;

// ******************************************************************************************
// const int Np = 6;
// const int Nt = 7;
// const double p_bins[Np+1]={10. ,15. ,20. ,25. ,30. ,40. ,50.};
// const double t_bins[Nt+1]={0.00,0.01,0.02,0.03,0.04,0.06,0.09,0.12};

// const int Np = 13;
// const int Nt = 4;
// const double p_bins[Np+1]={10.,11.,12.,13.,15.,17.,19.,22.,25.,27.,30.,35.,40.,50.};
// const double t_bins[Nt+1]={0.00,0.01,0.04,0.12,0.3};

// const int Np = 15;
// const int Nt = 4;
// const double p_bins[Np+1]={3.,5.,7.,10.,12.,13.,15.,17.,19.,22.,25.,27.,30.,35.,40.,50.};
// const double t_bins[Nt+1]={0.00,0.01,0.04,0.12,0.3};

const int Np = 10;
const int Nt = 2;
const double p_bins[Np+1]={12.,13.,15.,17.,19.,22.,25.,27.,30.,35.,40.};
const double t_bins[Nt+1]={0.01,0.04,0.12};

// const int Np = 1;
// const int Nt = 1;
// const double p_bins[Np+1]={10.,50.};
// const double t_bins[Nt+1]={0.01,0.12};

double N_id[6][5][Np][Nt];
//double R_id[6][4][Np][Nt];

double last_para[30];
double last_para2[Np][Nt][30];

string analysis;
string data_file;
string data_template;
int data_ff_nb;
int data_lf_nb;
int data_nb;
int file_nb = 0;
int nb_events[6] = {0,0,0,0,0,0};
string fit_type;
string hist_file_k0 = "hist.root";
string hist_file_lam = "hist.root";
string hist_file_phi = "hist.root";
string out_file = "rich.root";
double lh_cut[5][6];
TH1D* h[6][5][Np][Nt];
TH2D* h2[6][5][Np][Nt];
TH2D* test_hist;
RooFitResult *r[6][Np][Nt];
int lw = 1;
double thr_diff = 0.;
int retry = 20;
bool rpipe = false;

bool use_improve = false;
bool use_hesse = true;
bool use_minos = false;
bool use_sidebins = true;
bool first_phi = true;
TFile* input;
TFile* input_k0;
TFile* input_phi;
TFile* input_lam;

// ******************************************************************************************

int main(int, char**);
bool get_inputFile(int pi);
void read_options();
void get_input_data_t1();
void get_input_data_t2();
void get_input_data2();

RooDataHist* gen_k0(int, int , int, int);
void write_hist();
void create_hist();
void get_plots();
void fit_table_k0(int);
void fit_table_phi(int);
void fit_table_lambda(int);
void print_table();
void set_plot_style();
