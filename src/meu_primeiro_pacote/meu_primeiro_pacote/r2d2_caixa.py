import rclpy
import numpy
import tf_transformations
import time
import math
from math import *
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Vector3

from rclpy.qos import QoSProfile, QoSReliabilityPolicy

class R2D2(Node):

    def __init__(self):
        super().__init__('R2D2')
        self.get_logger().debug ('Definido o nome do nó para "R2D2"')

        qos_profile = QoSProfile(depth=10, reliability = QoSReliabilityPolicy.BEST_EFFORT)

        self.get_logger().debug ('Definindo o subscriber do laser: "/scan"')
        self.laser = None
        self.create_subscription(LaserScan, '/scan', self.listener_callback_laser, qos_profile)

        self.get_logger().debug ('Definindo o subscriber do laser: "/odom"')
        self.pose = None
        self.create_subscription(Odometry, '/odom', self.listener_callback_odom, qos_profile)

        self.get_logger().debug ('Definindo o publisher de controle do robo: "/cmd_Vel"')
        self.pub_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)

        self.mestados = 0
        self.espera(0.8)
        self.distancia = 0.0
        self.distancia_r2d2 = 0.0
        self.angulo_r2d2 = 0.0

     def distancia_objetivo(self):
        objetivo = [9,9]
        self.distancia = math.dist((self.pose.position.x, self.pose.position.y), objetivo)
        
        self.angulo_r2d2 = math.atan2(9 - self.pose.position.x, 9 - self.pose.position.y)

    def espera(self, max_seconds):
        start = time.time()
        j = 0
        while j < max_seconds:
            j = time.time() - start            
            rclpy.spin_once(self)

    def listener_callback_laser(self, msg):
        self.laser = msg.ranges
       
    def listener_callback_odom(self, msg):
        self.pose = msg.pose.pose
    
    def run(self):
        self.get_logger().debug ('Executando uma iteração do loop de processamento de mensagens.')
        rclpy.spin_once(self)

        self.get_logger().debug ('Definindo mensagens de controde do robô.')
        self.ir_para_frente = Twist(linear=Vector3(x= 0.5,y=0.0,z=0.0),angular=Vector3(x=0.0,y=0.0,z= 0.0))
        self.parar          = Twist(linear=Vector3(x= 0.0,y=0.0,z=0.0),angular=Vector3(x=0.0,y=0.0,z= 0.0))

        self.get_logger().info ('Ordenando o robô: "ir para a frente"')
        self.pub_cmd_vel.publish(self.ir_para_frente)
        rclpy.spin_once(self)

        self.get_logger().info ('Entrando no loop princial do nó.')
        while(rclpy.ok):
            
            self.pose.position 
            self.pose.orientation
         
            _, _, yaw = tf_transformations.euler_from_quaternion([self.pose.orientation.x, self.pose.orientation.y, self.pose.orientation.z, self.pose.orientation.w])

            rclpy.spin_once(self)

            self.get_logger().debug ('Atualizando as distancias lidas pelo laser.')
            distancia_direita = numpy.array(self.laser[0:10]).mean()
            self.distancia_direita   = min((self.laser[  0: 80])) # -90° até -10° 
            self.distancia_frente    = min((self.laser[ 80:100])) # -10° até  10° 
            self.distancia_esquerda  = min((self.laser[100:180])) #  10° até 90° 
            
            cmd = Twist()
            self.e_angulo = self.angulo_r2d2 - yaw
            self.distancia_objetivo()
            

            if self.mestados == 0:
                if(abs(self.e_angulo) >= 0.06):
                    cmd.angular.z = 0.4
                    self.pub_cmd_vel.publish(cmd)
                    self.get_logger().info ('Virando para o objetivo')
                elif( self.distancia <= 3 and abs(self.e_angulo) <= 0.06):
                    self.mestados = 2                
                else:
                    cmd.angular.z = 0.0
                    self.pub_cmd_vel.publish(cmd)
                    self.get_logger().info ('olhando para o objetivo, distancia=' + str(self.distancia) + 'distancia_r2d2=' + str(self.pose.position.x)+ str(self.pose.position.y))
                    
                    self.mestados = 1
        
            elif self.mestados == 1:
                self.get_logger().info ('est = 1')
                if(self.distancia_frente > self.distancia_direita and self.distancia_frente > self.distancia_esquerda and self.distancia_frente > 1):
                    self.get_logger().info ('frente liberada')
                    self.mestados = 2
                elif(self.distancia_esquerda > self.distancia_direita and self.distancia_esquerda > self.distancia_frente ):
                    cmd.angular.z = 0.5
                    self.get_logger().info ('frente não liberada, turning left')
                    self.pub_cmd_vel.publish(cmd)
                elif(self.distancia_direita > self.distancia_frente and self.distancia_direita > self.distancia_esquerda ):
                    cmd.angular.z = -0.5
                    self.get_logger().info ('frente não liberada, turning right')
                    self.pub_cmd_vel.publish(cmd)
                else:
                    cmd.angular.z = 0.5
                    self.pub_cmd_vel.publish(cmd)
                    self.get_logger().info ('Moving around')

            elif self.mestados == 2: 
                    self.get_logger().info ('est = 2, moving')
                    cmd.linear.x = 0.5
                    self.pub_cmd_vel.publish(cmd)
                    self.get_logger().debug ("Distância até o obstáculo" + str(self.distancia_frente))
                
                    if(self.distancia <= 3 and self.distancia >=1 and abs(self.e_angulo) <= 0.06):
                        cmd.linear.x = 0.5
                        self.pub_cmd_vel.publish(cmd)
                        self.get_logger().info ('Incoming')
                    elif (self.distancia_frente < self.distancia_direita and self.distancia_frente < self.distancia_esquerda or self.distancia_frente < 1):
                        self.get_logger().info ('frente obstruída')
                        self.mestados = 0
                    if(self.distancia <= 0.8):
                        cmd.angular.z = 0.0
                        cmd.linear.x = 0.0
                        self.pub_cmd_vel.publish(cmd)
                        self.get_logger().info ('Você chegou ao seu destino!')

        self.get_logger().info ('Ordenando o robô: "parar"')
        self.pub_cmd_vel.publish(self.parar)
        rclpy.spin_once(self)

    # Destrutor do nó
    def __del__(self):
        self.get_logger().info('Finalizando o nó! Tchau, tchau...')
        # Função principal

def main(args=None):
    rclpy.init(args=args)
    node = R2D2()
    try:
        node.run()
        node.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
