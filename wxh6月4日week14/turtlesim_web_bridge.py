#!/usr/bin/env python3
"""
ROS2 Turtlesim Web Bridge (方案B)
功能：ROS2节点 + 迷宫规则 + 碰撞检测 + WebSocket服务 + 自动探索
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import asyncio
import websockets
import json
import math
import random

class TurtlesimWebBridge(Node):
    def __init__(self):
        super().__init__('turtlesim_web_bridge')
        
        # --- 1. ROS2 基础配置 ---
        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        self.pose = None
        
        # --- 2. 迷宫与运动参数配置 ---
        self.map_min = 0.5      # 迷宫左/下边界
        self.map_max = 10.5     # 迷宫右/上边界
        self.safe_dist = 1.5    # 距离墙壁多远开始转向（防碰撞）
        self.lin_speed = 2.0    # 前进速度
        self.ang_speed = 2.0    # 转向角速度
        
        # --- 3. 状态机变量 ---
        self.state = 'MOVE'     # 状态机：MOVE(前进), TURNING(转向)
        self.turn_start_theta = 0.0
        self.target_theta = 0.0
        
        # 启动异步 WebSocket 服务
        self.get_logger().info('🚀 启动 Web Bridge...')
        asyncio.get_event_loop().run_until_complete(self.start_websocket_server())

    def pose_callback(self, msg):
        """接收小乌龟的实时位置"""
        self.pose = msg
        # 每次收到新位置，都执行一次控制逻辑
        self.control_loop()

    def control_loop(self):
        """核心控制逻辑：迷宫探索与防碰撞"""
        if self.pose is None:
            return
            
        cmd = Twist()
        
        if self.state == 'MOVE':
            # 计算距离四面墙的距离
            dist_left = self.pose.x - self.map_min
            dist_right = self.map_max - self.pose.x
            dist_bottom = self.pose.y - self.map_min
            dist_top = self.map_max - self.pose.y
            min_dist = min(dist_left, dist_right, dist_bottom, dist_top)
            
            # 碰撞检测：如果离墙太近，触发转向
            if min_dist < self.safe_dist:
                self.get_logger().warn(f'⚠️ 检测到墙壁 (距离: {min_dist:.2f})，准备转向...')
                self.state = 'TURNING'
                self.turn_start_theta = self.pose.theta
                # 随机向左或向右转 90度 (约1.57弧度)
                direction = 1 if random.random() > 0.5 else -1
                self.target_theta = self.turn_start_theta + (1.57 * direction)
                
                cmd.linear.x = 0.0
                cmd.angular.z = self.ang_speed * direction
            else:
                # 安全区域：继续直线前进
                cmd.linear.x = self.lin_speed
                
        elif self.state == 'TURNING':
            # 计算当前角度与目标角度的差值
            angle_diff = self.target_theta - self.pose.theta
            
            # 将角度差标准化到 [-pi, pi] 之间
            while angle_diff > math.pi:
                angle_diff -= 2.0 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2.0 * math.pi
                
            if abs(angle_diff) < 0.1: 
                # 转向完成，恢复前进状态
                self.get_logger().info('✅ 转向完成，继续探索')
                self.state = 'MOVE'
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
            else:
                # 还在转向中
                direction = 1 if angle_diff > 0 else -1
                cmd.linear.x = 0.0
                cmd.angular.z = self.ang_speed * direction
                
        # 发布速度指令给小乌龟
        self.cmd_pub.publish(cmd)

    async def start_websocket_server(self):
        """WebSocket 服务端：用于前端网页控制或状态显示"""
        async def handler(websocket, path):
            self.get_logger().info('🌐 网页客户端已连接')
            try:
                async for message in websocket:
                    data = json.loads(message)
                    # 这里可以扩展接收前端发来的遥控指令
                    self.get_logger().info(f'收到前端指令: {data}')
            except websockets.exceptions.ConnectionClosed:
                self.get_logger().info('❌ 网页客户端断开连接')

        async with websockets.serve(handler, "0.0.0.0", 8765):
            self.get_logger().info('🔗 WebSocket 服务已启动，监听端口: 8765')
            await asyncio.Future()  # 永久挂起，保持服务运行

def main(args=None):
    rclpy.init(args=args)
    node = TurtlesimWebBridge()
    
    # 在单独的线程中运行 ROS2 的 spin 循环
    import threading
    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()
    
    # 主线程运行 WebSocket 的 asyncio 事件循环
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()