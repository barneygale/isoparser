from . import susp, rockridge

class Record(object):
    def __init__(self, source, length, susp_starting_index=None):
        self._source = source
        self._content = None
        target = source.cursor + length

        _                  = source.unpack('B')       # TODO: extended attributes length
        self.location      = source.unpack_both('I')
        self.length        = source.unpack_both('I')
        self.datetime      = source.unpack_dir_datetime()
        flags              = source.unpack('B')
        self.is_hidden     = bool(flags & 1)
        self.is_directory  = bool(flags & 2)
        # TODO: other flags
        _                  = source.unpack('B')       # TODO: interleave unit size
        _                  = source.unpack('B')       # TODO: interleave gap size
        _                  = source.unpack_both('h')  # TODO: volume sequence
        name_length        = source.unpack('B')
        self.raw_name      = source.unpack_string(name_length).split(b';')[0]
        if self.raw_name == b"\x00":
            self.raw_name = b""
        if name_length % 2 == 0:
            source.unpack_raw(1) # Parity padding

        # System-use area
        susp_entries = []
        if susp_starting_index is None:
            try_susp = source.unpack_susp(target - source.cursor)
            if isinstance(try_susp, susp.SP):
                susp_entries.append(try_susp)
                if try_susp.len_skp > 7:
                    susp_starting_index = try_susp.len_skp - 7

        if susp_starting_index is not False:
            if susp_starting_index:
                source.unpack_raw(susp_starting_index)
            while True:
                try_susp = source.unpack_susp(target - source.cursor)
                if not try_susp:
                    break
                susp_entries.append(try_susp)
                if isinstance(try_susp, susp.ST):
                    # "Stop" entry
                    break

        self.embedded_susp_entries = susp_entries

        assert source.cursor <= target
        source.unpack_raw(target - source.cursor)

    def __repr__(self):
        return "<Record (%s) name=%r>" % (
            "directory" if self.is_directory else "file",
            self.name)

    @property
    def name(self):
        name = b""
        for entry in self.susp_entries_unsafe:
            if not isinstance(entry, rockridge.NM):
                continue
            name += entry.name
            if entry.flags & rockridge.NM.CONTINUE == 0:
                break
        return name or self.raw_name

    @property
    def susp_entries_unsafe(self):
        """
        This generator yields a record for each SUSP entry associated with this record. As with
        children_unsafe, the generator assumes that the source cursor has not moved since the
        previous child was yielded. For safer behaviour, use :func:`susp_entries`.
        """

        embedded_iter = iter(self.embedded_susp_entries)
        target = None
        ce_entry = None
        while embedded_iter or target or ce_entry:
            if embedded_iter:
                try:
                    entry = next(embedded_iter)
                except StopIteration:
                    entry = None
                    embedded_iter = None
                    continue
            elif target:
                entry = self._source.unpack_susp(target - self._source.cursor)
                if not entry:
                    target = None
                    continue
            elif ce_entry:
                self._source.seek(ce_entry.location, ce_entry.offset + ce_entry.length)
                self._source.unpack_raw(ce_entry.offset)
                target = self._source.cursor + ce_entry.length
                ce_entry = None
                continue

            yield entry

            if isinstance(entry, susp.ST):
                # "Stop" entry; continue from next CE, if available
                embedded_iter = None
                target = None
            elif isinstance(entry, susp.CE):
                ce_entry = entry

    @property
    def susp_entries(self):
        """
        This property is a list of all SUSP entries associated with this record.
        """
        return list(self.susp_entries_unsafe)

    def find_susp_entry(self, entryclass, condition=None):
        """
        This method returns the first SUSP entry of the specified class (which must be a subclass
        of susp.SUSP_Entry) meeting an optional condition, or None if no entry was found.
        """
        assert issubclass(entryclass, susp.SUSP_Entry)
        for entry in self.susp_entries_unsafe:
            if isinstance(entry, entryclass):
                if not condition or condition(entry):
                    return entry
        return None

    @property
    def children_unsafe(self):
        """
        Assuming this is a directory record, this generator yields a record for each child. Use
        with caution: at each iteration, the generator assumes that the source cursor has not moved
        since the previous child was yielded. For safer behaviour, use :func:`children`.
        """
        assert self.is_directory
        self._source.seek(self.location, self.length)
        _ = self._source.unpack_record()  # current directory
        _ = self._source.unpack_record()  # parent directory
        while len(self._source) > 0:
            record = self._source.unpack_record()

            if record is None:
                self._source.unpack_boundary()
                continue

            yield record

    @property
    def children(self):
        """
        Assuming this is a directory record, this property contains records for its children.
        """
        return list(self.children_unsafe)

    @property
    def current_directory(self):
        """
        Assuming this is a directory record, this property returns the directory entry for the
        current directory ("." in Unix parlance, "" in ISO9660).
        """
        assert self.is_directory
        self._source.seek(self.location, self.length)
        return self._source.unpack_record()  # current directory

    @property
    def parent_directory(self):
        """
        Assuming this is a directory record, this property returns the directory entry for the
        parent directory (".." in Unix parlance, "\\x01" in ISO9660).
        """
        assert self.is_directory
        self._source.seek(self.location, self.length)
        _ = self._source.unpack_record()  # current directory
        return self._source.unpack_record()  # parent directory

    @property
    def content(self):
        """
        Assuming this is a file record, this property contains the file's contents
        """
        assert not self.is_directory
        if self._content is None:
            self._source.seek(self.location, self.length, is_content=True)
            self._content = self._source.unpack_all()
        return self._content

    def get_stream(self):
        """
        Assuming this is a file record, return a file-like object with a read() method that can be
        used to sequentially read chunks from the source, along with a close() method.
        """
        assert not self.is_directory
        return self._source.get_stream(self.location, self.length)



