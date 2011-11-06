import bisect


class IndentationLevelsController:

  def __init__(self):
    super(IndentationLevelsController, self).__init__()
    self.__levels = []
    self.__indents = []

  def findLevel(self, indent):
    pos = bisect.bisect_left(self.__indents, indent)
    if pos == len(self.__levels):
      return self.AppendLevel(self)
    if self.__levels[pos].indent == indent:
      return self.UseLevel(self.__levels[pos])
    # self.__levels[pos].indent > indent,
    # self.__levels[pos-1].indent < indent
    if pos > 0:
      return self.UseLevel(self.__levels[pos-1])
    return self.PrependLevel(self)

  class AppendLevel:

    def __init__(self, controller):
      super(IndentationLevelsController.AppendLevel, self).__init__()
      self.shouldCreate = True
      self.parentElement = controller._lastChild
      self.__controller = controller

    def appendLevel(self, level):
      self.__controller._appendLevel(level)

  class PrependLevel:

    def __init__(self, controller):
      super(IndentationLevelsController.PrependLevel, self).__init__()
      self.shouldCreate = True
      self.parentElement = None
      self.__controller = controller

    def appendLevel(self, level):
      self.__controller.clear()
      self.__controller._appendLevel(level)

  class UseLevel:

    def __init__(self, level):
      super(IndentationLevelsController.UseLevel, self).__init__()
      self.shouldCreate = False
      self.existingLevel = level

  _lastChild = property(lambda self: None if not self.__levels else self.__levels[-1].lastChild)

  def _appendLevel(self, level):
    if self.__levels:
      assert(level.indent > self.__indents[-1])
    self.__levels.append(level)
    self.__indents.append(level.indent)
    return level

  def cutNested(self, level):
    pos = self.__levels.index(level) + 1
    del self.__levels[pos:]
    del self.__indents[pos:]

  def clear(self):
    self.__levels = []
    self.__indents = []