# read.py
# very simple way: open-read-close
f = open('textfile.txt', 'r')
data = f.read()
f.close()

# read-with.py
# read file without close, with statement will close it for us :)
with open('submission.html', 'r') as f:
    text = f.read()

# write.py
data = 'Beautiful Python'

f = open('file.txt', 'w')
f.write(data)
f.close()

# write-with.py
# write to file using with, no need to close file explicitly
with open('submission.html', 'w') as f:
    data = 'Beautiful python'
    f.write(data)