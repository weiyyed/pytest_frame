import os
import pytest
import requests
# from httprunner.client import HttpSession

from common import tags, config, asserts

root_dir=os.path.dirname(os.path.dirname(__file__))
env_conf_file=os.path.join(root_dir,'config','env.yml')
ENV=config.Config.load(env_conf_file)

class Feature(pytest.File):
    def collect(self):
        count = 1
        feature = config.Config.load(self.fspath)
        base = feature.get(tags.BASE)
        use_session = feature.get(tags.USE_SESSION, True)

        if feature.get(tags.SCENARIOS) is not None:
            for s in feature.get(tags.SCENARIOS):
                name = s.get(tags.DESC, '{}_{}'.format(self.name, count))
                count += 1
                ins = s.get(tags.INS)
                outs = s.get(tags.OUTS)
                if isinstance(ins, dict) and isinstance(outs, dict):
                    yield Scenario(name, self, base, ins, outs, use_session)


class Scenario(pytest.Item):
    def __init__(self, name, parent, base=None, ins=None, outs=None, use_session=True):
        super(Scenario, self).__init__(name, parent)
        self.name = name
        self.base = base
        self.ins = ins
        self.outs = outs
        self.use_session = use_session

    def _append_attrs(self, src, ext, tag=tags.HEADERS):
        if isinstance(ext, dict) and ext.get(tag) is not None:
            for key in ext.get(tag):
                if key not in src:
                    src[key] = ext.get(tag).get(key)

    def runtest(self):
        url = (ENV.get(tags.ENV_BASE_URL, '') + self.base.get(tags.URL, '') + self.ins.get(tags.URL, '/')).replace(
            '[^:]//', '/')
        if not url.endswith('/'): url = url + '/'

        headers = self.ins.get(tags.HEADERS, {})
        self._append_attrs(headers, self.base, tags.HEADERS)
        self._append_attrs(headers, ENV, tags.ENV_BASE_HEADER)

        method = self.ins.get(tags.METHOD)
        data = self.ins.get(tags.DATA)
        expected = self.outs

        req = requests.Request(url=url, headers=headers, method='POST')
        if method is not None and str(method).upper() == 'GET':
            req.method = 'GET'
            req.params = data
        else:
            req.data = data

        http_session = requests.session()
        if self.use_session:
            http_session = HttpSession()
            prep = http_session.prepare_request(req)
        else:
            prep = req.prepare()

        resp = http_session.send(prep)
        asserts.assert_dict(resp.json(), expected)

class HttpSession(requests.Session):
    pass