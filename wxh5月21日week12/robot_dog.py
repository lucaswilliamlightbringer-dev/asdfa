import pybullet as p
import pybullet_data
import time
import numpy as np


class QuadrupedController:
    def __init__(self, robot_id):
        self.robot_id = robot_id

        # === 关节定义 ===
        # Laikago 关节索引
        self.leg_joints = {
            'FR': [0, 1, 2],  # 右前
            'FL': [4, 5, 6],  # 左前
            'RR': [8, 9, 10],  # 右后
            'RL': [12, 13, 14]  # 左后
        }

        # 关节复位角度 (站立姿态)
        # 注意：PyBullet中Laikago的关节定义，1和2分别是thigh和calf
        self.default_angles = {
            'FR': [0, 0.67, -1.25],
            'FL': [0, 0.67, -1.25],
            'RR': [0, 0.67, -1.25],
            'RL': [0, 0.67, -1.25]
        }

        # === 运动参数 ===
        self.stand_height = 0.42  # 期望的机身离地高度 (米)
        self.forward_speed = 0.4  # 期望的前进速度 (米/秒)
        self.step_height = 0.08   # 抬腿高度 (米)
        self.gait_freq = 2.5      # 步态频率 (赫兹)

        # === 控制增益 (PD控制器参数) ===
        # 用于维持站立高度的虚拟弹簧刚度
        self.kp_height = 2000
        self.kd_height = 100

        # 用于髋关节位置控制的增益
        self.kp_hip = 100
        self.kd_hip = 5

    def get_body_height(self):
        """获取当前机身高度"""
        pos, _ = p.getBasePositionAndOrientation(self.robot_id)
        return pos[2]

    def get_body_velocity(self):
        """获取当前机身线速度"""
        lin_vel, _ = p.getBaseVelocity(self.robot_id)
        return lin_vel

    def trot_gait(self, t, leg_name):
        """
        生成对角小跑步态
        返回: [髋关节目标角度, 大腿目标角度, 小腿目标角度]
        """
        # 1. 相位控制：对角腿同步 (FL & RR 同相, FR & RL 反相)
        phase_offset = 0 if leg_name in ['FL', 'RR'] else np.pi
        phase = 2 * np.pi * self.gait_freq * t + phase_offset

        # 2. 步态逻辑
        # 判断当前腿是在“支撑相”(踩地) 还是 “摆动相”(抬腿)
        # sin(phase) > 0 时为摆动相 (抬腿)
        is_swing = np.sin(phase) > 0

        # --- 髋关节控制 (控制前后摆动以实现前进) ---
        # 髋关节摆动幅度决定了步长
        hip_amp = 0.15
        hip_angle = hip_amp * np.sin(phase)

        # --- 腿部高度控制 (PD控制) ---
        # 我们不仅仅设置固定角度，而是根据期望高度计算腿长
        current_height = self.get_body_height()
        height_error = self.stand_height - current_height

        # 基础腿长对应的角度 (简单逆运动学近似)
        # 当 sin(phase) = -1 (踩到底) 时，腿最长
        # 当 sin(phase) = 1 (抬最高) 时，腿最短

        thigh_base = self.default_angles[leg_name][1]
        calf_base = self.default_angles[leg_name][2]

        # 增加一个高度修正量
        # 如果身体太低，height_error > 0，我们需要缩短腿(让角度绝对值变大)来撑起身体
        # 这里使用简单的比例控制来调整大腿和小腿
        height_correction = height_error * 5  # 增益系数

        if is_swing:
            # 摆动相：抬腿
            # 抬腿时，膝盖弯曲更多
            lift = self.step_height * np.sin(phase)
            thigh_target = thigh_base - lift * 2  # 大腿向上收
            calf_target = calf_base + lift * 3    # 小腿向后收
        else:
            # 支撑相：踩地并推动身体
            # 支撑时，努力维持默认站立角度 + 高度修正
            thigh_target = thigh_base + height_correction
            calf_target = calf_base - (height_correction * 1.8) # 小腿配合大腿

        return [hip_angle, thigh_target, calf_target]

    def step(self, t):
        """主控制循环"""
        for leg_name, joint_ids in self.leg_joints.items():
            # 1. 获取目标角度
            targets = self.trot_gait(t, leg_name)

            # 2. 发送给仿真引擎
            # 髋关节 (Joint 0)
            p.setJointMotorControl2(
                bodyUniqueId=self.robot_id,
                jointIndex=joint_ids[0],
                controlMode=p.POSITION_CONTROL,
                targetPosition=targets[0],
                force=100,
                positionGain=0.1,  # 降低Gain让运动更柔和
                velocityGain=0.5
            )

            # 大腿 (Joint 1)
            p.setJointMotorControl2(
                bodyUniqueId=self.robot_id,
                jointIndex=joint_ids[1],
                controlMode=p.POSITION_CONTROL,
                targetPosition=targets[1],
                force=150,
                positionGain=0.05,
                velocityGain=0.4
            )

            # 小腿 (Joint 2)
            p.setJointMotorControl2(
                bodyUniqueId=self.robot_id,
                jointIndex=joint_ids[2],
                controlMode=p.POSITION_CONTROL,
                targetPosition=targets[2],
                force=150,
                positionGain=0.05,
                velocityGain=0.4
            )


def setup_simulation():
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    # 增加求解器迭代次数，让接触更稳定（这对上台阶很重要）
    p.setPhysicsEngineParameter(
        fixedTimeStep=1.0 / 240.0,
        numSolverIterations=200,
        numSubSteps=2
    )

    # 加载地面
    plane_id = p.loadURDF("plane.urdf")

    # === 添加台阶 ===
    # 创建彩色台阶用于测试
    colors = [[1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]]
    for i in range(4):
        # 每个台阶长0.3米，高0.05米
        box_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.3, 0.3, 0.025])
        visual_id = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.3, 0.3, 0.025], rgbaColor=colors[i])

        # 计算位置：x轴方向排列，z轴方向升高
        pos_x = 1.0 + (i * 0.3)
        pos_z = 0.025 + (i * 0.05)

        p.createMultiBody(
            baseMass=0,  # 质量为0表示静态物体
            baseCollisionShapeIndex=box_id,
            baseVisualShapeIndex=visual_id,
            basePosition=[pos_x, 0, pos_z]
        )

    # 设置摄像机视角
    p.resetDebugVisualizerCamera(
        cameraDistance=2.5,
        cameraYaw=45,
        cameraPitch=-20,
        cameraTargetPosition=[1.5, 0, 0.5]
    )


def load_robot():
    # 使用Laikago URDF
    # 注意：确保你的 pybullet_data 中包含 laikago 文件夹
    start_pos = [0, 0, 0.45]
    start_orientation = p.getQuaternionFromEuler([0, 0, 0])

    robot_id = p.loadURDF(
        "laikago/laikago_toes.urdf",
        start_pos,
        start_orientation,
        useFixedBase=False,
        flags=p.URDF_USE_SELF_COLLISION
    )

    return robot_id


def main():
    setup_simulation()
    robot_id = load_robot()
    controller = QuadrupedController(robot_id)

    print("仿真开始... 机器人将尝试走向台阶")

    t = 0
    dt = 1 / 240.0

    try:
        while p.isConnected():
            # 1. 计算控制
            controller.step(t)

            # 2. 物理步进
            p.stepSimulation()

            # 3. 时间更新
            t += dt
            time.sleep(dt)

    except KeyboardInterrupt:
        print("仿真结束")
        p.disconnect()


if __name__ == "__main__":
    main()