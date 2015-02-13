import itertools,math,operator,time
import Image,ImageChops

def ImgToPix(Img):
    """
    Returns a Pixel Access Object which behaves like a 2-dimensional array of pixels.
    Example: ImgToPix(Image.open('image.png'))
    """
    return Img.load()

def ImgSize(Img):
    """
    Returns a tuple containing (width,height) of the Image
    Example: ImgSize(Image.open('image.png'))
    """
    return Img.size

def PixToTuple(PixObj,ImgSizeTuple):
    """
    Returns a tuple of pixel values from a pixel access object created using ImgToPix() function
    """
    _width = ImgSizeTuple[0]
    _height = ImgSizeTuple[1]
    _ImgList = []
    for row,column in itertools.product(range(_width),range(_height)):
        _ImgList.append(PixObj[row,column])
    _ImgTuple = tuple(_ImgList)
    return _ImgTuple

def ImgMinPix(ImgTuple):
    """
    Returns the minimum pixel value in the image tuple obtained from PixToTuple() function
    """
    return min(ImgTuple)

def ImgMaxPix(ImgTuple):
    """
    Returns the maximum pixel value in the image tuple obtained from PixToTuple() function
    """
    return max(ImgTuple)

def ImgDiff(img1,img2):
    """
    Computes the difference between Img1 and Img2, and gets the bounding box of non-zero regions in the difference image.
    Returns a tuple containing (left,upper,right,lower) of the non-zero regions if Img1 and Img2 are different or None if Img1 and Img2 are identical.
    """
    Img1 = Image.open(img1)
    Img2 = Image.open(img2)
    diff = ImageChops.difference(Img1,Img2).getbbox()
    return diff

def ImgSimilar(img1,img2):
    """
    Computes the degree of similarity between Img1 and Img2 and returns the RMS (Root Means Squared) value of the absolute difference
    """
    Img1 = Image.open(img1)
    Img2 = Image.open(img2)
    Img1Hist = Img1.histogram()
    print Img1Hist
    Img2Hist = Img2.histogram()
    print Img2Hist
    return math.sqrt(reduce(operator.add,map(lambda ImH1,ImH2: abs(ImH1-ImH2),Img1Hist,Img2Hist)) / (float(Img1.size[0]) * Img1.size[1]))

def ImgSave(Img,Name):
    """
    Saves Img in the Name given. The image will be saved by default in the directory in which the calling script is present.
    The default nature can be modified by providing destination directory along with the Name.
    """
    Img.save(Name)

def testVideoPresence(img1,img2):
    Img1 = Image.open(img1)
    Img2 = Image.open(img2)
    Img1Pix = ImgToPix(Img1)
    Img2Pix = ImgToPix(Img2)
    (Img1W, Img1H) = ImgSize(Img1)
    (Img2W, Img2H) = ImgSize(Img2)
    Img1Size = (Img1W, Img1H)
    Img2Size = (Img2W, Img2H)
    Img1Tuple = PixToTuple(Img1Pix,Img1Size)
    Img2Tuple = PixToTuple(Img2Pix,Img2Size)
    Img1MaxPix = ImgMaxPix(Img1Tuple)
    Img2MaxPix = ImgMaxPix(Img2Tuple)
    print Img1MaxPix,Img2MaxPix
    if Img1MaxPix < 40 and Img2MaxPix < 40:
        print "[Output:Black screen detected]"
    elif Img1MaxPix < 40 and Img2MaxPix > 40:
        print "[Output:Initially Black screen, later video running]"
    elif Img1MaxPix > 40 and Img2MaxPix < 40:
        print "[Output:Initially later video running, later Black Screen]"
    elif ImgDiff(img1,img2) is not None:
        print "[Output:Video running]"
    else:
        print "[Output: Video Freeze]"

def testImgSimilar(img1,img2):
	img_similar = ImgSimilar(img1,img2)
	return img_similar
