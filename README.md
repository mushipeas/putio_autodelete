# `Putio Auto-Delete`

The script automatically deletes all files older than X days from your Put.io account.

Directory exclusion is possible, which prevents certain directories (but not their contents!) from
being deleted.

The dryrun function will show files that meet the deletion criteria, but will not perform any actions.

Requires OAUTH key to be used as an argument or placed in an optional config file.

Written for and tested on Python 3.7.5

## To Initialise the Project

### Recommended:
In the root dir of project (where `setup.py` resides), run:

    pip install .

This will install the script into your system.

Optionally, to test out, you can install `after` creating and activating an environment:

    python -m venv .venv

### Activate the environment:
    .\.venv\Scripts\activate (Windows)
    source .venv/bin/activate (UNIX)

### Install required packages:
    pip install .

### Alternative install for development (dev only):
    pip install -e .

## Useage

### Running the script:
    usage: putio_autodelete [-h] [-o OAUTH_TOKEN] [-m MAX_AGE] [-c CONFIG] [-d]

        The script automatically deletes all files & dirs older than X days from your
        Put.io account. Folders with the names in EXCLUDED_DIRS in the config file
        will not be deleted, but their contents will be (if they match the age
        criteria). The OAUTH Token must be present, either as a direct argument or in
        the config file.

        optional arguments:
        -h, --help              show this help message and exit
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
        -d, --dryrun            Shows files to delete but does not delete anything.

### Config.ini:
The program can be run with a config file, as:

    putio_autodelete -c config.ini

The config file should contain the OAUTH Token as a minimum (though this can be separately input in the command line).
The real benefit is being able to include `EXCLUDED_DIRS` which are folders that will not be deleted.
This is useful for preventing folders linked to RSS Feeds / Automation from getting deleted by the script.

Sample `config.ini`:

    [DEFAULTS]
    OAUTH_TOKEN = XXXXXXXXXXXXXXXXXXXX
    MAX_AGE = 7.0
    EXCLUDED_DIRS = [ "Sample_FolderA", "Sample_FolderB", "Sample Folder C" ]

### Automation:

It is recommended that you set up a `config.ini` file and use `putio_autodelete -c config.ini` to run the script
in any automation, especially if directory exclusions are important to you.
Directory exclusions cannot be set up without the config file.

### Docker

Build the container:

    docker build --tag putio-autodelete .

Run the script standalone:

    docker run --rm putio-autodelete [-h] [-o OAUTH_TOKEN] [-m MAX_AGE] [-d]

(or) run the script with a config file:

    docker run -v /ABSOLUTE/PATH/TO/config.ini:/app/config.ini --rm putio-autodelete -c /app/config.ini [-d]

(or) you can place the config file in the putio_autodelete subfolder before running `docker build`, and remove the need to mount the file at run-time with `-v`:

    docker run --rm putio-autodelete -c /app/config.ini [-d]

### Usage as part of another program:

Once installed, it can be imported into a project with:

    import putio_autodelete

The main function `auto_delete` can be run from the module. It is defined as follows:

    def auto_delete(oauth_token: str, max_age: "num", dryrun: bool, excluded_dirs: list=[])
       Deletes files older than max_age days from the putio account associated with the oauth_token. The folders (NOT their contents) in excluded_dirs will be left even if they match the age criteria. Returns True if files have been found/deleted matching the age criteria. False if no files were found.