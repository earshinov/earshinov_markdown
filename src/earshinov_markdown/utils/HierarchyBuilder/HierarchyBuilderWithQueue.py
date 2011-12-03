from .HierarchyBuilder import HierarchyBuilder


class HierarchyBuilderWithQueue(HierarchyBuilder):

  def __init__(self):
    super(HierarchyBuilderWithQueue, self).__init__()
    self._levels = []

  def push(self, obj):
    self._levels.append(obj)

  def put(self, obj):
    self._levels[-1] = obj

  def pop(self):
    self._levels.pop()

  def popN(self, n):
    del self._levels[-n:]

  def popAll(self):
    del self._levels[:]