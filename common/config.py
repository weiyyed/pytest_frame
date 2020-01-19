# -*- coding: utf-8 -*-
import yaml
class Config():
    # def __init__(self,fspath):
    #     self.fspath=fspath
    @classmethod
    def load(cls,fspath):
        if isinstance(fspath,str):
            with open(fspath,'r') as f:
                raw=yaml.safe_load(f)
        else:
            raw = yaml.safe_load(fspath.open())
        return raw
