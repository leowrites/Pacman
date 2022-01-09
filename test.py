import math

def check_radar(self, degree, map):
    len = 0
    x = int(
          self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
    y = int(
           self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

    while not map.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
            len = len + 1
            x = int(
                self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = int(
                self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

    dist = int(
        math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
    self.radars.append([(x, y), dist])
