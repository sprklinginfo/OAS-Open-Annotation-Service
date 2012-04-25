from seecr.test import SeecrTestCase

from meresco.components.http.utils import CRLF
from oas.harvester import Dashboard, Environment
from oas.login.basichtmlloginform import User

from testutil import joco

from urllib import urlencode

class DashboardTest(SeecrTestCase):
    def setUp(self):
        SeecrTestCase.setUp(self)
        self.dashboard = Dashboard()
        self.env = Environment(root=self.tempdir)
        self.dashboard.addObserver(self.env)

    def testRedirectOnGet(self):
        result = joco(self.dashboard.handleRequest(path='/whatever', Client=('127.0.0.1', 3451), Method='GET', session={}))
        header, body = result.split(CRLF*2)
        self.assertTrue('302' in header)
        self.assertTrue('Location: /' in header, header)

    def testCreateNotLoggedIn(self):
        result = joco(self.dashboard.handleRequest(path="/create", Client=('127.0.0.1', 1234), Method='POST', session={}))
        header, body = result.split(CRLF*2)
        self.assertTrue('302' in header)
        self.assertTrue('Location: /' in header, header)

    def testCreateLoggedIn(self):
        session = {
            'user': User('admin'),
        }
        Body = urlencode(dict(repository='repoId1', formUrl='/harvester_dashboard?repository=%(repository)s'))
        result = joco(self.dashboard.handleRequest(path="/create", Client=('127.0.0.1', 1234), Method='POST', session=session, Body=Body))
        header, body = result.split(CRLF*2)
        self.assertTrue('302' in header)
        self.assertTrue('Location: /harvester_dashboard?repository=repoId1' in header, header)

        self.assertEquals("repoId1", list(self.env.getRepositories())[0].name)

    def testEditRepository(self):
        session = dict(user=User('admin'))
        
        joco(self.dashboard.handleRequest(
            path="/create", 
            Client=('127.0.0.1', 1234), 
            Method='POST', 
            session=session, 
            Body=urlencode(dict(repository='repoId1', formUrl='/harvester_dashboard'))))

        self.assertEquals("", list(self.env.getRepositories())[0].baseUrl)
        self.assertEquals("", list(self.env.getRepositories())[0].metadataPrefix)
        self.assertEquals("", list(self.env.getRepositories())[0].setSpec)
        self.assertEquals("", list(self.env.getRepositories())[0].apiKey)
        self.assertEquals(False, list(self.env.getRepositories())[0].active)
        joco(self.dashboard.handleRequest(
            path="/something/update", 
            Client=('127.0.0.1', 1234), 
            Method='POST', 
            session=session, 
            Body=urlencode(dict(
                repository='repoId1', 
                baseUrl='http://localhost/oai',
                metadataPrefix='aprefix',
                setSpec='aset',
                apiKey='an api key',
                active='on',
                formUrl='/harvester_dashboard'))))
        self.assertEquals("http://localhost/oai", list(self.env.getRepositories())[0].baseUrl)
        self.assertEquals("aprefix", list(self.env.getRepositories())[0].metadataPrefix)
        self.assertEquals("aset", list(self.env.getRepositories())[0].setSpec)
        self.assertEquals("an api key", list(self.env.getRepositories())[0].apiKey)
        self.assertEquals(True, list(self.env.getRepositories())[0].active)

        joco(self.dashboard.handleRequest(
            path="/something/update", 
            Client=('127.0.0.1', 1234), 
            Method='POST', 
            session=session, 
            Body=urlencode(dict(
                repository='repoId1', 
                baseUrl='http://localhost/oai',
                metadataPrefix='aprefix',
                setSpec='aset',
                apiKey='an api key',
                formUrl='/harvester_dashboard'))))
        self.assertEquals(False, list(self.env.getRepositories())[0].active)

    def testDeleteRepository(self):
        session = dict(user=User('admin'))
        
        joco(self.dashboard.handleRequest(
            path="/create", 
            Client=('127.0.0.1', 1234), 
            Method='POST', 
            session=session, 
            Body=urlencode(dict(repository='repoId1', formUrl='/harvester_dashboard'))))
        self.assertEquals(1, len(list(self.env.getRepositories())))
        result = joco(self.dashboard.handleRequest(
            path="/delete", 
            Client=('127.0.0.1', 1234), 
            Method='POST', 
            session=session, 
            Body=urlencode(dict(repository='repoId1', formUrl='/harvester_dashboard'))))
        self.assertEquals(0, len(list(self.env.getRepositories())))
        header, body = result.split(CRLF*2)

        self.assertTrue('302' in header)
        self.assertTrue('Location: /harvester_dashboard' in header, header)
