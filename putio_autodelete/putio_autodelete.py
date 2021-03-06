import argparse
import configparser
import datetime
import json
import time
import putiopy


def auto_delete(
    oauth_token: str, max_age: "num", dryrun: bool, excluded_dirs: list = []
):
    """Deletes files older than `max_age` days from the putio account associated with
    the `oauth_token`. The folders (NOT their contents) in `excluded_dirs` will be
    left even if they match the age criteria.
    Returns True if files have been found/deleted matching the age criteria.
    False if no files were found.
    """

    client = putiopy.Client(oauth_token)

    max_age_delta = datetime.timedelta(days=max_age)
    cutoff_date = datetime.datetime.today() - max_age_delta

    files = client.File.list(
        parent_id=-1, file_type="FILE,AUDIO,VIDEO,IMAGE,ARCHIVE,PDF,TEXT,SWF"
    )
    old_files = [file_ for file_ in files if file_.created_at < cutoff_date]

    for file_ in old_files:
        if dryrun:
            print("      Old file Found: {}".format(file_.name))
        else:
            try:
                file_.delete(True)
            except:
                print("[x] Could not delete: {}".format(file_.name))
            else:
                print("        File Deleted: {}".format(file_.name))
            time.sleep(0.2)

    folders = client.File.list(parent_id=-1, file_type="FOLDER")
    old_folders = [
        folder
        for folder in folders
        if folder.created_at < cutoff_date
        and folder.size == 0
        and folder.name not in excluded_dirs
    ]

    for folder in old_folders:
        if dryrun:
            print("    Old folder Found: {}".format(folder.name))
        else:
            try:
                folder.delete(True)
            except:
                print("[x] Could not delete: {}".format(folder.name))
            else:
                print("      Folder Deleted: {}".format(folder.name))
            time.sleep(0.2)

    if old_files or old_folders:
        return True
    else:
        return False


def parse_args():
    parser = argparse.ArgumentParser(
        prog="putio_autodelete",
        description="""
            The script automatically deletes all files & dirs older than X days
            from your Put.io account. Folders with the names in EXCLUDED_DIRS
            in the config file will not be deleted, but their contents
            will be (if they match the age criteria).
            The OAUTH Token must be present, either as a direct argument or in
            the config file.
        """,
    )

    parser.add_argument(
        "-o",
        "--oauth_token",
        help="""String representing your OAUTH token, resembling:
            WARNING: This arg will take priority over the config file.
            XXXXXXXXXXXXXXXXXXXXX
            """,
        type=str,
    )

    parser.add_argument(
        "-m",
        "--max_age",
        help="""Maximum age in days for files/folders to keep.
            WARNING: Config file settings take priority.
            Default=7.0""",
        type=float,
        default=7.0,
    )

    parser.add_argument(
        "-c",
        "--config",
        help="""Config file containing running parameters.
            This can be used instead of any other args.
            i.e "config.ini" or "/home/config.ini"
            See README for details.
            """,
        type=str,
    )

    parser.add_argument(
        "-d",
        "--dryrun",
        help="Shows files to delete but does not delete anything.",
        action="store_true",
    )

    return parser.parse_args()


def parse_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    cfg = config["DEFAULTS"]

    oa_token = str(cfg["OAUTH_TOKEN"]) if "OAUTH_TOKEN" in cfg else None
    max_age = float(cfg["MAX_AGE"]) if "MAX_AGE" in cfg else None
    exc_dirs = (
        list(json.loads(cfg["EXCLUDED_DIRS"])) if "EXCLUDED_DIRS" in cfg else None
    )

    return oa_token, max_age, exc_dirs


def main():
    args = parse_args()

    if args.config:
        try:
            oa_token_cfg, max_age_cfg, exc_dirs_cfg = parse_config(args.config)
        except (json.decoder.JSONDecodeError, ValueError) as exc:
            raise Exception("Config file does not meet format requirements.")
    else:
        oa_token_cfg, max_age_cfg, exc_dirs_cfg = None, None, None

    try:
        oa_token = args.oauth_token or oa_token_cfg
    except NameError:
        raise Exception("oath token must be provided. See --help or README.")
    else:
        max_age = max_age_cfg or args.max_age
        exc_dirs = exc_dirs_cfg or []

        print("Started!")
        if args.dryrun:
            print("Dryrun...")
        print("Maximum age: {:.1f} days".format(max_age))
        if not auto_delete(oa_token, max_age, args.dryrun, exc_dirs):
            print("No files found")
        print("Done!")


if __name__ == "__main__":
    main()
