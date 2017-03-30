#!/usr/bin/python

import math
import time
from dotstar import Adafruit_DotStar

num_pixels = 240 # Number of LEDs in strip.

strip = Adafruit_DotStar(num_pixels)        # Use SPI (pins 10=MOSI, 11=SCLK).

strip.begin()             # Initialize pins for output.
strip.setBrightness(255)  # Full brightness.

def simple_chaser(strip, step, period=60):
  for pixel in range(strip.numPixels()):
    r = 1.0 + 0.5*math.cos(
      (pixel - step)/float(period)*2*math.pi - 2*math.pi/3)
    g = 1.0 + 0.5*math.cos(
      (pixel - step)/float(period)*2*math.pi + 2*math.pi/3)
    b = 1.0 + 0.5*math.cos(
      (pixel - step)/float(period)*2*math.pi)
    color = ((min(255, int(256*max(r, 0))) << 16) +
             (min(255, int(256*max(g, 0))) << 8) +
             (min(255, int(256*max(b, 0)))))
    strip.setPixelColor(pixel, color)

class TravelingWave(object):
  def __init__(self, wavenumber, omega, phi_0, gain, offset):
    self.wavenumber = wavenumber
    self.omega = omega
    self.phi_0 = phi_0
    self.gain = gain
    self.offset = offset

  def value(self, x, t):
    return self.offset + self.gain * math.cos(self.phi_0 + self.wavenumber * x - self.omega * t)

def traveling_wave_chaser(strip, step, r_wave, g_wave, b_wave):
  for pixel in range(strip.numPixels()):
    r = r_wave.value(pixel, step)
    g = g_wave.value(pixel, step)
    b = b_wave.value(pixel, step)
    color = ((min(255, int(256*max(r, 0))) << 16) +
             (min(255, int(256*max(g, 0))) << 8) +
             (min(255, int(256*max(b, 0)))))
    strip.setPixelColor(pixel, color)
      
    
period = 60

r_wave = TravelingWave(2*math.pi/period, 1*math.pi/period, 0.0, 0.5, 0.5)
g_wave = TravelingWave(2*math.pi/period, 2*math.pi/period, 2*math.pi/3, 0.5, 0.5)
b_wave = TravelingWave(math.pi/period, -2*math.pi/period, -2*math.pi/3, 0.5, 0.5)

while True:
  for step in range(4*period):
    #simple_chaser(strip, step, period)
    traveling_wave_chaser(strip, step, r_wave, g_wave, b_wave)
    strip.show()
    time.sleep(0.020)
