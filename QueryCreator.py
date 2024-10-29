import re

class Query:
    def __init__(self, reg: str, groups_to_resp_func):
        self.reg = reg
        self.groups_to_resp_func = groups_to_resp_func

    def resp(self, query):
        resp = re.search(self.reg, query)

        if resp is None:
            return None

        return self.groups_to_resp_func(*resp.groups())