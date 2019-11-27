import numpy as np
import cv2

def get_index_by_value(value):
    index = int(value / (255 / 10))
    if index == 10:
        return 0
    else:
        return 9 - index

def show_digits_image(image):
    curr_image = None
    for i in range(0, image.shape[0]):
        curr_row = None
        for j in range(0, image.shape[1]):
            index = get_index_by_value(image[i][j])
            digit_image = digit_images[index]
            if curr_row is None:
                curr_row = digit_image
            else:
                curr_row = np.concatenate((curr_row, digit_image), axis=1)

        if curr_image is None:
            curr_image = curr_row
        else:
            curr_image = np.concatenate((curr_image, curr_row), axis=0)

    cv2.imshow('numbers', curr_image)

digit_images = []
for i in range(0, 10):
    digit_images.append(cv2.imread('assets/' + str(i) + '.jpg'))

cap = cv2.VideoCapture(0)

while(True):
    _, image = cap.read()
    resized_image = cv2.resize(image, (800, 600))

    gray_resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    gray_downscaled_image = cv2.resize(gray_resized_image, (80, 60))

    cv2.imshow('frame', resized_image)

    show_digits_image(gray_downscaled_image)

    cv2.imshow('downscale', gray_downscaled_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
