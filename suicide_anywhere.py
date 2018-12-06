import math
import time
import krpc

conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel

srf_frame = vessel.orbit.body.reference_frame
obt_frame = vessel.orbit.body.non_rotating_reference_frame
orb_speed = conn.add_stream(getattr, vessel.flight(obt_frame), 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), 'speed')

print "Deorbiting Vessel..."
vessel.control.speed_mode = vessel.control.speed_mode.surface
ap = vessel.auto_pilot
ap.sas = True
ap.sas_mode = ap.sas_mode.retrograde
time.sleep(10)
while vessel.orbit.periapsis_altitude > 0:
    vessel.control.throttle = 1.0
vessel.control.throttle = 0.0

while altitude() > 50000:
    pass

# under 50km
while orb_speed() > 1500:
    vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
while altitude() > 10000:
    pass

# under 10km
while srf_speed() > 500:
    vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
while altitude() > 2000:
    pass

# under 2000m
while srf_speed() > 150:
    vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
while altitude() > 400:
    pass

# under 300m
while altitude() > 25:
    if srf_speed() > altitude()/5:
        vessel.control.throttle = 0.95
    elif srf_speed() > altitude()/10:
        vessel.control.throttle = 0.1
    elif srf_speed() > altitude()/15:
        vessel.control.throttle = 0

# under 50m
while altitude() > 2:
    if srf_speed() >7:
        vessel.control.throttle = 0.5
    else:
        vessel.control.throttle = 0

vessel.control.throttle = 0
