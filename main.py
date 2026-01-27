import cv2
from PIL import Image
import numpy as np


images = {
    "hytale":"hytale.webp",
    "miku":"miku.png",
    "miku2":"mikuv2.webp",
    "shape":"Dodecahedron.png",
    "mikupng":"mikuv2.png"
}

if __name__ == "__main__":
    print("hello")
    img = cv2.imread(images["shape"], cv2.IMREAD_UNCHANGED)
    #blurred = cv2.GaussianBlur(img, (3,3), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    edges = cv2.ximgproc.thinning(edges)
    cv2.namedWindow('Grayscale', cv2.WINDOW_NORMAL)
    cv2.imshow('Grayscale', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
