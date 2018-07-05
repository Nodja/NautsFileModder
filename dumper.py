import datetime

from animo.config import load_config
from animo.dump import dump_files
from animo.env import create_env


if __name__ == "__main__":
    load_config()
    create_env()
    
    date_str = datetime.datetime.now().strftime("%Y_%m_%e-%H_%M_%S")
    dump_files("_env\\Data", f"_dumps\\{date_str}")