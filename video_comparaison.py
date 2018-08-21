import subprocess
import sys
import os

FFMPEG_BIN = "ffmpeg"
directory = '/Users/richardlim/Downloads/ea/creatives/'
#video = "ea1.mp4"
video = "5acd41a9f50414e872175b7efa76db21eb585101.mp4"




def parsing_ffmpeg_SSIM(line):
  if line.find("SSIM") < 0:
    return 0

  substring = line[line.find("SSIM")+5:]
  substring = substring.replace(' (inf)','')
  substring = substring.replace('inf', '1.0')
  array = substring.split(' ')
  currentsum=0
  index=0
  for number in array:
    if  number.find(':') > 0:
      currentsum += float(number[number.find(':')+1:])
      index += 1
  return currentsum/index


def parsing_ffmpeg_PSNR(line):
  if line.find("PSNR") < 0:
    return [0,0]

  substring = line[line.find("average")+8:].split(' ')[0]
  if substring == "inf":
    return 100

  return float(substring)


def compare_videos(video1, video2):
  commands = [FFMPEG_BIN,
              '-i',
              directory + video1,
              '-i',
              directory + video2,
              '-lavfi',
              "ssim;[0:v][1:v]psnr",
              '-f',
              'null',
              '-' ]
  print commands

  #ffmpeg output is located in stderr
  result = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = result.communicate()

  ssim = 0
  psnr = 0
  #ffmpeg output is located in stderr
  if(err) : 
    for line in err.splitlines():
      if line.startswith('[Parsed_ssim'):
        ssim = parsing_ffmpeg_SSIM(line)
      if line.startswith('[Parsed_psnr'):
        psnr = parsing_ffmpeg_PSNR(line)
  return [ssim, psnr]



for file in os.listdir(directory):
  if '.mp4' in file and file != video:
    res = compare_videos(video, file)

  print '-- Comparing {} and {}'.format(video, file)
  print 'SSIM: {} - PSNR: {}'.format(res[0], res[1])
  if res[0] == 1 or res[1] ==100:
    break



# Typical values for the PSNR in lossy image and video compression are between 30 and 50 dB, provided the bit depth is 8 bits, where higher is better. 
# For 16-bit data typical values for the PSNR are between 60 and 80 dB. 
# Acceptable values for wireless transmission quality loss are considered to be about 20 dB to 25 dB.