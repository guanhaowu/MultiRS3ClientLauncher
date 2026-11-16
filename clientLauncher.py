"""Launch up to 36 RuneScape clients."""
import argparse
import os
import subprocess
import time


def executeClient():
    path = os.environ.get('RS3_CLIENT_PATH', r'C:\Program Files\Jagex\RuneScape Launcher\RuneScape.exe')
    subprocess.Popen([path])


def runClient(count):
    for index in range(int(count)):
        print(f'Starting client {index + 1}...')
        executeClient()
        time.sleep(0.3)


def run(count):
    count = int(count)
    if not 1 <= count <= 36:
        raise ValueError('Client count must be between 1 and 36.')
    for start in range(0, count, 5):
        runClient(min(5, count - start))
        time.sleep(5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('count', type=int)
    run(parser.parse_args().count)
