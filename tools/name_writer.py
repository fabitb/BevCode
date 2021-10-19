from barcode.writer import ImageWriter, mm2px, pt2mm, ImageFont


class NameWriter(ImageWriter):

    def __init__(self, name):
        ImageWriter.__init__(self)
        self.name = name

    def _paint_text(self, xpos, ypos):
        font = ImageFont.truetype(self.font_path, self.font_size * 2)
        for subtext in self.name.split("\n"):
            width, height = font.getsize(subtext)
            # determine the maximum width of each line
            pos = (
                mm2px(xpos, self.dpi) - width // 2,
                mm2px(ypos, self.dpi) - height // 4,
            )
            self._draw.text(pos, subtext, font=font, fill=self.foreground)
            ypos += pt2mm(self.font_size) / 2 + self.text_line_distance
