"""
-PYTHON TASK
Please implement a program that synchronizes two folders: source and replica.
The program shoud maintain a full, identical copy of source folder at replica folder.

- Synchronization must be one-way: after the synchronization,
content of the replica folder should be modified to exactly match content of the source folder;
- Synchronization should be performed periodically;
- File creation/copying/removal operations should be logged to a file and to the console output;
- Folder paths, synchronization interval and log file path should be provided using the command line arguments;
- It is undesirable to use third-party libraries that implement folder synchronization;
- It is allowed and recommended to use external libraries implementing other well-known algorithms.
For example there is no point in implementing yet another function that calculates MD5 if you needed for the task
 -- it is perfectly acceptable to use a third party (or built-in) library.
- The solution should be presented in the form of a link to the public Github repository
"""

import argparse
import datetime
import os
import shutil
import time
from datetime import datetime
import logging


def synchronize_folders(source, replica, interval, log_file):
    """
    Function used to call initial and periodic synchronization
    """
    log(log_file, "STARTING THE PROGRAM")

    # Check if replica exists
    if not os.path.exists(replica):
        os.makedirs(replica)
        log(log_file, f"Created initial replica directory: {replica}")

    # Initial synchronization
    synchronize(source, replica, log_file)

    # Interval synchronization
    while True:
        synchronize(source, replica, log_file)
        time.sleep(interval)


def synchronize(source, replica, log_file):
    """
    Function used to perform synchronization
    """
    # Get directories and file from both folders
    source_components = set(os.listdir(source))
    if not os.path.exists(replica):
        os.makedirs(replica)
        log(
            log_file,
            f"While program was on, replica was deleted and created again: {replica}"
        )
    replica_components = set(os.listdir(replica))

    # Determine components to copy to replica or to remove from replica
    components_to_copy = source_components - replica_components
    components_to_delete = replica_components - source_components

    # Print the following to terminal only(left out from log file):
    # folder's components, to be copied and to be deleted
    logging.info("Source's components: %s", source_components)
    logging.info("Replica's components: %s", replica_components)
    logging.info("Components to be COPIED: %s", components_to_copy)
    logging.info("Components to be DELETED: %s", components_to_delete)
    logging.info("************************************************")

    # Synchronize directories
    for component in source_components:
        source_path = os.path.join(source, component)
        replica_path = os.path.join(replica, component)
        if os.path.isdir(source_path):
            # Check subfolder exists in replica
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)
                log(
                    log_file,
                    f"Created SOURCE DIR:{source_path}, COPIED TO REPLICA:{replica_path}"
                )
            synchronize(source_path, replica_path, log_file)
        elif os.path.isfile(source_path):
            if component not in replica_components:
                # os.symlink(source_path, replica_path)
                shutil.copy2(source_path, replica_path)
                log(
                    log_file,
                    f"Created SOURCE FILE:{source_path}, LINKED/COPIED TO REPLICA:{replica_path}"
                )

    # Delete folders and files inexistent in Source
    for component in components_to_delete:
        path_to_delete = os.path.join(replica, component)
        # if os.path.isfile(path_to_delete):
        if os.path.isfile(path_to_delete) or os.path.islink(path_to_delete):
            if component not in source_components:
                os.remove(path_to_delete)
                log(
                    log_file,
                    f"FILE NOT FOUND IN SOURCE: {component}, DELETED file from REPLICA: {path_to_delete}"
                )
        elif os.path.isdir(path_to_delete):
            shutil.rmtree(path_to_delete)
            log(
                log_file,
                f"DIRECTORY NOT FOUND IN SOURCE: {component}, DELETED directory from REPLICA: {path_to_delete}"
            )


def log(log_file, message):
    """Logs the synchronization process"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"\n[{timestamp}] : {message}"
    logging.info(log_message)
    with open(log_file, "a") as logger:
        logger.write(log_message + "\n")
        logger.write("************************************************\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Folder Synchronization")
    parser.add_argument("source", help="Source folder's path")
    parser.add_argument("replica", help="Replica folder's path")
    parser.add_argument("interval",
                        type=int,
                        help="Synchronization interval time in seconds")
    parser.add_argument("log_file", help="Log file's path")
    args = parser.parse_args()

    synchronize_folders(args.source, args.replica, args.interval,
                        args.log_file)
