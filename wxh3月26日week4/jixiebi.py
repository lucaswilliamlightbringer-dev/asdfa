import pybullet as p
import pybullet_data as pd
import time
import math

# --- 1. 初始化环境 ---
p.connect(p.GUI)
p.setAdditionalSearchPath(pd.getDataPath())
p.setGravity(0, 0, -9.8)
p.resetDebugVisualizerCamera(1.2, 45, -30, [0.5, 0, 0.65])

# --- 2. 加载地面、桌子和机械臂 ---
p.loadURDF("plane.urdf")
table_pos = [0.5, 0, 0]
p.loadURDF("table/table.urdf", table_pos, useFixedBase=True)

panda_pos = [0.5, 0, 0.625]
pandaId = p.loadURDF("franka_panda/panda.urdf", panda_pos, useFixedBase=True)

# --- 3. 放置方块在桌子前沿 ---
cube_pos_fixed = [0.7, 0.0, 0.655]  # 桌面外侧前沿
cube_ori = p.getQuaternionFromEuler([0, 0, 0])
cube_id = p.loadURDF("cube_small.urdf", cube_pos_fixed, cube_ori)
p.changeDynamics(cube_id, -1, lateralFriction=1.0, spinningFriction=1.0, rollingFriction=0.001, mass=0.1)

# --- 4. Panda 控制函数 ---
def move_ee(target_pos, target_ori=[math.pi,0,0], steps=120):
    current_poses = [p.getJointState(pandaId, i)[0] for i in range(7)]
    target_poses = p.calculateInverseKinematics(pandaId, 11, target_pos, p.getQuaternionFromEuler(target_ori))
    for t in range(steps):
        alpha = (t+1)/steps
        interp_poses = [current_poses[i]*(1-alpha) + target_poses[i]*alpha for i in range(7)]
        for i in range(7):
            p.setJointMotorControl2(pandaId, i, p.POSITION_CONTROL, interp_poses[i], force=500)
        p.stepSimulation()
        time.sleep(1./240.)

def control_gripper(open=True, steps=50):
    pos = 0.04 if open else 0.0
    for _ in range(steps):
        p.setJointMotorControl2(pandaId, 9, p.POSITION_CONTROL, pos, force=50)
        p.setJointMotorControl2(pandaId, 10, p.POSITION_CONTROL, pos, force=50)
        p.stepSimulation()
        time.sleep(1./240.)

# --- 5. 智能抓取逻辑 ---
hover_pos = [0.55, 0, 0.8]  # 悬停观察位置
control_gripper(open=True)
move_ee(hover_pos, steps=120)

try:
    while True:
        # 获取方块位置
        cube_pos, _ = p.getBasePositionAndOrientation(cube_id)

        # 末端位置
        ee_pos = p.getLinkState(pandaId, 11)[0]
        dist = math.sqrt((cube_pos[0]-ee_pos[0])**2 + (cube_pos[1]-ee_pos[1])**2 + (cube_pos[2]-ee_pos[2])**2)
        
        if dist > 0.3:
            # 悬停等待观察
            move_ee(hover_pos, steps=20)
            continue

        # --- 靠近方块 ---
        approach_pos = [cube_pos[0], cube_pos[1], cube_pos[2]+0.05]
        move_ee(approach_pos, steps=100)

        grasp_pos = [cube_pos[0], cube_pos[1], cube_pos[2]+0.01]
        move_ee(grasp_pos, steps=100)

        # 夹爪闭合抓取
        control_gripper(open=False)

        # --- 抓取后抬起并伸直手臂 ---
        lift_pos = [cube_pos[0], cube_pos[1], 1.0]
        move_ee(lift_pos, steps=150)

        stretch_pos = [0.6, 0.0, 1.0]  # 桌子前方伸直
        move_ee(stretch_pos, steps=150)

        # --- 放置方块到桌面中间位置 ---
        place_pos = [0.55, 0.0, 0.655]
        move_ee(place_pos, steps=120)

        # 松开夹爪
        control_gripper(open=True)

        # 回到悬停观察位置
        move_ee(hover_pos, steps=120)

except KeyboardInterrupt:
    print("手动关闭模拟")
finally:
    p.disconnect()