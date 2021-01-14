from Priogrid import Priogrid

a = Priogrid(49201)
b = Priogrid.from_lat_lon(lat=55.25, lon=37.24)
c = Priogrid.from_row_col(row=9, col=21).next_left().queen_contiguity()
print(c)

"""
assert Priogrid(130521).queen_contiguity()[2][2].id==129802
assert Priogrid.from_lat_lon(10.51, 2.29).id == 145085
assert Priogrid.from_row_col(151, 412).id == 108412
assert Priogrid.from_row_col(151, 412).next_right().id == 108413
assert Priogrid.rowcol2id(151, 412) == 108412
assert Priogrid.rowcol2id(151, 413) == 108413
assert Priogrid.rowcol2id(151, 280) == 108280
assert Priogrid.rowcol2id(119, 616) == 85576
assert Priogrid(50618).col == 218
assert Priogrid(50618).row == 71
assert Priogrid.rowcol2id(71,218) == 50618
assert Priogrid.lat2row(10.51) == 202
assert Priogrid.lat2row(10.75) == 202
assert Priogrid.lat2row(10.03) == 201
assert Priogrid.lat2row(10.49) == 201
assert Priogrid.lat2row(-14.75) == 151
assert Priogrid.lat2row(-14.94) == 151
assert Priogrid.lat2row(-14.52) == 151
assert Priogrid.lon2col(126.52) == 614
assert Priogrid.lon2col(37.47) == 435
assert Priogrid.lon2col(-73.52) == 213
assert Priogrid.id2lat(108214) == -14.75
assert Priogrid.id2lon(108213) == -73.75
assert Priogrid.latlon2id(-14.78,25.86) == 108412
assert Priogrid.latlon2id(-8.75, 179.25) == 117359
assert Priogrid.latlon2id(70.75, 179.25) == 231839

"""