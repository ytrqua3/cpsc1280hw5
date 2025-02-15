pat="^([^,]*,){6}DALLAS [^,]*(.*)Wildlife snag$"
echo $pat
grep -E "$pat" $1
