grep -E "^([^,]*,){15}(1[5-9]|2[0-9]|30)(,[^,]*){6}$" $1 | sort -n -t"," -k4
