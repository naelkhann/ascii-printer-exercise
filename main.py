
class AsciiPrinter:
    def __init__(self):
        # Each coord in canvas is a stack (can have multiple layers)
        self.canvas = [[[] for i in range(10)] for i in range(6)]
        self.layers = []
        self.rectangles = {}

    # Prints current canvas (10 x 6 max)
    def printCanvas(self):
        # Add column of x-axis identifiers
        print(" ".join(["X"] + [str(i) for i in range(10)]))
        for i in range(6):
            # Add column of y-axis identifiers
            row = [str(i)]
            for layers in self.canvas[i]:
                last_layer = len(layers)
                # Get fill_char of top most layer
                if last_layer:
                    row.append(layers[last_layer - 1])
                else:
                    row.append("-")
            print(" ".join(row))

    # Draw rect at x1,y1 (top left) to x2,y2 (bottom right)
    def drawRect(self, args, layer=None):
        def rankByLayer(item):
            if item not in self.layers:
                return 0
            return self.layers.index(item)

        fill_char, left_x, top_y, right_x, bottom_y = args

        for i in range(int(top_y), int(bottom_y) + 1):
            for j in range(int(left_x), int(right_x) + 1):
                fill_char_layer_idx = None
                if fill_char in self.layers:
                    fill_char_layer_idx = self.layers.index(fill_char)
                # Append layer fill_char
                self.canvas[i][j].append(fill_char)
                # Sort layers
                self.canvas[i][j].sort(key=rankByLayer)

        self.layers.append(fill_char)
        self.rectangles[fill_char] = {
            "fill_char": fill_char,
            "left_x": left_x,
            "top_y": top_y,
            "right_x": right_x,
            "bottom_y": bottom_y
        }

    # Erase all layers in area
    def eraseArea(self, args):
        left_x, top_y, right_x, bottom_y = args
        for i in range(int(top_y), int(bottom_y) + 1):
            for j in range(int(left_x), int(right_x) + 1):
                self.canvas[i][j] = []

    # Drag and drop from a select coordinate
    # Grabs rect at coordinate, and moves rect to new coordinate maintaining original shape
    def dragAndDrop(self, args):
        def removeRect(fill_char, i, j):
            if fill_char not in self.canvas[i][j]:
                return

            idx = self.canvas[i][j].index(fill_char)
            self.canvas[i][j].pop(idx)

            removeRect(fill_char, i + 1, j)
            removeRect(fill_char, i - 1, j)
            removeRect(fill_char, i, j + 1)
            removeRect(fill_char, i, j - 1)

        def calcEdges(fill_char, select_x, select_y, release_x, release_y):
            top_y = self.rectangles[fill_char]["top_y"]
            bottom_y = self.rectangles[fill_char]["bottom_y"]
            left_x = self.rectangles[fill_char]["left_x"]
            right_x = self.rectangles[fill_char]["right_x"]
            deltaTop = select_y - int(top_y)
            deltaBottom = int(bottom_y) - select_y
            deltaLeft = select_x - int(left_x)
            deltaRight = int(right_x) - select_x
            newTop = release_y - deltaTop
            newBottom = release_y + deltaBottom
            newLeft = release_x - deltaLeft
            newRight = release_x + deltaRight
            removeRect(fill_char, select_y, select_x)
            self.drawRect([fill_char, newLeft, newTop, newRight, newBottom])

        select_x, select_y, release_x, release_y = args
        select_x = int(select_x)
        select_y = int(select_y)
        release_x = int(release_x)
        release_y = int(release_y)
        # Get top most layer at coord
        coord_has_rect = self.canvas[select_y][select_x][0]
        if coord_has_rect:
            fill_char = self.canvas[select_y][select_x][0]
            calcEdges(fill_char, select_x, select_y, release_x, release_y)

    # Parses line instruction, grabbing command and using rest of line as args for command
    def parseCommand(self, command, args):
        match command:
            case "PRINT_CANVAS":
                print("printing canvas")
                self.printCanvas()
            case "DRAW_RECTANGLE":
                print("drawing rectangle")
                self.drawRect(args)
            case "ERASE_AREA":
                print("erasing area")
                self.eraseArea(args)
            case "DRAG_AND_DROP":
                print("dragging and dropping")
                self.dragAndDrop(args)


def main():
    # Parse instruction file
    instructions = open("instruction_file.txt", "r")
    ascii_printer = AsciiPrinter()
    # Go through line and parse command and args out of each line
    for line in instructions:
        line_arr = line.strip().split(" ")
        # First arg is the command itself
        command = line_arr[0]
        # Remaining args are positional args for command (if command needs it)
        command_args = line_arr[1:]
        ascii_printer.parseCommand(command, command_args)


if __name__ == "__main__":
    main()
