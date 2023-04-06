import csv 
from statistics import mean,stdev
import sys

"""
There are 3 different fault conditions detected
1) The variation between predicted encoder value and actual encoder value exceeds {stdev_encoder_diff} * 3 more than {max_number_variations} times
2) The variation exceeds {max_encoder_diff} once
3) The either the Encoder or Potentiometer have the same value for more than {max_number_same_values} times

{max_encoder_diff} and {stdev_encoder_diff} are calculated from normal.csv

The {time} is reported for the earliest fault condition detected. It is possible that one fault condition could be detected earlier than another, 
but have a time stamp at a later time. #TODO choose the earliest fault of all conditions.

The perfect.csv will generate a same value fault for obvious reasons.

"""

#Constants
# encoder 2048 counts per rev
# pot 255 counts per rev
# 30:1 encode:pot

slope = 2048*30/255
max_encoder_diff=832 #calculated from normal.csv
stdev_encoder_diff=128
 
max_number_variations=4
max_number_same_values=20 

def read_file(filename):
    with open(filename) as csv_file:
        sensor_reader=csv.DictReader(csv_file)
        cal_encoder=[]
        cal_pot=[]
        test_encoder={}
        test_pot={}
        for row in sensor_reader:
#           print(row)
            time=float(row['time'])
            encoder=int(row['encoder_readout'])
            pot=int(row['potentiometer_readout'])
#            print(time,encoder,pot)
            if(time<=0.5): #calibration phase
                cal_encoder.append(encoder)
                cal_pot.append(pot)
            else: #test phase
                test_encoder[time]=encoder
                test_pot[time]=pot
        pot_offset=round(mean(cal_pot))

        return(pot_offset,test_encoder,test_pot)

def get_noisefigure(pot_offset,test_encoder,test_pot):
   encoder_diff=[]
   for (time,pot) in test_pot.items():
       encoder=test_encoder[time]
       encoder_predict=(pot-pot_offset)*slope
       encoder_diff.append(abs(encoder_predict-encoder))
   return(max(encoder_diff),stdev(encoder_diff))

def test_file(pot_offset,test_pot,test_encoder,max_encoder_diff,stdev_encoder_diff):
   prev_encoder=None
   prev_pot=None
   encoder_count=0
   pot_count=0
   encoder_time=0
   pot_time=0
   variation_count=0
   variation_time=0
   for (time,pot) in test_pot.items():
       encoder=test_encoder[time]
       encoder_predict=(pot-pot_offset)*slope
       encoder_diff=abs(encoder_predict-encoder)

       #TODO: Move test framework into own class
       if(encoder_diff>max_encoder_diff):
           print(f"Variation exceeded between predicted encoder value({encoder_predict}) and actual encoder value({encoder}) for Potentiometer value ({pot}) at time ({time})")
           return

       if(encoder_diff>stdev_encoder_diff*3): #3rd stdev away
           variation_count+=1
       else:
           variation_count=0
           variation_time=time
       if(variation_count>max_number_variations):
           print(f"Max number of variations ({max_number_variations}) with ({variation_count}) exceeded at time ({variation_time})")
           return

       if(encoder==prev_encoder):
           encoder_count+=1
       else:
           encoder_count=0
           encoder_time=time
           prev_encoder=encoder
       if(encoder_count>max_number_same_values):
           print(f"Max number of same values({max_number_same_values}) for Encoder failed at time ({encoder_time}) with value ({encoder})")
           return

       if(pot==prev_pot):
           pot_count+=1
       else:
           pot_count=0
           pot_time=time
           prev_pot=pot
       if(pot_count>max_number_same_values):
           print(f"Max number of same values({max_number_same_values}) for Potentiometer failed at time ({pot_time}) with value ({pot})")
           return
   print("No Errors detected")
   return

# get values from calibration file
#(pot_offset_norm,test_encoder_norm,test_pot_norm)=read_file("normal.csv")
#(max_encoder_diff,stdev_encoder_diff)=get_noisefigure(pot_offset_norm,test_encoder_norm,test_pot_norm)
#print(max_encoder_diff,stdev_encoder_diff)

filename = sys.argv[1]
(pot_offset,test_encoder,test_pot)=read_file(filename)
test_file(pot_offset,test_pot,test_encoder,max_encoder_diff,stdev_encoder_diff)

# TODO: Add logging, organize classes 
# TODO: Add ability to turn off different types of fault conditions.
