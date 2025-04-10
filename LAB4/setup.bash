WORKSPACE_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source ROS2 first (system Python)
source /opt/ros/humble/setup.bash
echo "ROS2 environment sourced"

export PYTHONPATH=/opt/ros/humble/lib/python3.10/site-packages:$PYTHONPATH


# Clean build artifacts
clean_build() {
    rm -rf build/ install/ log/
    echo "Build artifacts cleaned"
}

# Setup virtual environment for analysis
setup_venv() {
    if [ ! -d "${WORKSPACE_ROOT}/.venv" ]; then
        echo "Creating Python virtual environment..."
        python3 -m venv .venv
    fi
    source "${WORKSPACE_ROOT}/.venv/bin/activate"
    pip install numpy matplotlib scipy pyserial pyproj pandas utm transforms3d
    echo "Virtual environment activated"
}

case "$1" in
    "build")
        clean_build
        colcon build
        ;;
    "analysis")
        setup_venv
        source "${WORKSPACE_ROOT}/install/setup.bash"
        ;;
    *)
        source "${WORKSPACE_ROOT}/install/setup.bash"
        ;;
esac