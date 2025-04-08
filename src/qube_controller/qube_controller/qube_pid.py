import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from rcl_interfaces.msg import SetParametersResult
from pid_controller_msgs.srv import SetReference
import math

class VelocityPIDControllerNode(Node):
    def __init__(self):
        super().__init__('velocity_pid_controller_node')

        # Deklarer PID-parametere
        self.declare_parameter('p', 10.0)
        self.declare_parameter('i', 0.01)
        self.declare_parameter('d', 0.0)
        self.declare_parameter('reference', 10.0)

        # Hent parameterne
        self.p = self.get_parameter('p').value
        self.i = self.get_parameter('i').value
        self.d = self.get_parameter('d').value
        self.reference = self.get_parameter('reference').value

        # Initialiser PID-kontrolleren
        self.controller = PIDController(self.p, self.i, self.d, self.reference)

        # Callback for dynamisk oppdatering av PID-parametere
        self.add_on_set_parameters_callback(self.parameter_callback)

        # Publisher for hastighets-pådrag til /velocity_controller/command (Float64MultiArray)
        self.publisher = self.create_publisher(Float64MultiArray, '/velocity_controller/commands', 10)

        # Abonner på /joint_states for å hente ut posisjon og hastighet
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Service for set_reference
        self.srv = self.create_service(SetReference, 'set_reference', self.set_reference_callback)

    def joint_state_callback(self, msg):
        if not msg.position:
            self.get_logger().warn("Ingen posisjonsdata mottatt!")
            return

        position = msg.position[0]
        velocity = msg.velocity[0] if len(msg.velocity) > 0 else 0.0

        # Det som reguleres
        measured_value = position  # alternativt: velocity

        # Oppdater PID-kontrolleren
        velocity_command = self.controller.update(measured_value)

        # Publiser hastighets-pådraget
        command_msg = Float64MultiArray()
        command_msg.data = [velocity_command]
        self.publisher.publish(command_msg)

        self.get_logger().info(f"P: {position:.3f}, V: {velocity:.3f}, Kommando: {velocity_command:.3f}")

    def parameter_callback(self, params):
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
        # Sjekk om referanseverdien er gyldig (her satt til [-pi, pi] som eksempel)
        if -math.pi <= request.request <= math.pi:
            self.controller.reference = request.request
            self.get_logger().info(f"Setter referanse til {self.controller.reference}")
            response.success = True
        else:
            self.get_logger().warn("Mottok ugyldig referanseverdi!")
            response.success = False
        return response

class PIDController:
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
