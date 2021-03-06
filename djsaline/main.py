import argparse
from jinja2 import Environment, PackageLoader
import os
import sys


class Project(object):
    _secret_key = None

    def __init__(self, **kwargs):
        self.project_name = raw_input("What's the name of your project? ")
        self.postgres = True
        self.git = True
        self.project_path = self.project_root = os.path.join(os.getcwd(), self.project_name)
        self.env = Environment(loader=PackageLoader('djsaline', 'templates'))

    def _create_file(self):
        template_files = os.listdir(os.path.join(os.getcwd(), 'templates'))
        for template_file in template_files:
                template = self.env.get_template(template_file)
                with open(os.path.join(self.project_root, self.project_name), 'wt') as fd:
                    fd.write(template.render(self._kwargs))



    @property
    def _kwargs(self):
        return {
            'postgres': self.postgres,
        }

    @property
    def root_files(self):
        files = {
            'Vagrantfile': 'vagrantfile'
        }

        files['.gitignore'] = 'gitignore'
        return files.items()

    @property
    def django_files(self):
        files = {
            'local_settings.py': 'settings_local',
        }

        return files.items()

    @property
    def salt_files(self):
        files = {
            'top.sls': 'top',
            '%s.sls' % self.project_name: 'salt_project',
            'requirements.sls': 'requirements',
            'motd': 'motd'
        }

        if self.mysql:
            files['mysql.sls'] = 'mysql'

        if self.postgres:
            files['pg_hba.conf'] = 'pgconf'
            files['postgres.sls'] = 'postgres'

        return files.items()

    def initialize(self):
        # Create root directory
        os.mkdir(self.project_name)
        self._create_file(self.root_files)

        # Create project
        os.chdir(self.project_path)
        self.project_path = os.path.join(os.getcwd(), self.project_name)
        os.mkdir(self.project_name)
        open(os.path.join(self.project_path, '__init__.py'), 'w+').close()
        self._create_file(self.django_files)

        os.chdir(self.project_name)
        # Create static directories
        os.mkdir('public')
        os.mkdir('templates')
        os.makedirs('static/css')
        os.makedirs('static/js')
        os.makedirs('static/img')
        os.makedirs('static/less')

        os.chdir('templates')
        self.project_path = os.path.join(os.getcwd())
        self._create_file([('base.html', 'base')])

        os.chdir(self.project_root)
        self.project_path = os.path.join(os.getcwd(), 'salt')
        os.makedirs('salt/roots/salt')

        if self.postgres:
            # Create the pillar directories
            os.mkdir('pillar')

        # Create minion
        self._create_file([('minion', 'minion')])

        self.project_path = os.path.join(os.getcwd(), 'salt', 'roots', 'salt')
        self._create_file(self.salt_files)

        if self.postgres:
            # create pillar directory and postgres settings.
            pillar = os.path.join(self.project_root, 'pillar')
            os.chdir(pillar)
            self.project_path = pillar

            self._create_file([
                ('top.sls', 'pillar_top'),
                ('settings.sls', 'pillar_settings')
            ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--heroku', action='store_true', default=False, help="Initialize the project for "
                                                                             "deployment to Heroku.")
    parser.add_argument('--mysql', action='store_true', default=False, help='Initialize the project with MySQL.')
    parser.add_argument('--postgres', action='store_true', default=False, help="Initialize the project with Postgres.")
    parser.add_argument('--hg', action='store_true', default=False, help="Initialize project for mercurial.")
    args = parser.parse_args()

    if args.mysql and args.postgres:
        sys.exit("You can only enable one database, you enabled both MySQL and Postgres.")

    if args.mysql and args.heroku:
        sys.exit("Enable MySQL is not valid with the heroku option.  By default postgres is enabled with "
                 "the heroku option is used.")

    project = Project(**vars(args))
    project.initialize()
