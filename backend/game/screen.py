class Screen(object):
    def __init__(self, cell_w, cell_h, w, h, logger, screen, background="", cells=[], text=""):
        self.logger = logger
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.w = w
        self.h = h
        self.screen = screen
        self.init(background, cells, text)

    def open(self):
        self.logger.open()

    def close(self):
        self.logger.close()

    def generate_line(self, cells):
        return ' | '.join([str(cells[x][0]) + ' ' + str(cells[x][1]) + ' ' + self.screen[int(cells[x][0])][int(cells[x][1])] + ' ' + str(cells[x][2]) for x in xrange(len(cells))])

    def init(self, background, cells, text):
        self.open()
        line = str(self.cell_w) + " " + str(self.cell_h) + " " + str(self.w) + " " + str(self.h) + " | "
        if background:
            line += 'all ' + background + " | " + text + " | "
        line += self.generate_line(cells)
        self.logger.log(line)

    def change_cells(self, cells, write_init=False):
        line = ''
        line += self.generate_line(cells)
        for cell in cells:
            self.screen[int(cell[0])][int(cell[1])] = cell[2]
        self.logger.log(line)


