rating=$(mktemp)

name_pat="^\"$2\","
grep -E "$name_pat" $1 | sort -n -r -t',' -k4 | head -n1 | cut -d',' -f4 >$rating
cat $rating
cat $rating | xargs -I{} grep -E "^\"$2\",([^,]*,){2}{}" $1 | cut -d',' -f3 | tr -d '"' | sort -nr | uniq


rm $rating
