# Captcha

## General
This exhibit allows to take your photograph, and show it rendered as a matrix of digit images from 0 to 9.
Then, by allowing the user to change the brightness of the image, digits are replaced to create the designated brightness effect.
It is designed to work with a button to take the photo and a dial that sets the brightness, which in turn simulate keyboard commands to the exhibit.

## Installation & Run
The exhibit runs using python 3 on linux, using the opencv library (known as cv2). 

After the latest python 3 installation, use:

```
pip3 install numpy
pip3 install imutils
pip3 install opencv-python
```

To install all necessary packages.

Then, to run, go to the root project dir and run:

```
python3 captcha.py
```

## Log
The exhibit supports a rotating log named captcha-dc.log in the root directory, that logs the following events:
* INIT (exhibit was started and initalization is done)
* IMAGE_CAPTURED (a live camera image was captured, following a space char sent from keyboard)
* BRIGHTNESS_CHANGED,N (brightness was changed by an input of '0' to '9' resulting in a brightness number N, with 6 being no change, 5, 4, 3, 2, 1 going darker and 7, 8, 9, 10 going lighter)


## Keyboard Input Interface
For simplicity, the exhibit simply reacts to keyboard.
Then, by having the button and dial simulate keyboard inputs, no special code is needed in the exhibit itself.

The exhibit reacts to the following keyboard characters:

When it runs, it always shows the camera live input on the left part of the screen.
Then, when the **space** character is pressed on the keyboard, an image is captured, and displayed on the screen, grayscaled and in neutral brightness.
Next to it, the digit-effect image is shown.
Now, if the chars **'0'** to **'9'** are sent, the brightness is updated accordignly, and both images on the right hand side are updated.

**Important note:** the '0' char represents brightness 10, and '1' to '9' represent 1 to 9 respectively.
6, which is the default brightness, is a neutral brighness, with 7, 8, 9 and 10 going brighter, and 5, 4, 3, 2, 1 going darker.

At any time, another space character can be received to replace the current image with an updated live camera one.

Finally, a keyboard input of the **'q'** character quits the exhibit (this is intended to be used with an actual keyboard if wanting to stop the exhibit software from running).
