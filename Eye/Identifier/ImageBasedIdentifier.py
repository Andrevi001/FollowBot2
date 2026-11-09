from Identifier.Identifier import Identifier
import config
import math
import Point

class ImageBasedIdentifier(Identifier):

    def _crop_around(self, frame, center: Point, length: int):
        """
        Crops a square with the specified side length, centered around the given point in the frame.
        
        Args:
            frame: numpy.array to be cropped
            center: Point center of the cropping, normalized value relative to frame.
            length: length of the square's side, measured in pixels.
        Returns:
            numpy.array containing the cropped area
        """

        img = frame.numpy_view()
        h, w = img.shape[:2]

        x = round(center.x * w) - length // 2
        y = round(center.y * h) - length // 2
        x1, y1 = x + length, y + length

        if x < 0 or y < 0 or x1 > w or y1 > h:
            return None

        return img[y:y1, x:x1]

    def _calculate_distance(self, point_a, point_b):
        """
        Used to calculate the distance between two given Point.
        The calculated distance is in pixels so it depends on the camera resolution (config.width, config.height.)
    
        Args:
            point_a: Point, the first point.
            point_b: Point, the second point.
        
        Returns:
            distance in pixels between point_a and point_b.
        """
    
        return math.dist([point_a.x * config.width, point_a.y * config.height], [point_b.x * config.width, point_b.y * config.height])