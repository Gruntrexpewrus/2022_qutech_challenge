echo "Starting Servers"
python server.py &
python qinterface_server.py &
kill $(lsof -t -i:1234)
