import bisect


class HierarchyByIndentationBuilder:

  def __init__(self, underlyingBuilder):
    self._indents = []
    self.underlyingBuilder = underlyingBuilder

  lastIndent = property(lambda self: None if not self._indents else self._indents[-1])

  def put(self, indent, obj):
    action = self._getActionByIndent(indent)
    action(obj)

  def putLine(self, line):
    content = line.lstrip()
    self.put(line[:-len(content)], content)


  def _getActionByIndent(self, indent):
    pos = bisect.bisect_left(self._indents, indent)
    if pos == len(self._indents):
      return lambda obj: self._appendLevel(indent, obj)
    if self._indents[pos] == indent:
      return lambda obj: self._useLevel(pos, obj)
    # self._indents[pos] > indent,
    # self._indents[pos-1] < indent
    if pos > 0:
      return lambda obj: self._useLevel(pos-1, obj)
    return lambda obj: self._prependLevel(indent, obj)

  def _appendLevel(self, indent, obj):
    self._push(indent, obj)

  def _useLevel(self, n, obj):
    self._popN((len(self._indents)-1) - n)
    self._put(obj)

  def _prependLevel(self, indent, obj):
    self._popAll()
    self._push(indent, obj)


  def _push(self, indent, obj):
    self._indents.append(indent)
    self.underlyingBuilder.push(obj)

  def _put(self, obj):
    self.underlyingBuilder.put(obj)

  def _popN(self, n):
    if n == 0:
      return
    del self._indents[-n:]
    self.underlyingBuilder.popN(n)

  def _popAll(self):
    del self._indents[:]
    self.underlyingBuilder.popAll()