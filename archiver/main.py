import click
import os
import io
import sys
from datetime import datetime
from archiver.encipher import AESCipher

class Archivist:

    def __init__(self):

        # get the path to the config file
        home = os.path.expanduser('~')
        root = os.path.join(home, '.archiver')
        config_path = os.path.join(root, 'config.txt')

        # if the config file doesn't exist, create it
        # then load it into the location variable
        if not os.path.exists(root):
            os.makedirs(root)

        if not os.path.exists(config_path):
            with open(config_path, 'w') as config_file:
                config_file.write(root)

        with open(config_path, 'r') as config_file:
            location = os.path.normpath(config_file.read())
                
                              
        self.location = location
        if not os.path.exists(self.location):
            os.makedirs(self.location)

    def get_location(self):
        return self.location

    def set_location(self, new_location):
        pass
        # change the contents of config file to new location
        # update self.location variable

    def write(self):

        # Get the text editor from the shell, otherwise default to Vim
        editor = os.environ.get('EDITOR','vim')

        # define the locations of the archive file and the temp file
        archive_path = os.path.join(self.location, 'archive.txt')
        temp_path = os.path.join(self.location, 'temp_entry.txt')

        # HACK check to see if there is an encrypted archive
        if os.path.exists(os.path.join(self.location, 'archive.txt.enc')):
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
            os.system(editor + ' ' + temp_path)

            # read the entry from the temp file once the user has saved their entry
            with open(temp_path, 'rU') as temp:
                entry = temp.read()

            # nuke all any temp files that were created by archiver or the text editor
            for file in os.listdir(self.location):
                if 'temp_entry' in file:
                    os.remove(os.path.join(self.location, file))

            # get the current time
            timestamp = datetime.now().isoformat(timespec='seconds')

            # write the whole thing to the archive
            with open(archive_path, 'a') as archive_file:
                archive_file.write('\n\n||\n\n' + timestamp + '\n\n|\n\n' + entry)
            return True

    def read(self):
        # HACK check to see if there is an encrypted archive
        if os.path.exists(os.path.join(self.location, 'archive.txt.enc')):
            click.echo(
                'Your archive is encrypted,' +
                ' run "arc decrypt" and then enter your key.'
                )
            return False
        else:
            with open (os.path.join(self.location, 'archive.txt'), 'r') as archive:
                return archive.read()
        

@click.group()
def archiver():
    pass


@archiver.command()
def write():
    # spin up the archivist object
    archivist = Archivist()
    # run the write method of the archivist
    written = archivist.write()
    # tell the user what happened

    if written:
        click.echo('Your entry was written to the archive.')

    else:
        pass



@archiver.command()
def read():
    # spin up the archivist object
    archivist = Archivist()
    click.echo(archivist.read())

@archiver.command()
def location():
    archivist = Archivist()
    click.echo(archivist.get_location())

@archiver.command()
def encrypt():

    # spin up archivist just to get location
    archivist = Archivist()
    path_to_txt = os.path.join(archivist.get_location(), 'archive.txt')

    # ask the user for a key
    key = input('Type in a key to use for encryption >>>')

    # get the contents of the archive
    with open(path_to_txt, 'r') as f:
        contents = f.read()
        
    newfile = path_to_txt + '.enc'
    
    cipher = AESCipher(key)
    
    with open(newfile, 'wb') as new:
        new.write(cipher.encrypt(contents))

    # remove the unencrypted file
    os.remove(path_to_txt)
    
    click.echo('Your file was encrypted.')

@archiver.command()
def decrypt():

    # spin up archivist just to get location
    archivist = Archivist()
    path_to_enc = os.path.join(archivist.get_location(), 'archive.txt.enc')

    # ask the user for a key
    key = input('Type in a key to use for decryption >>>')
    
    with open(path_to_enc, 'rb') as f:
        contents = f.read()
        
    newfile = path_to_enc[:-4]
    
    cipher = AESCipher(key)
    
    with open(newfile, 'w') as new:
        new.write(cipher.decrypt(contents))

    #remove encrypted file
    os.remove(path_to_enc)
    
    click.echo('Your file was decrypted.')
    

archiver.add_command(location)

if __name__ == '__main__':
    archiver()
