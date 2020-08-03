CC      = g++
CFLAGS  = -Wall -std=c++11 -Wextra -O3 -g
LDFLAGS = `root-config --glibs --cflags` -lRooFit -lRooFitCore
#INCL += -I/usr/local/roorarfit/RooRarFit
#LIB += -L/usr/local/roorarfit

OBJ = fit_table.cc fit_table.h

all: table

table:  $(OBJ)
	$(CC) $(CFLAGS) -o fit_table fit_table.cc $(LDFLAGS) $(LIB) $(INCL)
