class Loggable():
  row = None
  col = None
  message = ''


def error(loggable):
  if loggable.row is not None and loggable.col is not None:
    print('At %d:%d'%(loggable.row, loggable.col))
  print(loggable.message)
