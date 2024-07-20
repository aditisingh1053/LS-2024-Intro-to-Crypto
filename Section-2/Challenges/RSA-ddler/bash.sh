cd Riddle
for ((i=100; i>=1; i--)); do
    echo "$i.zip"
    unzip "$i.zip"
done