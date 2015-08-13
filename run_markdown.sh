read -r -d '' HTML_HEAD1 << EOM
<!DOCTYPE html>
<head>
    <meta charset="utf-8"/>
    <style>
EOM

read -r -d '' HTML_HEAD2 << EOM
    </style>
</head>
<body>
EOM

read -r -d '' HTML_TAIL << EOM
</body>
</html>
EOM

rm ./article.html

echo $HTML_HEAD1 > ./article.html

cat ./colors.css >> ./article.html

echo $HTML_HEAD2 >> ./article.html

python -m markdown2 --extras fenced-code-blocks ./article.txt >> ./article.html

echo $HTML_TAIL >> ./article.html



grip ./article.txt --export ./article_grip.html
