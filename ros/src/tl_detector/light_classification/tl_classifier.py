from styx_msgs.msg import TrafficLight
import cv2

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        pass

    def find_circles(self, bw_image):
        img = cv2.GaussianBlur(bw_image, (5, 5), 0)
        min_radius = bw_image.shape[0] / 200
        max_radius = bw_image.shape[0] / 20
        min_distance = min_radius * 6
        circles = cv2.HoughCircles(img,
                                   cv2.HOUGH_GRADIENT,
                                   1,
                                   minDist = int(min_distance),
                                   param1=50,
                                   param2=10,
                                   minRadius=int(min_radius),
                                   maxRadius=int(max_radius))
        if circles is not None:
            return circles
        else:
            return []

    def count_red_circle(self, hsv):
        red_lower_mask = cv2.inRange(hsv, (0,160,160), (10,255,255))
        red_upper_mask = cv2.inRange(hsv, (170,160,160), (180,255,255))
        mask = red_lower_mask | red_upper_mask
        circles = self.find_circles(mask)
        return len(circles)

    def count_yellow_circle(self, hsv):
        mask = cv2.inRange(hsv, (20,160,160), (40, 255,255))
        circles = self.find_circles(mask)
        return len(circles)

    def count_green_circle(self, hsv):
        mask = cv2.inRange(hsv, (55,160,160), (75, 255,255))
        circles = self.find_circles(mask)
        return len(circles)

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        rcount = self.count_red_circle(hsv_img)
        ycount = self.count_yellow_circle(hsv_img)
        gcount = self.count_green_circle(hsv_img)

        if rcount == 0 and ycount == 0 and gcount == 0:
            return TrafficLight.UNKNOWN

        if rcount > ycount and rcount > gcount:
            return TrafficLight.RED

        if ycount > rcount and ycount > gcount:
            return TrafficLight.YELLOW

        if gcount > rcount and gcount > ycount:
            return TrafficLight.GREEN

        return TrafficLight.UNKNOWN
