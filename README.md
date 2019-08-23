# Motor Skills Trace Game
A simple game designed to test participants motor skills

[![Gameplay 1](https://github.com/mattman1/motor_skills_trace_game/blob/master/images/Game1.png)]()
[![Gameplay 2](https://github.com/mattman1/motor_skills_trace_game/blob/master/images/Game2.png)]()
[![Gameplay 3](https://github.com/mattman1/motor_skills_trace_game/blob/master/images/Game3.png)]()

## Hardware
This program is designed to work with National Instruments USB DAQ devices. This game has been tested with the NI USB-6002 DAQ device, although it should work with other NI DAQ units.
Before continuning ensure you have a NI DAQ unit. Or feel free to modify the code to work with your desired DAQ unit.

## Installing
First install the latest version of Python, if it is not already installed.
```
https://www.python.org/downloads/
```
When installing Python ensure that the option to add Python to PATH is checked. 

[![Install Python](https://github.com/mattman1/motor_skills_trace_game/blob/master/images/InstallPython.png)]()

Once Python is installed we will need to install the following Python packages.
- nidaqmx
- pygame
- math
- statistics
- random

Some of these packages may already be installed. If they must be installed use pip install "package name" on the windows command line.

## Usage
1. Select a target file or load a configuration

[![Gameplay 3](https://github.com/mattman1/motor_skills_trace_game/blob/master/images/SelectTraceFile.png)]()

2. Click get MVC to get the participants MVC. The target positions will scale to this MVC value

3. Click Start Trace Tests to begin the game 

[![Gameplay 3](https://github.com/mattman1/motor_skills_trace_game/blob/master/images/StartTest.png)]()

4. The graphical trace file creator can be used to make your own custom trace filess
