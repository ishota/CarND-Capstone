import rospy
from yaw_controller import YawController
from pid import PID
from lowpass import LowPassFilter

GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self,
                 vehicle_mass,
                 fuel_capacity,
                 brake_deadband,
                 decel_limit,
                 accel_limit,
                 wheel_radius,
                 wheel_base,
                 steer_ratio,
                 max_lat_accel,
                 max_steer_angle):
        # TODO: Implement

        self.vehicle_mass    = vehicle_mass
        self.fuel_capacity   = fuel_capacity
        self.brake_deadband  = brake_deadband
        self.decel_limit     = decel_limit
        self.accel_limit     = accel_limit
        self.wheel_radius    = wheel_base
        self.wheel_base      = wheel_base
        self.steer_ratio     = steer_ratio
        self.max_lat_accel   = max_lat_accel
        self.max_steer_angle = max_steer_angel

        # Controller
        self.yaw_controller = YawController(wheel_base, steer_ratio, 0.1, max_lat_accel, max_steer_angle)
        self.throttle_controller = PID(0.3, 0.1, 0.1)

        # Lowpass filter
        self.vel_lpf = LowPassFilter(0.5, 0.05)
        self.yaw_lpf = LowPassFilter(0.5, 0.05)

        self.last_vel = 0
        self.last_time = rospy.get_time()

    def control(self, *args, **kwargs):
        # TODO: Change the arg, kwarg list to suit your needs

        if not dbw_enabled:
            self.throttle_controller.reset()
            self.vel_lpf.reset()
            self.yaw_lpf.reset()
            return 0.,0.,0.
        
        current_vel = self.vel_lpf.filt(current_vel)

        steering = self.yaw_controller.get_steering(linear_vel, angular_vel, current_vel)
        steering = self.yaw_lpf.filt(steering)

        velocity_error = linear_vel - current_vel
        self.last_vel  = current_vel

        current_time   = rospy.get_time()
        sample_time    = current_time - self.last_time
        self.last_time = current_time

        throttle = self.throttle_controller.step(velocity_error, sample_time)

        if linear_vel == 0 and current_vel < 0.1:
            throttle = 0
            brake = 700
        elif throttle < 0.1 and velocity_error < 0:
            throttle = 0
            decel = max(velocity_error, self.decel_limit)
            brake = abs(decel) * self.vehicle_mass * self.wheel_radius
        else
            brake = 0

        # Return throttle, brake, steer
        return 1., 0., 0.
