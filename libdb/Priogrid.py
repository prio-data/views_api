from __future__ import annotations
from typing import List

class Priogrid(object):

    def __init__(self, id: int):
        self.id = id
        self.row = self.id2row(id)
        self.col = self.id2col(id)
        self.lat = self.id2lat(id)
        self.lon = self.id2lon(id)

    def __repr__(self):
        return f'Priogrid({self.id})'

    def __str__(self):
        return f'Priogrid(id={self.id}) #=> row:{self.row}, col:{self.col}, lat:{self.lat}, lon:{self.lon}'

    @classmethod
    def from_lat_lon(cls, lat: float, lon: float) -> Priogrid:
        """
        A factory producing a Priogrid Object from a lat and lon
        :param lat: A WGS84 valid lat (i.e. -90..90)
        :param lon: A WGS84 valid lon (i.e. -180..180)
        :return: A Priogrid Object at that position
        """
        return cls(cls.latlon2id(lat, lon))


    @classmethod
    def from_row_col(cls, row: int, col: int) -> Priogrid:
        """
        A factory producing a Priogrid Object from a row and col
        :param row: A Priogrid valid row (i.e. 0..360)
        :param col: A Priogrid valid col (i.e. 0..720)
        :return: A Priogrid Object at the (row,col) position
        """
        return cls(cls.rowcol2id(row, col))

    def next_right(self) -> Priogrid:
        """
        A factory method returning a Priogrid Object situated to the RIGHT of the currentone
        :return: A Priogrid Object
        """
        if self.col < 720:
            return Priogrid.from_row_col(self.row, self.col+1)
        else:
            return None

    def next_left(self) -> Priogrid:
        if self.col > 1:
            return Priogrid.from_row_col(self.row, self.col-1)
        else:
            return None

    def next_down(self) -> Priogrid:
        if self.row > 1:
            return Priogrid.from_row_col(self.row-1, self.col)
        else:
            return None

    def next_up(self) -> Priogrid:
        if self.row < 360:
            return Priogrid.from_row_col(self.row+1, self.col)
        else:
            return None

    def rook_contiguity(self) -> List[List[Priogrid]]:
        """
        Factory object, producing the rook contiguity matrix (3x3 cross convolution kernel) of the current object
        Objects outside of edges return None.
        :return: A matrix (2-D List of lists) of Priogrid objects representing the rook contiguity matrix
        """
        up = [None, self.next_up(), None]
        center = [self.next_left(), self, self.next_right()]
        down = [None, self.next_down(), None]
        return [up, center, down]

    def queen_contiguity(self) -> List[List[Priogrid]]:
        """
        Factory object, producing the queen contiguity matrix (3x  convolution kernel) of the current object
        Objects outside of edges return None.
        :return: A matrix (2-D List of lists) of Priogrid objects representing the queen contiguity matrix
        """

        queen = self.rook_contiguity()
        if queen[0][1] is not None:
            queen[0][0] = queen[0][1].next_left()
            queen[0][2] = queen[0][1].next_right()
        if queen[2][1] is not None:
            queen[2][0] = queen[2][1].next_left()
            queen[2][2] = queen[2][1].next_right()
        return queen

    @classmethod
    def id2lat(cls, id):
        """
        Return a centroid latitude for a given id.
        :param id: id
        :return: a centroid (x.25) lat position for the cell identified by id
        """
        return cls.row2lat(cls.id2row(id))

    @classmethod
    def id2lon(cls, id):
        """
        Return a centroid longitude for a given id.
        :param id: id
        :return: a centroid (x.25) lon position for the cell identified by id
        """
        return cls.col2lon(cls.id2col(id))

    @classmethod
    def latlon2id(cls, lat, lon):
        """
        Returns a Priogrid ID from a lat and lon set of floats
        :param lat: latitude
        :param lon: longitude
        :return: a pg id
        """
        row = cls.lat2row(lat)
        col = cls.lon2col(lon)
        id = cls.rowcol2id(row, col)
        return id

    @staticmethod
    def id2row(id):
        return int(id / 720)+1

    @staticmethod
    def id2col(id):
        return id % 720

    @staticmethod
    def rowcol2id(row, col):
        return (row-1)*720+col

    @staticmethod
    def lat2row(lat):
        return int(abs(-90 - lat) / 0.5) + 1

    @staticmethod
    def lon2col(lon):
        return int(abs(-180 - lon) / 0.5) + 1

    @staticmethod
    def col2lon(col):
        return (-180+(col*0.5))-0.25

    @staticmethod
    def row2lat(row):
        return (-90+(row*0.5))-0.25

