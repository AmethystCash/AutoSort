# AutoSort

### The problem

As students, we noticed a growing problem in our university cafeteria. People would often have trouble with recycling and picking the right bin to throw their trash into. Nowadays those bins aren't available to us, we have to leave all of the trash in one general bin which then gets sorted by other workers. 

## The solution

AutoSort! A bin that can automate the process of sorting rubbish for you. It does so by utilizing machine vision and a garbage classification model from HuggingFace.

## The setup

We're using a RaspberryPi 4 to run our scripts. That part is located in our 3d-printed bin. You can see our initial design down below.

![bin sketch](./readme-images/bin-sketch.jpg)

To take pictures of the trash that falls in the bin we're currently using a regular webcam. We're planning to upgrade it to a picamera in the future.

To open and close the individual doors we use servos.

## SolidWorks models 

Models of proposed bin design can be found in the SolidWorks folder. The STL files directory contains .stl exports that can be opened without SolidWorks. The Parts directory contains all of the individual parts as .SLDPRT files. The Assembly/Parts directory contains a final assembly and the referenced parts which are all dupilcates of what's in the Parts directory. 

Exporting from solidworks can be inconsistent, if you are unable to view the parts please see the YouTube video under [AutoSort in action](#autosort-in-action) along with the .stl files.

## How does it work?

Every time the bin is opened we will take a snapshot of what's in the bin. We then send that image to a garbage classificaion model which tells us the packaging information. Then the bin opens one of it's compartments for the rubbish to fall into. In addition to that we also send the information to discord, and firebase for data analysis and visualization. 

Here's a flow-chart ilustrating that process:

![code flow-chart](./readme-images/code-graph-new-whitebg.jpg)



  
## How to get started?

1. Clone the repository.
2. Make sure that you have some kind of a camera/webcam connected to your device.
3. Install all the necessary packages:
  - `os`
  - `time`
  - `threading`
  - `colorama`
  - `inflect`
  - `reqests`
  - `json`
  - `opencv-python`
  - `gradio`
  - `gpiozero`
  - `firebase_admin`
  - `python-dotenv`
4. Create a `.env` file.
5. Add an `API_KEY = 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` line to it (in case it fails, you can generate a new prototyping API key from the HuggingFace link provided [here](https://huggingface.co/yangy50/garbage-classification)).
6. You can now run the `main_testing.py` file.

### Disclaimer: 

With that you won't be able to use our discord webhook/firebase features. If you wish to experience the live webhook feature follow the next few steps:

7. Create a discord server.
8. Add a webhook in one of your discord channels.
9. Copy the webhook key and paste a `WEBHOOK_URL = your webhook url goes here add it here` line to the `.env` file.

Now you can see live updates from AutoSort in discord!

## AutoSort in action

(videos and images of autosort doing autosort, coming soon)

## Roadmap

1. Convert precise type of rubbish to(for example can, bottle or paper) to which bin should open.
2. 3D Print the model of the bin
3. Change from using space bar as a trigger to using the door sensor.
4. First full deploy 

## Credits
- yangy50, for the garbage classification model, you can check it out here: https://huggingface.co/yangy50/garbage-classification.
