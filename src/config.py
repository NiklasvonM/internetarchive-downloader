from typing import Optional, Literal, List, Tuple, Union
import yaml
from pydantic import BaseModel, root_validator, Extra


class ConfigArgs(BaseModel):
    command: Literal["download", "verify"] = "download"
    logfolder: str = "ia_downloader_logs"
    identifiers: Optional[List] = None
    search: str = ""
    threads: Literal[1, 2, 3, 4, 5] = 5
    """
    May not be greater than 5 to reduce iarchive server load
    """
    split: Literal[1, 2, 3, 4, 5] = 1
    """
    May not be greater than 5 to reduce iarchive server load
    Default: 1
    """
    verify: bool = False
    filefilters: Optional[Union[List[str], str]] = None
    invertfilefiltering: bool = False
    credentials: Optional[Tuple[str, str]] = None
    hashfile: Optional[str] = None
    cacherefresh: bool = False
    data_folders: Optional[List[str]] = None
    nopaths: bool = False
    output_folder: str = "output"
    resume: bool = False
    class Config:
        extra = Extra.ignore # or 'allow' str


    @root_validator(pre=True)
    @classmethod
    def _check_arg_values(cls, args):
        #error_message = "Argument %s has received illegal value %s!"
        assert len(args["identifiers"]) > 0
        assert args["threads"] <= 5 #Reason: Reduce iarchive server load
        assert args["split"] <= 5 #Reason: Reduce iarchive server load
        assert (args["split"] > 1 & args["threads"] == 1) or args["split"] == 1
        assert (args["credentials"] is None or len(args) == 2)
        return args

    def __contains__(self, item):
        return hasattr(self, item) and self.__getattribute__(item) is not None

    @classmethod
    def from_config_file(cls, config_file_path: str = "config/config.yaml"):
        """
        Instantiates the `ConfigArgs` from `config_file_path`.
        """
        with open(config_file_path, "r", encoding="UTF-8") as config_file:
            args = yaml.safe_load(config_file)
        return ConfigArgs(**args)
