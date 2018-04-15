import click
import os
import io
import sys
from datetime import datetime
from archiver.encipher import AESCipher
from archiver.archivist import Archivist
        

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
