# ServoBench_GUI_modules

[tag:Pyside] [tag:QtDesigner, UDP, json]

[tag:javascript]


The repository contains the GUI modules for the motion simulation bench software.

The GUI is designed in Qt Designer, with the PySide 6 framework. The simulator is connected to the PC from the controller via a patch cord, data packets transfer from the PC to the controller is implemented on the UDP protocol. Stationary and software operation modes are implemented in the software. To store modes, settings, etc. are used json files. The software saves logs in csv, builds graphs in real time

![2022-09-23_15-46-07](https://user-images.githubusercontent.com/68301720/193608635-116d434c-6fc3-4452-985c-05270ae9821d.png)

![2022-09-23_15-47-00](https://user-images.githubusercontent.com/68301720/193608702-259db111-bba6-4cc8-bcdb-87057f687d1a.png)

![2022-09-23_15-47-18](https://user-images.githubusercontent.com/68301720/193608716-b3542e25-8c1b-4449-afeb-c91c0e52f824.png)

