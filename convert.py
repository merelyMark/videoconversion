import os, subprocess, re, time
from stat import *
from ast import literal_eval as make_tuple

resolutions = ['480','720']
vid_command = ' -c:v libx264 -preset veryslow -tune film -crf 22 -vf scale=-2:'
resolution = '480' 
aud_command = ' -c:a copy '
meta_command = ' -map_metadata 0 '
FIX_DATETIME = True
CONVERT_720 = True
IN_DIR = './'
OUT_DIR= './' 
TEST_CONVERT = False
TEST_DATETIME = False

pt = re.compile("(\d+)x(\d+)")

def fix_datetime(filename, outfile):
    in_st = os.stat(IN_DIR+filename)
    in_atime = in_st[ST_ATIME]
    in_mtime = in_st[ST_MTIME]

    #print time.ctime(in_atime) + ' ' + time.ctime(in_mtime)

    out_st = os.stat(outfile)
    out_atime = out_st[ST_MTIME]
    if (TEST_DATETIME):
        print (time.ctime(out_atime) + ' ' + time.ctime(in_mtime))
    else:
        os.utime(outfile, (out_atime, in_mtime))


def convert_720(filename, outfile):
    if (not os.path.isfile(outfile)):
        clean_outfile = OUT_DIR + re.escape(filename)
        info_command = 'ffmpeg -i ' + IN_DIR + re.escape(filename)
        #print info_command
        output_command = info_command + vid_command + resolution + ' ' + aud_command
        output_command = output_command + ' ' + clean_outfile
        p = subprocess.Popen(info_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        s, err = p.communicate()

        tups = [item for item in err.decode('utf8').split(' ') if item.strip()]
        if CONVERT_720:
            for tup in tups:
                if(pt.match(tup)):
                    tup = [item for item in tup.split('x') if item.strip()]
                    
                    if (len(tup) > 0 and int(float(tup[0])) > 0):
                        if (TEST_CONVERT):
                            print (output_command)
                        #go ahead and convert it to 720
                        else:
                            np = subprocess.Popen(output_command, shell=True)
                            np.communicate()

                            if FIX_DATETIME:
                                fix_datetime(filename, outfile)
                            break
                #print tup
    else:
        print ('ALREADY EXISTS: ' + outfile)
        #fix the date/time stamp
        if FIX_DATETIME:
            fix_datetime(filename, outfile)

tot_cnt = 0
for resolution in resolutions:
    cnt = 0
    OUT_DIR = './' + resolution + '/'
    for filename in os.listdir(IN_DIR):
        if filename.endswith(".mp4"):
            cnt += 1
            tot_cnt += 1
            outfile = OUT_DIR + filename
            convert_720(filename, outfile)    

    print ("Finished # " + str(cnt) )

print ("Total converted: " + str(tot_cnt))
