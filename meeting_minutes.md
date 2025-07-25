# Meeting 2025-07-22

Location: Lab Time: 12:30 am

Minutes Made by Abdul Manaf Mansoor.

- Participants:
- Varshini Barallu Manjunath
- Rohith Joy
- Murtuza Udaipurvala
- Abdul Manaf Mansoor
- Anisha Bhanderi
- Smit Patel
- Prof. Mink

Discussed Topics

1. Final Coil Model(Rohit) : Two coils will be used in the design one on the top and one on the bottom—mounted. The model will be 3D printed and ready by tomorrow. Smith and Murtuza will handle the winding process.
* Feedback from Professor : Focus on completing the project. Get the first prototype printed and ready for testing. Might need more changes.

2. Capacitor Calculation(Smith): Discussed energy calculation using capacitor formula (1/2)*C*V^2. Discussion of mechanical energy conversion. 
* Discussion with professor : Energy efficiency is below 10% based on observations from the previous project. Work done and energy loss were calculated for a 20A current coil. Picture Attached in Hessenbox.
   This calculation should be included in the report.

3. Discussion of Work Plan (Murtuza) : Discussed work plan packages for everyone.
              1) Extended Existing Design with new hardware:
                  a) Motor Controller
                  b) STM32 Board
                  c) Python Dashboard
                  d) Matlab Simulation
               2) New Coil Model:
                  a) 3D printing new model
                  b) Winding New model
                  c) Magnetic sensor

4. Python Dashboard (Manaf) : Dashboard updated with time in Millisecond presented.
*   Feedback from Professor: The dashboard still has dummy data in seconds. The dashboard display a burst of data and then stop. The dashboard is cleared and new data is plotted when it arrives. Next demostration should
   get data from microcontroller. This could be achieved by having a button on microcontroller that sends burst of data when it is pressed. This data is received on serial and then plotted.

General : During the leave period, meetings should be held once a week, and the minutes should be updated. Lab access requires safety and security instructions to be given first by Mohammed Shaami. Everyone’s vacation
plans should be discussed.


# Meeting 2025-07-01

Location: A3.2.08 Time: 10:00 am

Minutes Made by Abdul Manaf Mansoor.

- Participants:
- Varshini Barallu Manjunath
- Rohith Joy
- Murtuza Udaipurvala
- Abdul Manaf Mansoor
- Anisha Bhanderi
- Smit Patel
- Prof. Mink

Discussed Topics

1. Coil Inductance Calculation
   
* Discussed methods to verify the accuracy of inductance measurements:
* Use of FEMM was discussed.
* Possibility of using an LCR meter was also discussed.
* Professor inquired about expected accuracy of the measurements; suggested that an accuracy of ±20% is acceptable.
* Professor emphasized that the marble's permeability will have a significant influence on the inductance (increase of inductance by 20...50%, maybe even more). So it does not make sense to calculate an "accurate" value for inductance without considering the marble. Consequence: A rough estimate of the inductance is sufficient. Basic inductance estimation formulas (e.g. https://en.wikipedia.org/wiki/Solenoid or https://de.wikipedia.org/wiki/Zylinderspule ) can be used.

2. 3D Printing and Accelerator Design

* Professor reiterated the goal: to develop an efficient accelerator, not just focus on the tube design. Tasks that must be completed to pass the project are listed in the pdf "Marble Accelerator Project" (p.3 "Tasks") which was presented in the Kickoff-Meeting and uploaded to Moodle at the beginning of the project in april.
* Advised to begin prototyping the accelerator.
* The current 3D modular design presented is having 75 to 85% success rate.

In the remodeling discussion:

* Emphasized the need to consider space for the marble to come to rest.
* Discussed forces acting on a marble at rest.
* Demonstrated a basic graph and force equation to estimate the minimum current needed to move the marble from rest.

3. Data Visualization
   
* Professor provided the following suggestions:
* Adjust x-axis scaling to reflect realistic project values.
* Replace current pulse animation of capacitor with a capacitor energy graph.
* Position graph should be in centimeters (cm), not meters.
* Time axis should be in milliseconds (ms).
* Graph should reset for each new data chunk to avoid overcrowding.
* Professor agreed on the use of wireless communication for data transfer but emphasized that the accelerator development must be prioritized.

4. Presentation Guidelines

* All missing PowerPoint presentations should be uploaded to Hessenbox.
* Reviewed checklist on GitHub regarding SI unit standards:
* Emphasized strict adherence in all presentations and reports.
  
Professor demonstrated:

* How to insert formulas in PowerPoint and the available formatting options.

Clarified usage of unit notations:

* Do not use parentheses (), square brackets [], or curly brackets {} for SI units, as it means multiplication, the unit of.., and the numerical value respectively.
*  Use a forward slash (/) instead.
* In mail, it was clarified by the professor regarding the usage of brackets.
* Detailed explanation on bracket usage is available in Chapter 7.1 / Page 15 of the PDF (link uploaded to GitHub).

5. Next Steps & Meeting Schedule

Due to upcoming exams:

* Next meeting to be postponed.
* Professor will be on holiday from July 25 for 3 weeks.
* Last available date for meeting before vacation: July 22.
* Target: Have the accelerator and prototype ready by then.
* Suggested to contact Shami for equipment requirements. Remark (Fabian): Shami has been informed that he can supply copper wire of a certain length /cross-section previously calculated by you (e.g. "20m of wire with 0.75mm diameter) for building accelerators. He will not issue any other components without prior consultation with me. Last opportunity to discuss this before my vacation: July 23rd.


# Meeting 2025-06-17

Location: A3.2.08 Time: 11:30 am

Minutes Made by Smit

- Participants:
- Varshini Barallu Manjunath
- Rohith Joy
- Murtuza Udaipurvala
- Abdul Manaf Mansoor
- Anisha Bhanderi
- Smit Patel
- Professor Mink



- Coil wire diameter calculation were presented by murtaza.
  Professor said calculation seems correct but also calculate inductance and time constant for wire diameter.

  Feedback by professor on presentation and slides.

  Introductory slides and presentation
    

- First part of presentation and slides were good.
- Phase slides were good but have been improved by adding key points.
- In simulation formula symbols were missing. (eg. for turns write N.)
- Not proper explaination for the data for eg. Coil inner radius and coil length.
  Explain values in image with arrow mark so everybody can understand.
- How to calculate force on marble explain this part in slide.
- In matlab simulation slide explain what final values are we getting and add explaination for velocity
  and position block with marking.
 - For coil wire optimization it coulbe better if photo of coil and marble accleration were provided
   at the beginning.
 - Title of STM32 should not be reprogramming.
 - For data visualization pictures could be better.
 - Coil carrier design will not work because of coil mount. Marble will not comes out from coil.

   Overall feedback by prefessor on presentation.

- Explain content of slides properly and give enough time to read slides.
- For 15 mins of presentation there should be 12 slides.
- If all are agree then we can do small presentation before final one to get feedback from professor.

  Next week's Agenda and meeting minutes will be done by Abdul Manaf. He will also give a short overview of the agenda at the beginning (2 to 3min)


   
# Intermediate meeting  2025-06-15

Location: Steinkaute , Friedberg Time: 1 pm

Minutes made by Smit

- Participants:
- Varshini Barallu Manjunath
- Rohith Joy
- Murtuza Udaipurvala
- Abdul Manaf Mansoor
- Anisha Bhanderi
- Smit Patel

Agenda :
About mid term presentation/ presentation slides and dividing tasks/discussion about overview of project 
and future work.



Phase-1
In this phase we discuss about tasks which was compulsory for all students.
-3D - Modeling of coil carrier
-FEMM Magnetic simulation and calculation based on that.

Phase-2

Brainstorming

In this phase we had discussion about what new things we are doing in project and what results we had achieved so far.
- Hall effect sensor design by Varshini and Rohith.
- Matlab simulation for overall system by Murtaza.
- Data visualization using Python matplot liberary by Anisha and Manaf.
- Coil wire optimization and calculation for it by Smit.
- Redesign of Coil carrier by Rohith and Varshini.
- STM32 Reprogramming by Murtaza.

  Phase -3

  Future Work
  
  In this phase we had discussion about task which are still pending and ideas needed for it.
  - Coil carrier and hall effect sensor designs are still not confirmed.
  - Power electronics for overll circuit. there is still some calculation we have to do for
    capacitance.
    
   
  
  
  

# Meeting 2025-06-03

Location: A3.2.08 Time: 10:00 am

Minutes Made by Anisha

- Participants:
- Varshini Barallu Manjunath
- Rohith Joy
- Murtuza Udaipurvala
- Abdul Manaf Mansoor
- Anisha Bhanderi
- Smit Patel
- Professor Mink
- Professor Klein
  
Anisha Bhanderi
* Overview of the Agenda explained

Discussed Topics

Anisha and Manaf 

* Data visualization of CSV, before using JSON format
* Made changes in the Python code according to the JSON data structure
* Explained the code used for plotting
* Visualized the data on Matplotlib and showed the result in graphs 

Feedback by Professor:

* Change the range of the 2nd graph, no need to use delta
* Change the JSON structure to reduce the number of bytes used
* Do not use unarranged putty values in future presentations

Smit Patel

* Selected coil wire of diameter 0.2 mm
* Reasons behind choosing thin wire: More number of turns, higher resistance, Stronger magnetic field
* Inductance is calculated by using a lua script
* Explained the calculation for resistance after changing the number of turns with a thinner wire.

Feedback by Professor:

* Question was asked: Why do you use thinner wire if you are not increasing the number of turns as expected?
* Higher resistance is not good. If resistance is higher, then we have to generate more energy, and for storing energy, capacitors with higher capacitance will be needed.
* Feedback for slides: Use units for each value. (website will be provided by Prof)
* For slides, containing more formulas: Write in more arranged way, it should not be concentrated at one place. Use a subscript when needed

Murtuza

* Saved sample data in a buffer and sent it on the UART in JSON format.
* Scheduling Systick for every 1 ms interrupt.
* Configuring the Timer to generate data every 0.1 ms interrupt. Timer is running at 10 KHz.
* Further tasks: Detecting Marble entry with Hall Effect sensor, Calculating Marble velocity. 

Feedback by professor:

*	For JSON data structure: Use array of values for all three data. By doing so, less number of bytes will be used and it will be easy to extract data for the other subteam.
*	While using readp and writep, a race condition can create a problem, which can lead to missing data or changing and getting the wrong data.
*	Same with send_data_flag as well

Rohit and Varshini

* 3D model for testing and tuning the hall effect sensor: to detect the position and calculate the speed
* For sensor placement: measured the sensor and keep a bit more space for ease
* Three differently inclined (10,20,30 degrees) models to check the change in speed
* Coil carrier to redirect marble right-angle upwards
* Two sensors placement: one on the center of coil winding and other one on the top
* Suggestion of using two windings: One where the marble enters and other one from where the marble goes out
* Concerns:

    o	Whether we can throw a marble to the top
  
    o	If we increase speed, it can damage the edges of the coil carrier at log run
  
    o	Which one will be better: right-angle coil carrier or inclined at some angle

Feedback by Prof Klein:

*	Got a general overview of the work, understood sketches
*	Question related to calculation: What will be the force to send the marble on top? What will be the speed of the marble?

Feedback by Prof Mink:

* Do some calculations like height, force, energy, speed of a marble, etc. It should be a priority to understand physical functionality
* Question: Why is there a square shape design (the same as winding design) on the top?
  Answered by Rohit: If one coil winding is not able to generate energy, then it will be easy to design a second winding design
* There should be one more sensor, to detect when the marble enters 

Professors' Overall instruction:

* Think of different coil carrier design
* Include name and slide number on slides from the next meeting
* Font size should be the same for all (16 px)
* For code, do not use black background. Try to use white to make it easily visible
* If the code is important and you want to explain it, then only include it in slides
* Before the presentation, merge all slides and upload to Hessenbox

Discussion about different designs of coil carrier:
* In vertical structure, there will be space where marble can rest. Therefore, there will not be a requirement to use a sensor at the entrance, to detect when marble enters
* The same idea can be implemented for inclined structures
* Compared to inclined structures, vertical structures need less force, because friction will be less in vertical structures

Feedback and suggestions by Prof Klein:

* It looks like team members are not connected; all are working just for their own part of the project.
* Start working as a team, there should be an idea of who is working on which part of the project
* Write a To-Do list and interface in every meeting
* What can be done to go to performing stage from storming phase?
* Use strategy of three flags

    o	Green flag – work has been done in time
  
    o	Yellow flag – work has not been done in time
  
    o	Red flag – work has not been started yet
*	Be responsible for your part of the project, while keeping a general idea about the whole project
*	Discuss in a team, each member should know some points: Definition of project, work packages, milestones, and what a common target is.

Next week's Agenda and meeting minutes will be done by Smit Patel. He will also give a short overview of the agenda at the beginning (2 to 3min)


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

