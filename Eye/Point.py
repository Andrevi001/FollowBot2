class Point:
    """Class that defines a 2D point and it's visibilty"""

    def __init__(self, x, y, visibility):
        self.__x = x
        self.__y = y
        self.__visibility = visibility

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def visibility(self):
        return self.__visibility