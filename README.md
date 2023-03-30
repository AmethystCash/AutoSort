# AutoSort

### The problem

As students, we noticed a growing problem in our university cafeteria. People would often have trouble with recycling and picking the right bin to throw their trash into. Nowadays those bins aren't available to us, we have to leave all of the trash in one general bin which then gets sorted by other workers. 

### The solution

AutoSort! A bin that can automate the process of sorting rubbish for you. It does so by utilizing:
1. A barcode scanner
2. Machine vision

### The setup

We're using a RaspberryPi to run our scripts. That part is located in our 3d-printed bin. You can see our initial design down below.

![alt text](./readme-images/bin-sketch.jpg)

To actually make the flaps move we're going to use linear actuators.














### How does it work?

Each frame we check if there's something in the bin, with either a sensor, a fuzzy search, or more machine vision. We then look for a barcode, if nothing is found we ask our Machine vision API to provide us that information. Then the bin opens one of its compartments for the rubbish to fall into. Here's a flow-chart ilustrating that process:

![alt text](./readme-images/code-graph.png)

The barcode part is made possible by https://world.openfoodfacts.org/.

The machine vision part by https://huggingface.co/yangy50/garbage-classification.




### How to get started?

(improve code further and explain how to get started)

### AutoSort in action

(videos and images of autosort doing autosort)

### Roadmap

(insert a roadmap)
