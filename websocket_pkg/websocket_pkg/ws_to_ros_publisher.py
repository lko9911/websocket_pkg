# ~/colcon_ws/src/websocket_ros/websocket_ros/ws_to_ros_publisher.py

import asyncio
import websockets
import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class WebSocketROSPublisher(Node):
    def __init__(self):
        super().__init__('websocket_ros_publisher')
        self.publisher_ = self.create_publisher(String, 'websocket_topic', 10)
        self.get_logger().info("ROS 2 WebSocket Publisher Node Started")

    async def echo(self, websocket, path):
        async for message in websocket:
            self.get_logger().info(f"Received from client: {message}")
            msg = String()
            msg.data = message
            self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = WebSocketROSPublisher()

    # asyncio 웹소켓 서버 실행
    start_server = websockets.serve(node.echo, "0.0.0.0", 8765)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
