/*
DiMoSC computes 1-stable manifold (max-sadlle path) from function 
defined on simplicial complex.

Input: Simplicial complex - binary version.
Output: [file_name]_vert.txt, [file_name]_edge.txt - ascii version.

See example for more input and output details.

Assumption: Number of simplices would not be more than MAX_INT / 3.
If it exceed the maximum allowed numnber, please use split and merge algorithm.

Usage: ./densityRips <input_file> <output_file> <persistence_threshold> <dimension> [use_previous]
*/

// g++ DiMoSC.cpp -I./phat/include -std=c++11 -o DiMoSC -w
// Debug switch - slower but output more information
#define DEBUG 0


int DIM;			// Dimension of data - 3 for 3D, 2 for 2D

// For higher dimension, change MAX_DIM
#define MAX_DIM 3			// - Will be used in Simplex.h
#define EPS_compare 1e-8	// - used in comparison functions

#include <ctime>
#include <fstream>
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

#include "Simplex.h"
#include "persistence.h"
#include "DiscreteVField.h"
#include "Simplicial2Complex.h"


#include "spt.h"

int main(int argc, char* argv[]){
    clock_t begin = clock();
    //------------------- pre_time ------------------------
	string output_file[2];
    string sp_output_file[2];
    string pre_save;
	bool use_pre_save = false;
	
	double et_delta = 0;
	double ve_delta = 0;
	
    if (argc < 5){
    	// must provide 4 parameters.
    	// argv[1] - inut_file
    	// argv[2] - output_file
    	// argv[3] - persistence_threshold
    	// argv[4] - dimension
    	// argv[5] - use_previous - optional
    	// argv[6] - triangle threshold - under experiment
		cout << "Usage: ./densityRips <input_file> <output_file> <persistence_threshold> <dimension> [use_previous]"
		<<endl;
		return 0;
    }else{
		output_file[0] = string(argv[2]) + "/vert.txt";
		output_file[1] = string(argv[2]) + "/edge.txt";
        sp_output_file[0] = string(argv[2]) + "_spvert.txt";
        sp_output_file[1] = string(argv[2]) + "_spedge.txt";


		ve_delta = atof(argv[3]);
		DIM = atoi(argv[4]);
	}
    if (argc >= 6){
		pre_save = string(argv[5]);
		use_pre_save = true;
    }
    if (argc >= 7){
    	et_delta = atof(argv[6]);
    }else{
    	et_delta = ve_delta;
    }
	
	cout << argc-1 << " parameters detected"<< endl;
	if (DEBUG){
		cout << "debug mode\n";
		// memory usage info.
		cout << sizeof(Simplex) << " " << sizeof(Vertex) << " " << sizeof(Edge) << " "
			 << sizeof(Triangle) << " " << sizeof(Triangle*)<< endl;
	}
	
	Simplicial2Complex K;
    clock_t begin_preprocess = clock();
	if (!use_pre_save){

        clock_t begin_ = clock();

		cout << "Reading in simplicial complex...\n";
		K.buildComplexFromFile2_BIN(argv[1]);
		cout << "Done\n";
		cout.flush();
		// cin.get(); // has test

        clock_t end_ = clock();
        double elapsed_secs_ = double(end_ - begin_) / CLOCKS_PER_SEC;
        cout<<"read in and build complex: "<<elapsed_secs_<<endl;

        begin_ = clock();
		// Build psudo morse function
		cout << "Building pseudo-Morse function...\n";
		K.buildPsuedoMorseFunction();
		cout << "Done\n";
		cout.flush();
		// cin.get(); 

        end_ = clock();

        elapsed_secs_ = double(end_ - begin_) / CLOCKS_PER_SEC;
        cout<<"building pseudo-Morse function: "<<elapsed_secs_<<endl;

        begin_ = clock();

		cout << "Building filtration...\n";
		K.buildFiltrationWithLowerStar();
		cout << "Done\n";
		cout.flush();
		// cin.get(); // has test

        end_ = clock();
        elapsed_secs_ = double(end_ - begin_) / CLOCKS_PER_SEC;
        cout<<"filtration time: "<<elapsed_secs_<<endl;

        begin_ = clock();

		cout << "Computing persistence pairs...\n";
		K.PhatPersistence();
		cout << "Done!\n";
		cout.flush();
        cout << "Outputing persistence pairs...\n";

        end_ = clock();
        elapsed_secs_ = double(end_ - begin_) / CLOCKS_PER_SEC;
        cout<<"persistence time: "<<elapsed_secs_<<endl;

		cout << "Writing pre_saved_data...\n";
		K.write_presave(argv[2]);
		cout << "Done!\n";
		cout.flush();
	}else{
		cout << "Reading in pre_saved_data...\n";
		K.Load_Presaved(argv[1], pre_save);
		cout << "Done\n";
		cout.flush();
		// cin.get();
		
		// Build psudo morse function
		cout << "Building pseudo-Morse function...\n";
		K.buildPsuedoMorseFunction();
		cout << "Done\n";
		cout.flush();
	}
    //------------------- pre_time ------------------------
    clock_t end = clock();
    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

    clock_t end_preprocess = clock();
    double preprocess_time = end_preprocess-begin_preprocess;
    cout<<"preprocess time: "<<preprocess_time/ CLOCKS_PER_SEC<<endl;

//    clock_t begin1 = clock();
//    //----------------cancel time----------------//
//	cout << "Cancelling persistence pairs with delta " << ve_delta << "\n";
//	begin = clock();
//	// Cancellation does not use function values on simplicies
//	K.cancelPersistencePairs(ve_delta);
//	cout << "Done\n";
//	end = clock();
//	elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
//	cout<<"cancellation time: "<<elapsed_secs<<endl;
//
//	begin = clock();
//	K.outputArcs(output_file[0], output_file[1], et_delta);
//	cout.flush();
//	end = clock();
//	elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
//	cout<<"retrive time: "<<elapsed_secs<<endl;
//
//	//----------------cancel time----------------//
//    clock_t end1 = clock();
//    double elapsed_secs1 = double(end1 - begin1) / CLOCKS_PER_SEC;

//    clock_t begin2 = clock();
//
//    //----------------- sp time ----------------//
//    //Build spanning tree with v-e pairs
//
//    cout<<"sp1:"<<endl;
//
//	begin = clock();
//
//    cout<<"build spanning tree.";
//    K.build_spt(ve_delta);
//    cout<<"Done."<<endl;
//
//	end = clock();
//	elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
//	cout<<"build sp tree time: "<<elapsed_secs<<endl;
//    //Retrive ve
//
//	begin = clock();
//
//    K.retrieve_1manifold();
//
//	end = clock();
//	elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
//	cout<<"retrive time: "<<elapsed_secs<<endl;
//
//	begin = clock();
//
//    K.convert_output();
//    K.write_output("1_vert.txt", "1_edge.txt");
//
//	end = clock();
//	elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
//	cout<<"write output time: "<<elapsed_secs<<endl;
//    //----------------- sp time ----------------//
//    clock_t end2 = clock();
//    double elapsed_secs2 = double(end2 - begin2) / CLOCKS_PER_SEC;
//    cout<<"sp time: "<<elapsed_secs2<<endl;

//    cout<<"pre process, persistence: "<<elapsed_secs<<endl;
//    cout<<"Cancel time: "<<elapsed_secs1<<endl;
//    cout<<"sp time: "<<elapsed_secs2<<endl;

//sp2
    clock_t begin3 = clock();
// build tree
    cout<<"sp2:"<<endl;
	begin = clock();

    cout<<"build spanning tree.";
    K.build_spt3(ve_delta);
    cout<<"Done."<<endl;

	end = clock();
	elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	cout<<"build sp tree time: "<<elapsed_secs<<endl;
//retrive
    begin = clock();

    //K.retrieve_1manifold2();
    K.retrieve_1manifold_simp();

    end = clock();
    elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout<<"retrive time: "<<elapsed_secs<<endl;
//output
    begin = clock();

    K.convert_output();
    K.write_output(output_file[0], output_file[1]);

    end = clock();
    elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout<<"write output time: "<<elapsed_secs<<endl;
//sp2
    clock_t end3 = clock();
    double elapsed_secs3 = double(end3 - begin3) / CLOCKS_PER_SEC;
    cout<<"sp2 time: "<<elapsed_secs3<<endl;
	return 0;
}
