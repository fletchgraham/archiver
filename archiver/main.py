import click
import os
import io
import sqlite3
import sys

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

    def get_location(self):
        return self.location

    def set_location(self, new_location):
        pass
        # change the contents of config file to new location
        # update self.location variable

    def write(self, entry):
        pass
        # cut up the entry into a nice list or dictionary
        # connect to db
        # create the main table if it doesn't exist
        # write the record to the table
        # close db connection
        # echo that it was written to the archive

    def read(self, date):
        pass
        # connect to db
        # search db by date
        # close the db
        # echo the result in a pretty way
        
        


@click.group()
def archiver():
    pass


@archiver.command()
def write():
    # spin up the archivist object
    archivist = Archivist()
    # collect the entry from the user
    entry = input('Create your entry >>> ')
    # run the write method of the archivist with the entry
    archivist.write(entry)
    click.echo('Your entry was written to the archive.')


@archiver.command()
def read():
    # spin up the archivist object
    archivist = Archivist()
    # get a date from the user
    date = input('Date >>> ')
    # call the read method of the archivist on the date
    archivist.read(date)
    click.echo('Your entry: ')

@archiver.command()
def location():
    archivist = Archivist()
    click.echo(archivist.get_location())

archiver.add_command(location)

if __name__ == '__main__':
    archiver()
