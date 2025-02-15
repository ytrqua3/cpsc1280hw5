cut -d"," -f"12" $1 | sort -t"," -k12 | uniq -c |sort -r| head -n2 | tr -s ' ' | cut -d" " -f3- | xargs -I {}  grep -E "^([^,]*,){11}{}(,[^,]*){10}$" $1 | sort -n -t"," -k4
