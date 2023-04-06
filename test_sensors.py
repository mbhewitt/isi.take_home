import csv 
from statistics import mean

# encoder 2048 counts per rev
# pot 255 counts per rev
# 30:1 encode:pot
slope = 2048*30/255
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
            if(time<0.5): #calibration phase
                cal_encoder.append(encoder)
                cal_pot.append(pot)
            else:
                test_encoder[time]=encoder
                test_pot[time]=pot

        encoder_offset=round(mean(cal_encoder))
        pot_offset=round(mean(cal_pot))
        encoder_min=min(cal_encoder)
        encoder_max=max(cal_encoder)
        print(encoder_offset,pot_offset,encoder_min,encoder_max)
        for (time,pot) in test_pot.items():
            encoder=test_encoder[time]
            encoder_predict=(pot-pot_offset)*slope
            encoder_diff=abs(encoder_predict-encoder)
            print (time,pot,encoder,encoder_predict,encoder_diff)
read_file("error.csv")
