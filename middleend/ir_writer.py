class IRWriter:
  outfile = None

  def __init__(self, path):
    self.outfile = open(path)

  def create_label(self, label):
    self.outfile.write('LABEL %s:\n'%label)


