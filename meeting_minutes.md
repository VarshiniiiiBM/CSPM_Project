# Meeting 2025-05-27

Location: A3.2.08
 Time: 10:00 am

Minutes Made by Varshini
Small corrections / clarifications by Fabian (2025-05-30)

- Participants:
- Varshini Barallu Manjunath
- Rohith Joy
- Murtuza Udaipurvala
- Abdul Manaf 
- Anisha
- Smit Patel Kumar
- Abhyshek Rajmohan
- Professor Mink



10.00 - 10.10 - Varshini
* Overview of the Agenda explained


10.10-10.25- Rohith and Varshini

* Slicing and 3D printing coil carrier, converting stl files back into CAD files

Feedback by Professor:
* Need to work on redesigning the coil carrier

10.25 - 10.42- Murtuza

* Explained code of uart to transmit test values on serial.
* Further task, Sample data at a high rate ( 10khz and send it on uart in bursts, every 5 seconds.)



Feedback by Professor:

* Use some JSON Structure (https://www.json.org) or define 1 start / stop character or string (e.g. "START" / "STOP") that will never happen in data (should be discussed with the team)
* Sending data every 50 ms is not useful, as sampling rate will be 10kHz or more
* In transmission of data there should be more delay
* Put the data sheets in the hessen box 
* Change the baud rate if it is not fast enough


10.45-10.52 - Manaf and Anisha

* Used Putty application 
* Code is in development state 
* Once the data structure is given changes in the code will be done 

Feedback by Professor:

* More work to be done on the code
* Update the code in the Github 


10.52-11.02 - Smit

* Went through the Magneto Static Tutotrial 
* Solution  is uploaded in the GitHub
* Once coil carrier is confirmed design will be created in FEMM
* Measurement of the wire, Magnetic force needed to push the marbel will be calculated
* First simulation is done and then its implemented

Feedback by Professor:

* Simulation should be uploaded 
* Take the existing one and optimize it 
* Think of different simulating design (For example: Diagonal, 45 degrees) and how to 3D model and simulate
* Calculate Resistance and Inductance to make sure it will work with 24V
* How to calculate Inductance?
* Maybe more windings?? higher for the marbel but same current??(needs to be decided and if agreed calculated)
* For the question asked by smit- How to calculate magnetic force? 
  - its done in the test 
  - its there in the lua code
  - it depends on how high you want to shoot the marbel
* Suggestion by professor - wire diameter 0.5mm ... 0.75mm seems to be optimum according to experiences made with previous designs; but also other diameters might work



11.04-11.10- Professors Overall Feedback to everybody

* Include more slides from next meeting 
* In the next weeks meeting along with Prof Klein everybody must present for 5 mins (min 4 - max 6)
* Focus more on the results of what we have done in the project already and not what you are planning to do; there can be a small outlook for future work (1 min for each student)
* See the coil of the other group.

1.Next weeks Agenda and meeting minutes will be done by Anisha. Please prepare everything (switch on the projector etc...) so that we can directly start 10:00 without further delay. Anisha will also give a short overview of the agenda at the beginning (2..3min)

2.Smit will collect the wire from professor at 9.00 am in the lab



11.10-11.30 - Abhyshek

* Questions asked about concept of coil gun, servo motors, controlling the angle of the coil gun, is it feasible to go with the coil?
* Sugesstion by Professor-

1.Potentional Engergy must be calculated

2.Number of Turns and Voltage is calculated by FEMM software

3.Luna script can be found in the GitHub


# Meeting 2025-05-08
Meeting time and location: 2025-05-08, 09:00; 

minutes kept by:  >>Rohith Joy<<

Participants:
- Rohith
- Murtaza
- Anisha
- Prof. Mink

Diskussed Topics:
- Generate a hessenbox link
- ppt on Project parts done by each member.
- Grundgesetz
- materials used to 3D print
- Purchasing hall-effect sensors
- FEMM test on next week
- Output measurement data via serial interface; plotting of values
- Generating a code with dummy values on STM board for plotting in MATLAB


Tasks todo until the next meeting:
- Abdul Manaf: prepare for FEMM test 
- Anisha: prepare for FEMM test
- Fabian: Prepare test on FEMM magnetic field simulation; provide sketches for CAD designs; Dynamic simulation
- Murtuza:prepare for FEMM test; Purchase quotation for hall-efect sensors 
- Rohith:prepare for FEMM test
- Smit:prepare for FEMM test
- Varshini:prepare for FEMM test


Next meeting: 14th May at 2:00 PM

