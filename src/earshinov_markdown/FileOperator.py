import sys


class FileOperator:

  def __init__(self, converter):
    self.__converter = converter

  def process(self, text):
    return self.__converter.convert(text)

  def processFiles(self, sourceFilename, outputFilename):

    if sourceFilename is None:
      source = sys.stdin.read()
    else:
      with open(sourceFilename, encoding='utf-8') as file:
        source = file.read()

    output = self.process(source)

    if outputFilename is None:
      print(output)
    else:
      with open(outputFilename, 'w', encoding='utf-8') as file:
        file.write(output)

  def processConsole(self, args):
    if len(args) == 1:
      inputFilename = None
      outputFilename = None
    elif len(sys.argv) == 3:
      inputFilename = args[1]
      outputFilename = args[2]
    else:
      print('Usage: %s [INPUT.html OUTPUT.html]' % args[0], file=sys.stderr)
      exit(1)
    self.processFiles(inputFilename, outputFilename)