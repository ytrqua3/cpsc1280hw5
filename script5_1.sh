set -f
file=$1
regex=$2
line=$(grep -n "% change from previous year,,,,,,,,,,,,,,,,,,,,,,,,," $file | cut -d":" -f1)
head -n $line $file | grep "$regex"

