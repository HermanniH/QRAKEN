# QRAKEN
Quantum RAndom Keys via ENtanglement. QRAKEN is a certified quantum random number generator for the Qiskit framework. It runs a series of Bell-experiments on the IBM quantum computers, from which a string of random numbers is extracted if the CHSH inequality is violated. The scheme does not assume i.i.d. conditions between runs or fair sampling, so memory effects of the hardware can be tolerated. From the CHSH correlator we calculate the amount of entropy present in the bitstring, which is then extracted. The resulting random numbers produced are certified to be truly random, in the sense that the numbers were created in the moment of measurement and have no seed. 

Bell’s theorem gives us bounds on the maximal amount of correlations between two distant parties if the outcomes of their experiments could in some way be predicted deterministically. However, if their experiments are entangled with each other, quantum mechanics allows them to violate this maximal bound. The conclusion must be that the measurement outcomes can not be predicted deterministically, i.e. they must be random. As a consequence, we can use the violation of a Bell-inequality as a certification scheme for randomness. A maximal violation of the CHSH-inequality (a type of Bell-inequality) guarantees that every single outcome is impossible to predict. A smaller violation leaves room to predict some fraction of the outcomes. This fraction is best described by the entropy H_min. We calculate this entropy based on [1], which does not assume i.i.d. conditions or fair sampling. With the entropy of the generated bit string, it is possible to calculate the number of purely random bits present in the string. These numbers can then be extracted with the aid of a randomness extractor, such as Trevisan’s extractor [2]. We use the implementation by the authors of [1], available on [GitHub](https://github.com/jdbancal/libtrevisan). 


## Pre-requisites:

- Numpy
- Scipy
- Trevisan extractor (follow installation steps [here](https://github.com/jdbancal/libtrevisan) )
- Binascii
- Pickle
- Qiskit

We recommend installing Anaconda, which provides you with most of the packages. Additionally you only need Qiskit and the extractor algorithm.


## Manual

To generate random numbers with QRAKEN, you first need to open Bell inequality_v2.ipynb. 
1) The first cell imports all required packages
2) Second cell is where you decide the parameters for the experiment:
   1)	Local: True/False, decides if you run the code locally on the qasm simulator, or if the code is submitted to the actual hardware.
   2) Mode: For mode, there are two options. The experiment can be run with a perfect Bell-state that maximally violates the CHSH inequality. Generating that state requires more gates. This is Mode = 0. With Mode =1 you generate a Bell state, which theoretically increases your CHSH violation (leading to a higher key rate), but this increases the required number of gates in the circuit. Mode 0 is explained [here](https://decpieibmquantumexperience.blogspot.com/2017/10/chsh-experiment-on-quantum-computer.html)
   3) Multcircuit: The code will generate 4 circuits, corresponding to the 4 different measurement scenarios. Multcircuit determines how many copies we submit each circuit within one batch submission to IBM. 
   4) Shots: How many evaluations of each circuit are done. Maximal number recommended. 

After this, evaluate all the cells in the notebook.

When your programme has executed, you will find the output as a file called something like “outputCHSH_machine_Concat_dataset.txt”. This is the file you will use as input for the extractor. Before we do that, we also need to calculate the amount of entropy available in the string. This is done using the script Parameters_extractors.py. 
Here you set your parameters as you like, the explanations for each of them can be found in the supplemental material of [1]. The main parameters in our interest are the following:
1)	n: This is the number of bits you have generate in the previous step. It can be found after the evaluation of the second cell in the notebook. The larger the n, the larger is m, the number of random bits we can extract from the string. (also m/n is larger).
2)	w_exp: this is the winning probability of the CHSH game. It is calculated according to w_exp = 0.5+S/8 for the CHSH parameter S, which is found at the end of the previous notebook. The S correlator value will depend on the actual hardware you use and even the specific pairs of qubits. The larger your S (-> w_exp), the better. 
3)	delta_est: is the significance level at which you want your bit string to random. The smaller you make this, the fewer bits you will be able to extract. 

Once you have evaluated the code, you will be presented by the numbers 2*n, m, and rate. These will be used as input to the Trevisan extractor. Now make sure your output-file from the notebook and the seed random number ‘rnd_short_subset1.txt’ are in the libtrevisan folder and run the following command in your terminal:

`./extractor -v --Blk_Design --bitext rsh --eps 1e-5 --alpha ‘rate’  --weakdes gfp --outputsize ‘m’ --inputsize ‘2*n’ --seed rnd_short_subset1.txt --input ‘input.txt’ --output_file ‘output.txt’`

You will most likely encounter an error, which says your m is too large and the most number of extractable bits is something marginally less. Adjust m down to that, as the algorithm is not able to extract quite as many bits as you’d wish for. 

Once you have run the extractor, you have an output file called ‘output.txt’, which contains the certified random numbers you have extracted from the raw data. 

Time to celebrate!


## References

[1] Shen, Lijiong, et al. "Randomness extraction from bell violation with continuous parametric down-conversion." Physical review letters 121.15 (2018): 150402.

[2] Ma, Xiongfeng, et al. "Postprocessing for quantum random-number generators: Entropy evaluation and randomness extraction." Physical Review A 87.6 (2013): 062327.

