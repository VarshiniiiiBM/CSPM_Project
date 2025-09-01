#Inductance Measurement Experiment 

The purpose of this experiment is to measure and analyze the inductance of electromagnet coils. By characterizing the inductance of different coil designs , we can optimize performance of coil.

#Equipment

In above Experiment setup file shows  equipments we used and connection we made for the experiment.

1). DC Power Supply
* It provides adjustable DC voltage and current for energizing the coil.

2). Function Generator (Signal Generator)
* It can produce different type of signals such as sinusoidal, square and triangular.
* Used to apply AC excitation signal to the coil for inductance measurement.

3). Oscilloscope 
* It captures and displays the time - domain waveform of voltage and current.
* We can observe phase difference between voltage and current.

4). Multimeter
* For direct measurement of coil´s resistance and inductance.

5). Breadboard
* We used custom breadboard where vertical group of 5 holes in the middle are connected internally.
* The long horizontal strips on the sides are power rails (positive and ground).

#About connection details of experiment

*The function generator is connected in series with coil and shunt resistor. Oscilloscope Channel 1 is connected across the coil and channel 2 is connected across the shunt resistor.
*Multimeter is directly connected across the coil to measure resistance.

#Experiment result on oscilloscope.

In Experiment result file we can see two different waveforms it indicates voltage and current characteristics.

*The yellow waveform is almost constant. It indicate the applied voltage from the function generator.
*The blue waveform shows a gradual rising curve, typical of current through an inductor. At the moment of voltage application, current starts at zero, then it increases gradually following an exponential curve,because coil stores energy in its magnetic field.
*The delay in current growth is direct effect of inductance.
*By measuring how fast the current rises (the time constant,T = L/R). the inductance of the coil can be calculated.

#Inductance result

* Here we got T(time constant) around 119μs on oscilloscope. Resistance value we got 5.8 Ω on multimeter.
* Inductance value is 689 μH.


#In project we are using two coils.Below are reistance and inductance values of both coil. 

1). Vertical Coil Resistance - 0.7126 Ω.
2). Vertical Coil Inductance - 686.6 μH. 
3). Horizontal Coil Resistance - 0.7644 Ω.
4). Horizontal Coil Inductance - 715.9 μH.
 

