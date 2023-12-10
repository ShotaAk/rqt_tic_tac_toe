
# RQt Tic-Tac-Toe

[![build_and_test](https://github.com/ShotaAk/rqt_tic_tac_toe/actions/workflows/build_and_test.yaml/badge.svg)](https://github.com/ShotaAk/rqt_tic_tac_toe/actions/workflows/build_and_test.yaml)

Let's play Tic-Tac-Toe on rqt!

https://github.com/ShotaAk/rqt_tic_tac_toe/assets/18494952/0dfd166d-ec24-4818-8bf4-a51381a28bd5

## Requirements

- ROS 2 Humble

## Installation

```sh
cd ~/ros2_ws/src
git clone https://github.com/ShotaAk/rqt_tic_tac_toe.git

cd ~/ros2_ws
colcon build --symlink-install
```

## Usage

First, register `rqt_tic_tac_toe` in `rqt` by executing the following command:

```sh
source ~/ros2_ws/install/setup.bash
rqt --force-discover
```

Next, start Tic-Tac-Toe.

![rqt_tic_tac_toe_on_rqt](https://github.com/ShotaAk/rqt_tic_tac_toe/assets/18494952/9493be17-cec3-46ae-b3c3-123eec18a040)

### PvP

1. Start `rqt_tic_tac_toe` with each other.
1. Enter the player name in **frame ID**.
1. Click on the board and the frame ID will be sent to the other player.
1. Select your opponent's ID from sync ID and you are ready to play.
1. Reset and start the game. Enjoy!

https://github.com/ShotaAk/rqt_tic_tac_toe/assets/18494952/ee695811-5cfb-4b04-a88a-60755b208c32

## Game Rule

https://en.wikipedia.org/wiki/Tic-tac-toe

## LICENSE

Apache 2.0
