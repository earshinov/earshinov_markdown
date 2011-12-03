class HierarchyBuilder:

  def push(self, obj):
    raise NotImplemented()

  def put(self, obj):
    raise NotImplemented()

  def pop(self):
    raise NotImplemented()

  def popN(self, n):
    for _ in range(n):
      self.pop()

  def popAll(self):
    raise NotImplemented()