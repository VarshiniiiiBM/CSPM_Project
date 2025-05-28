# Meeting 2025-05-27

Location: A3.2.08
 Time: 10:00 am

Minutes Made by Varshini

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

* Use some Jason Structure or define just 1 character that will never happen in data (should be discussed with the team)
* Sending data every 50 ms is not suggested 
* In transmission of data there should be more delay
* Put the data sheets in the hessen box 
* Change the baud rate because its not fast enough


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
* Try modifying Resistance  
* How to calculate Inductance?
* Maybe more windings?? higher for the marbel but same current??(needs to be decided and if agreed calculated)
* For the question asked by smit- How to calculate magnetic force? 
  - its done in the test 
  - its there in the lua code
  - it depends on how high you want to shoot the marbel
* Suggestion by professor - 0.5mm of the thickness is optimum but, might be improved



11.04-11.10- Professors Overall Feedback to everybody

* Include more slides from next meeting 
* In the next weeks meeting along with Prof Klein everybody must present for 5 mins (min 4 - max 6)
* Focus more on the results of what we have done in the project already.
* See the coil of the other group.

1.Next weeks Agenda and meeting minutes will be done by Anisha 

2.Smit will collect the wire from professor at 9.00 am in the lab


11.10-11.30 - Abhyshek

* Questions asked about concept of coil gun, servo motors, controlling the angle of the coil gun, is it feasible to go with the coil?
* Sugesstion by Professor-

1.Potentional Engergy must be calculated

2.Number of Turns and Voltage is calculated by FEMM software

3.Luna script can be found in the GitHub

