from .AncestorAttributesExtension import AncestorAttributesExtension
from .AutoLinkTargetExtension import AutoLinkTargetExtension
from .CodeNewlinesRemovalExtension import CodeNewlinesRemovalExtension
from .StrikeExtension import StrikeExtension
from .UrlizeExtension import UrlizeExtension


class DefaultExtensions:
  
  @staticmethod
  def get():
    return [
      # расширения, встроенные в python-markdown
      'def_list',
      'headerid(forceid=False)',
      # свои расширения
      AncestorAttributesExtension(),
      AutoLinkTargetExtension(),
      CodeNewlinesRemovalExtension(),
      StrikeExtension(),
      UrlizeExtension(),
    ]
  
  @staticmethod
  def patchMarkdownGlobals():
    AncestorAttributesExtension.patchMarkdownGlobals()