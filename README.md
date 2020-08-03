# cozmo-tensorflow
Cozmo the Robot learns to recognize everyday objects using TensorFlow.

![finder](assets/cozmo-detective.gif)

## The setup

Install the [Cozmo SDK](http://cozmosdk.anki.com/docs/)
```bash
virtualenv ~/.env/cozmo -p python3
source ~/.env/cozmo/bin/activate
git clone https://github.com/leapsky/tensorflow-maze.git
cd cozmo-tensorflow
pip install -r requirements.txt
```

## 1. Use Cozmo to generate training data

Getting enough training data for a deep learning project is often a pain. But thankfully we have a robot who loves to run around and take photos with his camera, so let's just ask Cozmo to take pictures of things we want him to learn. Let's start with a can of delicious overpriced seltzer. Place Cozmo directly in front of a bottle of seltzer, and make sure that he has enough space to rotate around the can to take some pictures. Be sure to enter the name of the object that Cozmo is photographing when you run the `cozmo-paparazzi` script.
```bash
python3 cozmo-paparazzi.py seltzer
```

![CozmoPaparazzi](assets/cozmo-paparazzi.gif)

Repeat that step for as many objects (categories) as you want Cozmo to learn! You should now see all your image categories as subdirectories within the `/data` folder.
