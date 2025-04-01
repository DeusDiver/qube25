import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from rcl_interfaces.msg import SetParametersResult
from pid_controller_msgs.srv import SetReference
import math

class VelocityPIDControllerNode(Node):
    def __init__(self):
        super().__init__('velocity_pid_controller_node')

        # Declare PID-parameterar
        self.declare_parameter('p', 1.0)
        self.declare_parameter('i', 0.0)
        self.declare_parameter('d', 0.01)
        self.declare_parameter('reference', 10.0)

        # Hent parameterar
        self.p = self.get_parameter('p').get_parameter_value().double_value
        self.i = self.get_parameter('i').get_parameter_value().double_value
        self.d = self.get_parameter('d').get_parameter_value().double_value
        self.reference = self.get_parameter('reference').get_parameter_value().double_value

        # Initialiser PID-kontrolleren
        self.controller = pidController(self.p, self.i, self.d, self.reference)

        # Callback for dynamisk oppdatering av PID-parametere
        self.add_on_set_parameters_callback(self.parameter_callback)

        # Opprett ein publisher for hastighets-pådrag til /velocity_controller/command
        self.publisher = self.create_publisher(Float64MultiArray, '/velocity_controller/command', 10)

        # Abonner på den målte verdien (endrar emnet etter kva som er aktuelt)
        self.subscription = self.create_subscription(
            Float64MultiArray,  # Forutsett at også måleverdien sendast som en liste med 1 element
            'measured_velocity',
            self.measurement_listener,
            10
        )

        # Opprett ein service-server for set_reference om nødvendig
        self.srv = self.create_service(SetReference, 'set_reference', self.set_reference_callback)

    def measurement_listener(self, msg):
        """Oppdater PID-kontrolleren med målte verdi og publiser hastighets-pådrag."""
        # Forvent at msg.data er ei liste med minst éin verdi
        if msg.data:
            measured_value = msg.data[0]
        else:
            measured_value = 0.0

        velocity_command = self.controller.update(measured_value)

        command_msg = Float64MultiArray()
        # Husk å pakke verdien inn i ei liste
        command_msg.data = [velocity_command]
        self.publisher.publish(command_msg)

    def parameter_callback(self, params):
        """Callback for dynamisk oppdatering av PID-parametere."""
        for param in params:
            if param.name == 'p' and param.value >= 0.0:
                self.controller.p = param.value
                self.get_logger().info(f"Oppdatert P til: {self.controller.p}")
            elif param.name == 'i' and param.value >= 0.0:
                self.controller.i = param.value
                self.get_logger().info(f"Oppdatert I til: {self.controller.i}")
            elif param.name == 'd' and param.value >= 0.0:
                self.controller.d = param.value
                self.get_logger().info(f"Oppdatert D til: {self.controller.d}")
            elif param.name == 'reference':
                self.controller.reference = param.value
                self.get_logger().info(f"Oppdatert Referanse til: {self.controller.reference}")
        return SetParametersResult(successful=True)

    def set_reference_callback(self, request, response):
        """Callback for `set_reference`-servicen."""
        if -math.pi <= request.request <= math.pi:
            self.controller.reference = request.request
            self.get_logger().info(f"Setter referanse til {self.controller.reference}")
            response.success = True
        else:
            self.get_logger().warn('Mottok ugyldig referanseverdi!')
            response.success = False
        return response


class pidController:
    def __init__(self, p, i, d, reference):
        self.p = p
        self.i = i
        self.d = d
        self.reference = reference
        self.previous_error = 0.0
        self.integral = 0.0

    def update(self, measured_value):
        error = self.reference - measured_value
        self.integral += error
        derivative = error - self.previous_error
        output = self.p * error + self.i * self.integral + self.d * derivative
        self.previous_error = error
        return output


def main(args=None):
    rclpy.init(args=args)
    node = VelocityPIDControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
