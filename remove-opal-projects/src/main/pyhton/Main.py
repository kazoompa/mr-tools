import argparse
import json
import opal.core
import sys
from argparse import Namespace

class OpalTool:
  def __init__(self):
    self.args = Namespace()

  def run(self, args):
    try:
      self.args = args
      projects = self.getProjects()

      for project in projects:
        self.deleteProject(project['name'])
        print "Deleted project %s" % project['name']

    except Exception, e:
      print >> sys.stderr, e
      sys.exit(2)

  def getProjects(self):
    return self.sendRequest("/projects")

  def deleteProject(self, project):
    return self.sendRequest("/project/%s" % project, 'DELETE')

  def sendRequest(self, url, method='GET'):
    try:
      request = opal.core.OpalClient.build(opal.core.OpalClient.LoginInfo.parse(self.args)).new_request()
      request.fail_on_error()
      request.method(method).resource(url)
      response = request.send()

      if (self.args.verbose):
        print response.content + '\n'

      if 'GET' == method:
        return json.loads(response.content)

    except Exception, e:
      print >> sys.stderr, 'Entity error occurred: ', url, e


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--user', '-u', required=False, help='User name')
  parser.add_argument('--password', '-p', required=False, help='User password')
  parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
  parser.add_argument('--opal', '-o', required=False, default='http://localhost:8080',
                      help='Opal server base url (default: http://localhost:8082)')

  OpalTool().run(parser.parse_args())
