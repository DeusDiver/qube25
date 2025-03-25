import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from std_msgs.msg import String

class PIDControllerNode(Node):
    def __init__(self):
        super().__init__('pid_controller_node')

        # Initialiser PID-controlleren med noen tilfeldige verdier
        self.controller = pidController(p=1.0, i=0.1, d=0.01, reference=10.0)

        # Publisher for å sende spenningen (voltage)
        self.publisher = self.create_publisher(Float64, 'input_voltage', 10)

        # Subscriber for å motta målte verdier (measured_angle)
        self.subscription = self.create_subscription(
            Float64,
            'angle',
            self.measurement_listener,
            10
        )

    def measurement_listener(self, msg):
        # Oppdater PID-controlleren med den målte verdien
        measured_value = msg.data
        voltage = self.controller.update(measured_value)

        # Publiser oppdatert spenning
        voltage_msg = Float64()
        voltage_msg.data = voltage
        self.publisher.publish(voltage_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PIDControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


class pidController:
    def __init__(self, p, i, d, reference):
        self.p = p
        self.i = i
        self.d = d
        self.reference = reference
        self.voltage = 0.0
        self.previous_error = 0.0
        self.integral = 0.0

    def update(self, measured_value):
        error = self.reference - measured_value
        self.integral += error
        derivative = error - self.previous_error
        self.voltage = self.p * error + self.i * self.integral + self.d * derivative
        self.previous_error = error
        return self.voltage

#######################################################################################################