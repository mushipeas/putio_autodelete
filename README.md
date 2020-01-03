# `Putio Auto-Delete`

The script automatically deletes all files older than X days from your Put.io account.

Directory exclusion is possible, which prevents certain directories (but not their contents!) from
being deleted.

The dryrun function will show files that meet the deletion criteria, but will not perform any actions.

Requires OAUTH key to be used as an argument or placed in an optional config file.

Written for and tested on Python 3.7.5

## To Initialise the Project

### Recommended:
In the root dir of project, run:

    python -m venv .venv
This should create a virtual environment

### Activate the environment:
    .\.venv\Scripts\activate (Windows)
    source .venv/bin/activate (UNIX)

### Install required packages:
    pip install -r requirements.txt

### Install development packages (dev only):
    pip install -r requirements.dev.txt

## Useage

### Running the script:
    usage: putio_autodelete.py [-h] [-o OAUTH_TOKEN] [-m MAX_AGE] [-c CONFIG]
                               [-d DRYRUN]

    The script automatically deletes all files & dirs older than X days from your
    Put.io account. Folders with the names in the excluded-directories argument
    will not be deleted, but their contents will be (if they match the age
    criteria). The OAUTH Token must be present, either as a direct argument or in
    the config file.

    optional arguments:
    -h, --help            show this help message and exit
    -o OAUTH_TOKEN, --oauth_token OAUTH_TOKEN
                            String representing your OAUTH token, resembling:
                            WARNING: This arg will take priority over the config
                            file. XXXXXXXXXXXXXXXXXXXXX
    -m MAX_AGE, --max_age MAX_AGE
                            Maximum age in days for files/folders to keep.
                            WARNING: Config file settings take priority.
                            Default=7.0
    -c CONFIG, --config CONFIG
                            Config file containing running parameters. This can be
                            used instead of any other args. i.e "config.ini" or
                            "/home/config.ini" See README for details.
    -d DRYRUN, --dryrun DRYRUN
                            Shows files to delete but does not delete anything.

### Config.ini:
The program can be run with a config file, as:

    > py putio_autodelete.py -c config.ini

The config file should contain the OAUTH Token as a minimum (though this can be separately input in the command line).
The real benefit is being able to include `EXCLUDED_DIRS` which are folders that will not be deleted.
This is useful for preventing folders linked to RSS Feeds / Automation from getting deleted by the script.

Sample `config.ini`:

    [DEFAULTS]
    OAUTH_TOKEN = XXXXXXXXXXXXXXXXXXXX
    MAX_AGE = 7.0
    EXCLUDED_DIRS = [ "Sample_FolderA", "Sample_FolderB", "Sample Folder C" ]

### Automation:

It is recommended that you set up a `config.ini` file and use `putio_autodelete.py -c config.ini` to run the script
in any automation, especially if directory exclusions are important to you.
Directory exclusions cannot be set up without the config file.
