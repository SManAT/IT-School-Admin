class Error():
  
  def __init__(self):
    self.error = False

  def reset(self):
    self.error = False

  def hasErrors(self):
    return self.error

  def setErrorMessage(self, msg):
    self.error = True
    self.msg = msg

  def getErrorMessage(self):
    return self.msg