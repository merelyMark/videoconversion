import os, subprocess, re, time
from stat import *
from ast import literal_eval as make_tuple
vid_command = ' -c:v libx264 -preset veryslow -tune film -crf 22 -vf scale=-2:720 '
aud_command = ' -c:a copy '
meta_command = ' -map_metadata 0 '
FIX_DATETIME = False
CONVERT_720 = True
pt = re.compile("(\d+)x(\d+)")
for filename in os.listdir('./4k/'):
    outfile = './720/' + filename
    if (not os.path.isfile(outfile)):
        outfile = './720/' + re.escape(filename)
        info_command = 'ffmpeg -i ./4k/' + re.escape(filename)
        #print info_command
        output_command = info_command + vid_command + aud_command
        output_command = output_command + ' ' + outfile
        p = subprocess.Popen(info_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        s, err = p.communicate()
        #tups = make_tuple(out)
        #print err
        tups = [item for item in err.split(' ') if item.strip()]
        if CONVERT_720:
            for tup in tups:
                if(pt.match(tup)):
                    tup = [item for item in tup.split('x') if item.strip()]
                    
                    if (len(tup) > 0 and int(float(tup[0])) > 0):
                        print output_command
                        go ahead and convert it to 720
                        np = subprocess.Popen(output_command, shell=True)
                        np.communicate()                    
                #print tup
    else:
        print 'ALREADY EXISTS: ' + outfile
        #fix the date/time stamp
        if FIX_DATETIME:
            in_st = os.stat('./4k/'+filename)
            in_atime = in_st[ST_ATIME]
            in_mtime = in_st[ST_MTIME]

            #print time.ctime(in_atime) + ' ' + time.ctime(in_mtime)
            
            out_st = os.stat(outfile)
            out_atime = out_st[ST_MTIME]
            #print time.ctime(out_atime) + ' ' + time.ctime(in_mtime)
            os.utime(outfile, (out_atime, in_mtime))