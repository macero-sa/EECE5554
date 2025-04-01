WORKSPACE_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d "${WORKSPACE_ROOT}/.venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

source "${WORKSPACE_ROOT}/.venv/bin/activate"

source /opt/ros/humble/setup.bash
echo "ROS2 environment sourced"

# add to this whenever a new package is used in any of the scripts
pip install numpy matplotlib scipy pyserial pyproj pandas utm empy transforms3d


if [ -f "${WORKSPACE_ROOT}/install/setup.bash" ]; then
    source "${WORKSPACE_ROOT}/install/setup.bash"
    echo "Python venv activated"
else
    echo "Workspace not built yet. Run 'colcon build' first."
fi
