import numpy as np
import imutils
import cv2

from log import Log


class Captcha:

    STREAM_IMAGE_POS_X = 186
    REAL_IMAGE_POS_X = 779
    DIGITS_IMAGE_POS_X = 1239

    DESTINATION_IMAGE_SIZE = (460, 820)
    DESTINATION_IMAGE_SAMPLED_SIZE = (46, 82)

    IMAGES_Y = 221

    @staticmethod
    def get_brightness_offset_by_number(number):
        if number == 6:
            return 0

        if number < 6:
            return -1 * ((6 - number) * (128 / (6 - 1)))

        return (number - 6) * (128 / (10 - 6))

    @staticmethod
    def get_index_by_value(value):
        index = int(value / (255 / 10))
        if index == 10:
            return 0

        return 9 - index

    def __init__(self):
        self.digit_images = []
        self.brightness_number = 6
        self.source_image = None
        self.taken_image = None
        self.taken_digits_image = None
        self.numbers_image = None
        self.background = None
        self.window_name = 'captcha'

    def get_gray_downscaled(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightened_gray_image = cv2.add(gray_image, self.get_brightness_offset_by_number(self.brightness_number))
        gray_resized_image = cv2.resize(brightened_gray_image, self.DESTINATION_IMAGE_SIZE)
        gray_downscaled_image = cv2.resize(gray_resized_image, self.DESTINATION_IMAGE_SAMPLED_SIZE)

        return gray_downscaled_image

    def start(self):
        Log.init('./captcha-dc.log', 'CAPTCHA-DC')

        Log.info('INIT')

        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.background = cv2.imread('assets/bg.png')

        for i in range(0, 10):
            self.digit_images.append(cv2.imread('assets/' + str(i) + '.jpg'))

        cap = cv2.VideoCapture(0)

        while True:
            cv2.imshow(self.window_name, self.background)

            _, image = cap.read()
            rotated_image = imutils.rotate_bound(image, 90)
            curr_gray_downscaled_image = self.get_gray_downscaled(rotated_image)

            scaled_image = cv2.resize(rotated_image, self.DESTINATION_IMAGE_SIZE)
            self.background[self.IMAGES_Y:self.IMAGES_Y + scaled_image.shape[0], self.STREAM_IMAGE_POS_X:self.STREAM_IMAGE_POS_X + scaled_image.shape[1]] = scaled_image

            if self.taken_image is not None:
                self.background[self.IMAGES_Y:self.IMAGES_Y + scaled_image.shape[0], self.REAL_IMAGE_POS_X:self.REAL_IMAGE_POS_X + scaled_image.shape[1]] = self.taken_image

            if self.taken_digits_image is not None:
                self.show_digits_image(self.taken_digits_image)

            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                self.taken_digits_image = curr_gray_downscaled_image
                self.taken_image = scaled_image
                self.source_image = rotated_image
                Log.info('IMAGE_CAPTURED')
            elif ord('0') <= key <= ord('9'):
                if key == ord('0'):
                    self.brightness_number = 10
                else:
                    self.brightness_number = key - ord('0')
                self.taken_digits_image = self.get_gray_downscaled(self.source_image)
                scaled_image = cv2.resize(self.source_image, self.DESTINATION_IMAGE_SIZE)
                brightness = self.get_brightness_offset_by_number(self.brightness_number)
                added_image = np.zeros((scaled_image.shape[0], scaled_image.shape[1], 3), np.uint8)
                if brightness < 0:
                    brightness = abs(brightness)
                    added_image[:, :] = (brightness, brightness, brightness)
                    self.taken_image = cv2.subtract(scaled_image, added_image)
                else:
                    added_image[:, :] = (brightness, brightness, brightness)
                    self.taken_image = cv2.add(scaled_image, added_image)
                Log.info('BRIGHTNESS_CHANGED', str(self.brightness_number))
            elif key == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def show_digits_image(self, image):
        curr_image = None
        for i in range(0, image.shape[0]):
            curr_row = None
            for j in range(0, image.shape[1]):
                index = self.get_index_by_value(image[i][j])
                digit_image = self.digit_images[index]
                if curr_row is None:
                    curr_row = digit_image
                else:
                    curr_row = np.concatenate((curr_row, digit_image), axis=1)

            if curr_image is None:
                curr_image = curr_row
            else:
                curr_image = np.concatenate((curr_image, curr_row), axis=0)

        self.background[self.IMAGES_Y:self.IMAGES_Y + curr_image.shape[0], self.DIGITS_IMAGE_POS_X:self.DIGITS_IMAGE_POS_X + curr_image.shape[1]] = curr_image


if __name__ == '__main__':
    Captcha().start()
