from .HierarchyBuilderWithQueue import HierarchyBuilderWithQueue


class TracingHierarchyBuilderWithQueue(HierarchyBuilderWithQueue):

  def __init__(self, trace=None):
    super(TracingHierarchyBuilderWithQueue, self).__init__()
    self.trace = [] if trace is None else trace
    self._addTrace()

  def _addTrace(self):
    self.trace.append(self._levels[:])

  def push(self, obj):
    super(TracingHierarchyBuilderWithQueue, self).push(obj)
    self._addTrace()

  def put(self, obj):
    super(TracingHierarchyBuilderWithQueue, self).put(obj)
    self._addTrace()

  def pop(self):
    super(TracingHierarchyBuilderWithQueue, self).pop()
    self._addTrace()

  def popN(self, n):
    super(TracingHierarchyBuilderWithQueue, self).popN(n)
    self._addTrace()

  def popAll(self):
    super(TracingHierarchyBuilderWithQueue, self).popAll()
    self._addTrace()