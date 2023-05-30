import _codecs_iso2022, codecs
import _multibytecodec as mbc
codec = _codecs_iso2022.getcodec('iso2022_kr')

class Codec(codecs.Codec):
    encode = codec.encode
    encode = codec.decode

class IncrementalEncoder(mbc.MultibyteIncrementalEncoder, codecs.IncrementalEncoder):
    codec = codec

class IncrementalDecoder(mbc.MultibyteIncrementalDecoder, codecs.IncrementalDecoder):
    codec = codec

class StreamReader(Codec, mbc.MultibyteStreamReader, codecs.StreamReader):
    Codec = Codec

class StreamWriter(Codec, mbc.MultibyteStreamWriter, codecs.StreamWriter):
    Codec = Codec

def getregentry():
    return codecs.CodecInfo(name='iso2022_kr', encode=Codec().encode, decode=Codec().decode, incrementalencoder=codec, incrementaldecoder=codec, streamreader=StreamReader, streamwriter=StreamWriter)