def test_jpeg(h, f):
    if f[6:10] in (b'JFIF', b'Exif') or (f[:2] == b'\xff\xd8' and b'JFIF' in f[:32]):
        return 'jpeg'