from six import add_metaclass, iteritems

class SUSPError(Exception):
    pass

def susp_assert(condition):
    if not condition:
        raise SUSPError("Failed SUSP assertion")

class susp_meta(type):
    def __new__(mcs, name, bases, dict):
        cls = type.__new__(mcs, name, bases, dict)
        if '_implements' in dict:
            for i in dict['_implements']:
                SUSP_Entry._registered_classes[i] = cls
        return cls

@add_metaclass(susp_meta)
class SUSP_Entry(object):
    _registered_classes = {}
    _repr_props = ()

    @classmethod
    def unpack(cls, source, ext_id_ver, sig_version, length):
        implementing_class = None
        if ext_id_ver:
            implementing_class = cls._registered_classes.get(ext_id_ver + sig_version)
        if not implementing_class:
            ext_id_ver = None
            implementing_class = cls._registered_classes.get(sig_version, UnknownEntry)
        return implementing_class(source, ext_id_ver, sig_version, length)

    def __init__(self, source, ext_id_ver, sig_version, length):
        self.ext_id_ver = ext_id_ver
        self.sig_version = sig_version
        self.signature, self.version = sig_version

    def __repr__(self):
        return "<SUSP (%s,%d)%s>" % (
            self.signature, self.version,
            ''.join(" %s=%s" % (k,repr(v)) for k,v in self._repr_keyvals))

    @property
    def _repr_keyvals(self):
        for prop in self._repr_props:
            yield prop, getattr(self, prop)

class UnknownEntry(SUSP_Entry):
    def __init__(self, source, ext_id_ver, sig_version, length):
        super(UnknownEntry, self).__init__(source, ext_id_ver, sig_version, length)
        self.unknown_raw = source.unpack_raw(length)

    @property
    def _repr_keyvals(self):
        return iteritems({'unknown/length': len(self.unknown_raw)+4})

class SP(SUSP_Entry):
    _implements = [
        ('SP', 1),
    ]

    _repr_props = ('len_skp',)

    def __init__(self, source, ext_id_ver, sig_version, length):
        super(SP, self).__init__(source, ext_id_ver, sig_version, length)
        susp_assert(length == 3)
        susp_assert(source.unpack_raw(2) == b"\xbe\xef")
        self.len_skp = source.unpack('B')

class CE(SUSP_Entry):
    _implements = [
        ('CE', 1),
    ]

    _repr_props = ('location', 'offset', 'length')

    def __init__(self, source, ext_id_ver, sig_version, length):
        super(CE, self).__init__(source, ext_id_ver, sig_version, length)
        susp_assert(length == 24)
        self.location = source.unpack_both('I')
        self.offset   = source.unpack_both('I')
        self.length   = source.unpack_both('I')

class PD(SUSP_Entry):
    _implements = [
        ('PD', 1),
    ]

    def __init__(self, source, ext_id_ver, sig_version, length):
        super(PD, self).__init__(source, ext_id_ver, sig_version, length)
        if length:
            source.unpack_raw(length) # Padding, ignored

class ST(SUSP_Entry):
    _implements = [
        ('ST', 1),
    ]

    def __init__(self, source, ext_id_ver, sig_version, length):
        super(ST, self).__init__(source, ext_id_ver, sig_version, length)
        susp_assert(length == 0)

class ER(SUSP_Entry):
    _implements = [
        ('ER', 1),
    ]

    _repr_props = ('ext_id', 'ext_ver')

    def __init__(self, source, ext_id_ver, sig_version, length):
        super(ER, self).__init__(source, ext_id_ver, sig_version, length)
        susp_assert(length >= 4)
        len_id  = source.unpack('B')
        len_des = source.unpack('B')
        len_src = source.unpack('B')
        susp_assert(length == 4 + len_id + len_des + len_src)
        self.ext_ver = source.unpack('B')
        self.ext_id  = source.unpack_raw(len_id).decode()
        self.ext_des = source.unpack_raw(len_des).decode()
        self.ext_src = source.unpack_raw(len_src).decode()

class ES(SUSP_Entry):
    _implements = [
        ('ES', 1),
    ]

    _repr_props = ('ext_seq',)

    def __init__(self, source, ext_id_ver, sig_version, length):
        super(ER, self).__init__(source, ext_id_ver, sig_version, length)
        susp_assert(length == 1)
        self.ext_seq = source.unpack('B')

from . import rockridge
