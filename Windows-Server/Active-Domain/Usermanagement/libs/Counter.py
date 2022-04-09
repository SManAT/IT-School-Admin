class Counter():
  """ Counter Class for statistics """
  createdUsers = 0
  userExists = 0
  userInvalid = 0
  wrongGroup = 0

  def incUser(self):
    self.createdUsers += 1

  def incUserExists(self):
    self.userExists += 1

  def incUserInvalid(self):
    self.userInvalid += 1

  def incWrongGroups(self):
    self.wrongGroup += 1

  def getCreatedUser(self):
    return self.createdUsers

  def getUserExists(self):
    return self.userExists

  def getUserInvalid(self):
    return self.userInvalid

  def getWrongGroups(self):
    return self.wrongGroup
