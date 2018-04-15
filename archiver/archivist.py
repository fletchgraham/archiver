import click
import os
from os import path, makedirs
import io
import sys
from datetime import datetime
from archiver.encipher import AESCipher
import json


class Archivist:

    def __init__(self):

        # homebase is where config file lives. doesn't change.
        self.homebase = path.join(path.expanduser('~'), '.archiver')
        self.config_path = path.join(self.homebase, 'config.json')

        # define the default config variable
        self.config = {
            'location': self.homebase,
            'encrypted': False,
            'archives': ['main']
            }

        # if homebase doesn't exist yet, create it
        if not path.exists(self.homebase):
            makedirs(self.homebase)

        if not path.exists(self.config_path):
            with open(self.config_path, 'w') as config_file:
                json.dump(self.config, config_file)

        with open(self.config_path, 'r') as config_file:
            self.config = json.loads(config_file.read())
                
        if not os.path.exists(self.config['location']):
            os.makedirs(self.config['location'])

    def get_location(self):
        return self.config['location']

    def write(self):

        # Get the text editor from the shell, otherwise default to Vim
        editor = os.environ.get('EDITOR','vim')

        # define the locations of the archive file and the temp file
        archive_path = path.join(self.config['location'], 'archive.txt')
        temp_path = path.join(self.homebase, 'temp_entry.txt')

        # HACK check to see if there is an encrypted archive
        if os.path.exists(os.path.join(self.config['location'], 'archive.txt.enc')):
            click.echo(
                'Your archive is encrypted,' +
                ' run "arc decrypt" and then enter your key.'
                )
            return False
        else:

            # create the temp file with a helpful message
            with open(temp_path, 'w') as temp:
                temp.write('')

            # open the temp file with an editor so the user can write their entry
            os.system(editor + ' ' + '"' + temp_path + '"')

            # read the entry from the temp file once the user has saved their entry
            with open(temp_path, 'rU') as temp:
                entry = temp.read()

            # nuke all any temp files that were created by archiver or the text editor
            for file in os.listdir(self.homebase):
                if 'temp_entry' in file:
                    os.remove(os.path.join(self.homebase, file))

            # get the current time
            timestamp = datetime.now().isoformat(timespec='seconds')

            # write the whole thing to the archive
            with open(archive_path, 'a') as archive_file:
                archive_file.write('\n\n||\n\n' + timestamp + '\n\n|\n\n' + entry)
            return True

    def read(self):
        # HACK check to see if there is an encrypted archive
        if os.path.exists(os.path.join(self.config['location'], 'archive.txt.enc')):
            click.echo(
                'Your archive is encrypted,' +
                ' run "arc decrypt" and then enter your key.'
                )
            return False
        else:
            with open (os.path.join(self.config['location'], 'archive.txt'), 'r') as archive:
                return archive.read()




            
