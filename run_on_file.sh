rm -rf ./server/world
cd server
java -jar craftbukkit-1.12.1.jar &
cpid=$!
cd ..
sleep 10
python $1 
kill $cpid