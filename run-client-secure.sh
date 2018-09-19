# Hello, please make sure you have completed the following steps BEFORE running this script
#
# 1. Make sure that FoxDot is in your python path (not pythonX).
# ( verify this by running the following command python -c "import FoxDot; print(FoxDot.__file__) )
#
# 2. Install Docker, and make sure the Docker client is running.
# 3. Start SuperCollider with FoxDot ( using FoxDot.start command)


# get foxdot path
python_path=$(python -c "import FoxDot; print(FoxDot.__file__)")
foxdot_path=${python_path%/*}
pkg_path=${foxdot_path%/*}

if ! [ -d $foxdot_path ] ; then
    echo "foxdot path: $foxdot_path is a not directory. please verify your foxdot installation ";
    exit;
fi

# get ip on local network
ip_address=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')

if ! [[ $ip_address =~ ^[0-9\.] ]] ; then
    echo "ip address: ip_address is invalid ... please investigate the command ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'";
    exit;
fi

# build docker image
printf "\nBuilding Docker Image with the following params:
---> IP address: $ip_address
---> foxdot_path: $foxdot_path
---> pkg_path: $pkg_path
\n"

docker build --build-arg ip_address=$ip_address --build-arg foxdot_path=$foxdot_path --build-arg pkg_path=$pkg_path --no-cache -t publictrooper .

# run docker container
docker run -it -p 54321:54321 publictrooper
