# isi.take_home
# How to Run
python3 test_sensors.py {filename}

There are 3 different fault conditions detected

1) The variation between predicted encoder value and actual encoder value exceeds {stdev_encoder_diff} * 3 more than {max_number_variations} times

2) The variation exceedes {max_encoder_diff} once

3) The either the Encoder or Potentiometer have the same value for more than {max_number_same_values} times

{max_encoder_diff} and {stdev_encoder_diff} are calculated from normal.csv

The {time} is reported for the earliest fault condition detected. It is possible that one fault condition could be detected earlier than another, but have a time stamp at a later time. #TODO choose the earliest fault of all conditions.

The perfect.csv will generate a same value fault for obvious reasons.


