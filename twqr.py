import pyzbar
import threading
from PIL import Image
from pyzbar import pyzbar
import cv2


depro = './mode/detect.prototxt'
decaf = './mode/detect.caffemodel'
srpro = './mode/sr.prototxt'
srcaf = './mode/sr.caffemodel'
detector = cv2.wechat_qrcode_WeChatQRCode(depro, decaf, srpro, srcaf)  # 这四个参数可以不填，填上是为了识别一张图有多个二维码的情况

lock = threading.Lock()


def scan_qr_code(image_path, threshold=150):
    with lock:
        image = Image.open(image_path)  # 将二进制转为PIL格式图片
        image2 = cv2.imread(image_path)  # 将二进制转为cv格式图片
        # 将图像转换为灰度图
        gray_image = image.convert('L')
        # 将灰度图转换为二值图
        binary_image1 = gray_image.point(lambda x: 0 if x < threshold else 255, '1')
        binary_image2 = gray_image.point(lambda x: 255 if x < threshold else 0, '1')
        # binary_image1.show()
        # binary_image2.show()
        for i in binary_image1, binary_image2:
            # 优先尝试vxqr
            barcodes, points = detector.detectAndDecode(image2)  # 使用灰度图像将image换成gray
            if len(barcodes) != 0:
                return barcodes[0]
            # 不行再使用zbar
            barcodes = pyzbar.decode(i)
            if barcodes:
                for barcode in barcodes:
                    barcode_data = barcode.data.decode("utf-8")
                    return barcode_data
        else:
            return ""
