
 def findDeltas(fill_char, select_x, select_y):
      # Traverse each direction until end of rect (canvas[i][j] != fil_char)
      # --
      # Find delta_left
      delta = select_x
       while self.canvas[select_y][delta] == fill_char:
            delta -= 1
        delta_left = select_x - delta

        # Find delta_top
        delta = select_y
        while self.canvas[delta][select_x] == fill_char:
            delta -= 1
        delta_top = select_y - delta

        # Find delta_right
        delta = select_x
        while self.canvas[select_y][delta] == fill_char:
            delta += 1
        delta_right = delta - select_x

        # Find delta_bottom
        delta = select_y
        while self.canvas[delta][select_x] == fill_char:
            delta += 1
        delta_bottom = delta - select_y

        return [delta_left, delta_top, delta_right, delta_bottom]
