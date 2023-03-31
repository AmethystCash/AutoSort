# AutoSort

### The problem

As students, we noticed a growing problem in our university cafeteria. People would often have trouble with recycling and picking the right bin to throw their trash into. Nowadays those bins aren't available to us, we have to leave all of the trash in one general bin which then gets sorted by other workers. 

### The solution

AutoSort! A bin that can automate the process of sorting rubbish for you. It does so by utilizing a barcode scanner, Open Food Facts API and the Machine vision Garbage Classification API

### The setup

We're using a RaspberryPi 4 to run our scripts. That part is located in our 3d-printed bin. You can see our initial design down below.

![alt text](./readme-images/bin-sketch.jpg)

To open and close the individual bins we will use Linear Actuators



### How does it work?

Every time the bin is opened we will take a snapshot of what's in the bin. We then look for a barcode, if nothing is found we send a request to the Machine vision API to determine what's in the bin. Then the bin opens one of it's compartments for the rubbish to fall into. Here's a flow-chart ilustrating that process:

![alt text](./readme-images/code-graph.png)

Open Food Facts: https://world.openfoodfacts.org/.

Machine Vision Garbage Classification: https://huggingface.co/yangy50/garbage-classification.




### How to get started?

Download all of the Python Scripts

### AutoSort in action

(videos and images of autosort doing autosort)

### Roadmap

1. Convert precise type of rubbish to(for example can, bottle or paper) to which bin should open.
2. 3D Print the model of the bin
3. Change from using space bar as a trigger to using the door sensor.
4. First full deploy 
