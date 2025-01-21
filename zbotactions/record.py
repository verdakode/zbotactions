#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from skillit.record.recorder import SkillRecorder
from skillit.play.player import FramePlayer


def get_zbot_ip():
    config_path = Path.home() / ".zbot_config.json"
    if not config_path.exists():
        print("No ZBot configuration found. Running setup...")
        from setup_zbot import setup_zbot

        setup_zbot()

    with open(config_path) as f:
        config = json.load(f)
        return config.get("ip")


# Default joint mapping for ZBot
JOINT_MAPPING = {
    "left_shoulder_yaw": 11,
    "left_shoulder_pitch": 12,
    "left_elbow_yaw": 13,
    "left_gripper": 14,
    "right_shoulder_yaw": 21,
    "right_shoulder_pitch": 22,
    "right_elbow_yaw": 23,
    "right_gripper": 24,
    "left_hip_yaw": 31,
    "left_hip_roll": 32,
    "left_hip_pitch": 33,
    "left_knee_pitch": 34,
    "left_ankle_pitch": 35,
    "right_hip_yaw": 41,
    "right_hip_roll": 42,
    "right_hip_pitch": 43,
    "right_knee_pitch": 44,
    "right_ankle_pitch": 45,
}


def record_skill(ip, skill_name):
    recorder = SkillRecorder(
        ip=ip, joint_name_to_id=JOINT_MAPPING, skill_name=skill_name
    )
    recorder.record()


def play_skill(ip, skill_name):
    player = FramePlayer(ip=ip, joint_name_to_id=JOINT_MAPPING)
    player.play(skill_name)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ["record", "play"]:
        print("Usage: playrecord [record|play] [skill_name]")
        sys.exit(1)

    command = sys.argv[1]

    # Get skill name from args or prompt
    if len(sys.argv) > 2:
        skill_name = sys.argv[2]
    else:
        skill_name = input("Enter skill name: ")

    ip = get_zbot_ip()
    if not ip:
        print("Error: Could not get ZBot IP address")
        sys.exit(1)

    print(f"Connecting to ZBot at {ip}...")
    if command == "record":
        record_skill(ip, skill_name)
    else:
        play_skill(ip, skill_name)


if __name__ == "__main__":
    main()
