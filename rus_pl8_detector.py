from thumbor.detectors.local_detector import CascadeLoaderDetector
from thumbor.point import FocalPoint
from thumbor.utils import logger

class Detector(CascadeLoaderDetector):

    def __init__(self, context, index, detectors):
        super(Detector, self).__init__(context, index, detectors)
        self.load_cascade_file(__file__, '/usr/src/app/haarcascade_licence_plate_rus_16stages.xml')

    def detect(self, callback):
        try:
            features = self.get_features()
        except Exception as e:
            logger.exception(e)
            logger.warn('Error during face detection; skipping to next detector')
            self.next(callback)
            return

        if features:
            for (left, top, width, height), neighbors in features:
                self.context.request.focal_points.append(
                    FocalPoint.from_square(left, top, width, height, origin="Russian Plate Detection")
                )
            callback()
        else:
            self.next(callback)