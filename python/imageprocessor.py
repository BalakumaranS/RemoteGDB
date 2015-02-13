import cv2
import numpy as np


def threshold(img, min, max, type):
    return cv2.threshold(img, min, max, type)


def morphology(img, type, kernel):
    return cv2.morphologyEx(img, type, kernel)


def erode(img, kernel, iterations):
    return cv2.erode(img, kernel, iterations = iterations)


def dilate(img, kernel, iterations):
    return cv2.dilate(img, kernel, iterations = iterations)


def image_enhance(imgname):
    img = cv2.imread(imgname, 0)

    #Binary thresholding
    t1,b1 = threshold(img, 160, 255, cv2.THRESH_BINARY)
    cv2.imwrite('b1.jpeg',b1)

    #Gaussian blur + Otsu's thresholding
    #blur1 = cv2.GaussianBlur(img,(5,5),0)
    #cv2.imwrite('blur1.jpeg',blur1)
    #t1,b1 = threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imwrite('b1.jpeg',b1)

    #Morphology close
    kernel = np.ones((5,5), np.uint8)
    c1 = morphology(b1, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(imgname, c1)

if __name__ == "__main__":
    image_enhance('capture/16/16.jpeg')