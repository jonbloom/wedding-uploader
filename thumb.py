from PIL import Image
import os

for subdir, dirs, files in os.walk('./tmp/uploads'):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith("g"):

        	im = Image.open(filepath)
        	im.thumbnail((500,500), Image.ANTIALIAS)
        	im.save(os.path.join(subdir, 'thumb', file))

            
# for infile in glob.glob("./tmp/uploads/*.jpeg"):
#   im = Image.open(infile)
#   # convert to thumbnail image
#   im.thumbnail((500, 500), Image.ANTIALIAS)
#   # don't save if thumbnail already exists
#   if infile[0:2] != "T_":
#     # prefix thumbnail file with T_
#     im.save(infile)