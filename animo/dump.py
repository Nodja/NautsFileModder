import glob
import json
import os
import re


from animo.filetools import decrypt, createandwrite
from animo.binded import unbind
from animo.config import get_config

def dump_files(src, dst, base="_env"):
    base = os.path.abspath(base)
    file_structure = glob.glob(f"{src}/**", recursive=True)
    
    config = get_config()
    skip_decrypt = json.loads(config['dump']['skip_decrypt'])
    skip_decrypt = tuple([path.lower() for path in skip_decrypt])
    
    for path in file_structure:
        if not os.path.isfile(path):
            continue
        
        rel_path = os.path.relpath(path, base)
            
        decrypt_path = rel_path.lower()
        
        if decrypt_path.startswith(skip_decrypt):
            continue
            
        print(f"Dumping {path}")
        data_encrypted = open(path, "rb").read()
        data_decrypted = decrypt(data_encrypted, decrypt_path)
        
        if decrypt_path.endswith("binded"):
            binded_dir = re.sub('\d+\.binded$', '.binded', rel_path)
            binded_dir = os.path.join(dst, binded_dir)
            for bindedfile in unbind(data_decrypted):
                bf_name = bindedfile[0]
                bf_data = bindedfile[1]
                out_path = os.path.join(binded_dir, bf_name)
                createandwrite(out_path, bf_data)
        
        createandwrite(f"{dst}\\{rel_path}", data_decrypted)