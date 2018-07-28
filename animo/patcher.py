import re

import pymem
from pymem import Pymem as _Pymem

from animo.config import get_config

class PatchError(Exception):
    pass
    
class Pymem(_Pymem):
    def write_bytes(self, address, value):
        if not self.process_handle:
            raise pymem.exception.ProcessError('You must open a process before calling this method')
        if value is None or not isinstance(value, bytes):
            raise TypeError('Invalid argument: {}'.format(value))
        try:
            pymem.memory.write_bytes(self.process_handle, address, value, len(value))
        except pymem.exception.WinAPIError as e:
            raise pymem.exception.MemoryWriteError(address, value, e.error_code)


def patch_game():
    config = get_config()
    
    def hex_pattern(pattern_string):
        _string = pattern_string.replace(' ', '')
        _pattern = b''
        for byte in re.findall('..', _string):
            if byte == '??':
                _pattern += b'.'
                continue
            _pattern += bytes.fromhex(byte)
        return _pattern
        
    sig = hex_pattern(config['patcher']['sig'])
    offset = int(config['patcher']['offset'])
    expected = bytes.fromhex(config['patcher']['expected'])
    replace_with = bytes.fromhex(config['patcher']['replace_with'])
    
    pm = Pymem("awesomenauts.exe")
    
    size = 2048
    
    def search_and_patch(start_address):
        _address = start_address
        patched = False
        while True:
            try:
                buffer = pm.read_bytes(_address, size)
            except:
                break
            sig_pattern = re.compile(sig)
            pattern_match = re.search(sig_pattern, buffer)
            if pattern_match is not None:
                local_offset = pattern_match.start()
                if expected == pm.read_bytes(_address + local_offset, len(expected)):
                    print(f"Target code found at {_address + local_offset}, patching...")
                    pm.write_bytes(_address + local_offset, replace_with)
                    patched = True
            _address += len(buffer)
        if patched is False:
            raise PatchError("Patching failed. No signature found.")
    
    address = int(pm.process_base_address, 16)
    try:
        search_and_patch(address)
    except PatchError:
        search_and_patch(address + (size / 2))
    
    