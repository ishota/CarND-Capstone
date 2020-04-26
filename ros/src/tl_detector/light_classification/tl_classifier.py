import cv2
import glob
import os
import numpy as np

# comment out to use main function
from styx_msgs.msg import TrafficLight


class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        self.red_lower_mask = [(0,164,160), (10,255,255)]
        self.red_upper_mask = [(170,164,160), (179,255,255)]
        self.yellow_mask = [(20,160,160), (40,255,255)]
        self.green_mask = [(50,164,160), (80,255,255)]

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

    def get_red_mask(self, hsv):
        red_lower_mask = cv2.inRange(hsv, self.red_lower_mask[0], self.red_lower_mask[1])
        red_upper_mask = cv2.inRange(hsv, self.red_upper_mask[0], self.red_upper_mask[1])
        mask = red_lower_mask | red_upper_mask
        return mask

    def get_yellow_mask(self, hsv):
        return cv2.inRange(hsv, self.yellow_mask[0], self.yellow_mask[1])

    def get_green_mask(self, hsv):
        return cv2.inRange(hsv, self.green_mask[0], self.green_mask[1])

    def count_red_circle(self, hsv):
        mask = self.get_red_mask(hsv)
        circles = self.find_circles(mask)
        return len(circles)

    def count_yellow_circle(self, hsv):
        mask = self.get_yellow_mask(hsv)
        circles = self.find_circles(mask)
        return len(circles)

    def count_green_circle(self, hsv):
        mask = self.get_green_mask(hsv)
        circles = self.find_circles(mask)
        return len(circles)

    def convert_hsv(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        hsv_img = self.convert_hsv(image)
        rcount  = self.count_red_circle(hsv_img)
        ycount  = self.count_yellow_circle(hsv_img)
        gcount  = self.count_green_circle(hsv_img)
        answer  = self.get_answer(rcount, ycount, gcount)

        if answer == 'UNKNOWN':
            return TrafficLight.UNKNOWN

        if answer == 'RED':
            return TrafficLight.RED

        if answer == 'YELLOW':
            return TrafficLight.YELLOW

        if answer == 'GREEN':
            return TrafficLight.GREEN

    def get_answer(self, rcount, ycount, gcount):

        if rcount == 0 and ycount == 0 and gcount == 0:
            return 'UNKNOWN'

        if rcount > ycount and rcount > gcount:
            return 'RED'

        if ycount > rcount and ycount > gcount:
            return 'YELLOW'

        if gcount > rcount and gcount > ycount:
            return 'GREEN'

        return 'UNKNOWN'

def main():

    TLC = TLClassifier()

    # reading images
    images = glob.glob(os.path.join("../../../../tfl_imgs/*.png"))
    num_images = len(images)
    img_list = []
    for i in range(num_images):
        img_list.append( cv2.imread(images[i]) )

    # convert BGR image to HSV image
    hsv_list = []
    for img in img_list:
        hsv_list.append( TLC.convert_hsv(img) )

    # mask green and find circle
    green_masked_list = []
    g_masked_img_list = []
    for hsv in hsv_list:
        masked_green = TLC.get_green_mask(hsv)
        green_masked_list.append( masked_green )
        g_masked_img_list.append( cv2.cvtColor(masked_green, cv2.COLOR_GRAY2BGR) )

    # mask yellow and find circle
    yellow_masked_list = []
    y_masked_img_list = []
    for hsv in hsv_list:
        masked_yellow = TLC.get_yellow_mask(hsv)
        yellow_masked_list.append( masked_yellow )
        y_masked_img_list.append( cv2.cvtColor(masked_yellow, cv2.COLOR_GRAY2BGR) )

    # mask red and find circle
    red_masked_list = []
    r_masked_img_list = []
    for hsv in hsv_list:
        masked_red = TLC.get_red_mask(hsv)
        red_masked_list.append( masked_red )
        r_masked_img_list.append( cv2.cvtColor(masked_red, cv2.COLOR_GRAY2BGR) )

    # save result
    result_img_list = []
    for i in range(num_images):
        img = img_list[i]
        hsv = hsv_list[i]
        g_masked_img = g_masked_img_list[i]
        y_masked_img = y_masked_img_list[i]
        r_masked_img = r_masked_img_list[i]
        rcount = TLC.count_red_circle(hsv)
        ycount = TLC.count_yellow_circle(hsv)
        gcount = TLC.count_green_circle(hsv)
        answer = TLC.get_answer(rcount, ycount, gcount)
        if answer is not 'UNKNOWN':
            cv2.putText(img, answer, (img.shape[1]/2, img.shape[0]/2), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 5, cv2.LINE_AA)

        result_img_list.append( cv2.hconcat([img, g_masked_img, y_masked_img, r_masked_img]))
        cv2.imwrite("../../../../tfl_imgs/result/" + answer + "_" + str(i+1) + ".png", result_img_list[i])

        cv2.imshow("image", result_img_list[i])
        cv2.waitKey(0)

if __name__ == "__main__":
    main()
