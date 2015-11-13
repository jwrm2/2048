from math import log

#----------------------------------------------------------------------------------------------------------------------------------

def isPower(num, base):
  """Returns whether or not a number is a natural power of the base."""
  if base == 1 and num != 1: return False
  if base == 1 and num == 1: return True
  if base == 0 and num != 1: return False
  if num  == 0             : return False
  power = int(log(num, base) + 0.5)
  return base ** power == num

#----------------------------------------------------------------------------------------------------------------------------------

class GameOverException(Exception):
  """Exception for when moves are attempted on a finished game."""

#----------------------------------------------------------------------------------------------------------------------------------

class HexColor(object):
  """A colour created from a 6 digit hex number."""

  def __init__(self, hr):
    """Parses the input to create rgb components."""
    self.hexRep = hr
    if(self.hexRep[0:2] == "0x"):
      self.hexRep = self.hexRep[2:]
    digits = []
    for c in list(self.hexRep):
      digits.append(int(c, 16))
    self.red   = 16*digits[0] + digits[1]
    self.green = 16*digits[2] + digits[3]
    self.blue  = 16*digits[4] + digits[5]

  def getHex(self):
    """Returns the hex representation as a string."""
    return "0x" + self.hexRep

  def getRed(self):
    """Returns the red component as an int between 0 and 255."""
    return self.red
  def getGreen(self):
    """Returns the green component as an int between 0 and 255."""
    return self.green
  def getBlue(self):
    """Returns the blue component as an int between 0 and 255."""
    return self.blue

  def getRedF(self):
    """Returns the red component as a float between 0 and 1."""
    return self.red/255.0
  def getGreenF(self):
    """Returns the green component as a float between 0 and 1."""
    return self.green/255.0
  def getBlueF(self):
    """Returns the blue component as a float between 0 and 1."""
    return self.blue/255.0
