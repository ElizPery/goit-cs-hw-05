import argparse
import asyncio
import aioshutil
from aiopath import AsyncPath
import logging

# List of possible extensions
FOLDERS = []

async def read_folder(source_path: AsyncPath):
    # Function takes path to the source directory and copy/sort files to destination directory

    for path in source_path.iterdir():

        # If it is dir make recursion
        if await path.is_dir():
            await read_folder(path)
        
        # If it is file call function to copy it to destination directory
        if await path.is_file():
            await copy_file(path)


async def copy_file(source: AsyncPath):
    # Function takes path to the source directory and copy files to destination directory by extensions

    destination = path_dest_dir

    suffix_of_file = source.suffix

    destination = AsyncPath(destination + f"/{suffix_of_file}")

    # Check if suffix in the list, if it is not, append it to the list and create dir
    if(suffix_of_file not in FOLDERS):
        FOLDERS.append(suffix_of_file)
        await destination.mkdir(parents=True, exist_ok=True)

    # Copy file
    await aioshutil.copyfile(source, destination)

    # Print info about copying file
    logger.info(f'Copied from {source.name} to {destination.name} directory')
    

if __name__ == '__main__':
    try:
        logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

        args = argparse.ArgumentParser()
        args.add_argument("source_dir")
        args.add_argument("destination_dir")

        path_source_dir = AsyncPath(args.get("source_dir"))
        path_dest_dir = AsyncPath('dist')

        # Check if there was entered destinatio directory
        try:
            path_dest_dir = AsyncPath(args.get("destination_dir"))
        except:
            print("Files would be sorted in 'dist' directory")

        # Check if the path is dir
        if(path_source_dir.is_file()):
            raise ValueError

        # Print name of search dir
        print(f'Copied and sorted from {path_source_dir.name} to {path_dest_dir.name} directory')

        asyncio.run(read_folder(path_source_dir))

    except:
        print('Something went wrong. Please check path!')