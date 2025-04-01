import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from rcl_interfaces.msg import SetParametersResult
from pid_controller_msgs.srv import SetReference  # Importer service-meldingen
import math

class PIDControllerNode(Node):
    def __init__(self):
        super().__init__('pid_controller_node')

        # Declare values
        self.declare_parameter('p', 1.0)
        self.declare_parameter('i', 0.0)
        self.declare_parameter('d', 0.01)
        self.declare_parameter('reference', 10.0)

        # Get values
        self.p = self.get_parameter('p').get_parameter_value().double_value
        self.i = self.get_parameter('i').get_parameter_value().double_value
        self.d = self.get_parameter('d').get_parameter_value().double_value
        self.reference = self.get_parameter('reference').get_parameter_value().double_value

        # Initialize PID controller
        self.controller = pidController(self.p, self.i, self.d, self.reference)

        # Callback to update parameters dynamically
        self.add_on_set_parameters_callback(self.parameter_callback)

        # Publish voltage
        self.publisher = self.create_publisher(Float64, 'input_voltage', 10)

        # Subscribe to 'measured_angle'
        self.subscription = self.create_subscription(
            Float64,
            'joint_state',
            self.measurement_listener,
            10
        )

        # ✅ Opprett en service-server for `set_reference`
        self.srv = self.create_service(SetReference, 'set_reference', self.set_reference_callback)

    def measurement_listener(self, msg):
        """Oppdater PID-kontrolleren med målt verdi."""
        measured_value = msg.data
        voltage = self.controller.update(measured_value)
        voltage_msg = Float64()
        voltage_msg.data = voltage
        self.publisher.publish(voltage_msg)

    def parameter_callback(self, params):
        """Callback for dynamisk oppdatering av PID-parametere."""
        for param in params:
            if param.name == 'p' and param.value >= 0.0:
                self.controller.p = param.value
                self.get_logger().info(f"Updated P to: {self.controller.p}")
            elif param.name == 'i' and param.value >= 0.0:
                self.controller.i = param.value
                self.get_logger().info(f"Updated I to: {self.controller.i}")
            elif param.name == 'd' and param.value >= 0.0:
                self.controller.d = param.value
                self.get_logger().info(f"Updated D to: {self.controller.d}")
            elif param.name == 'reference':
                self.controller.reference = param.value
                self.get_logger().info(f"Updated Reference to: {self.controller.reference}")
        return SetParametersResult(successful=True)  # Return a valid result

    def set_reference_callback(self, request, response):
        """✅ Callback for `set_reference`-servicen."""
        if -math.pi <= request.request <= math.pi:
            self.controller.reference = request.request
            self.get_logger().info(f"Setting reference to {self.controller.reference}")
            response.success = True
        else:
            self.get_logger().warn('Received invalid reference value!')
            response.success = False
        return response


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


def main(args=None):
    rclpy.init(args=args)
    node = PIDControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()