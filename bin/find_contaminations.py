#!/usr/bin/python2.7
import sys, os, time, logging, glob
from pathlib import Path
from multiprocessing import Pool
from optparse import OptionParser

ROOT_PATH = str(Path(os.path.dirname(os.path.realpath(__file__))).parent)
sys.path.append(ROOT_PATH)

from decross.settings import Settings
from decross.path_resolver import PathResolver
from decross.name_converter import NameConverter
from decross.types_manager import TypesManager
from decross.contaminations_finder import ContaminationsFinder

SETTINGS_PATH = 'config/settings.yml'

parser = OptionParser(description="Main contamination finder script")
parser.add_option("--config_path", help="Alternative config path")
(options, args) = parser.parse_args()

def analyze_blastab(path):
    ContaminationsFinder(path).process()

def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    global logger
    logger = logging.getLogger()

    Settings.load(options.config_path or PathResolver.abs_path_for(SETTINGS_PATH))

    PathResolver.assure_path_exists(PathResolver.results_path_for())
    os.system('rm %s/*' % PathResolver.results_path_for())

    NameConverter.load()
    TypesManager.load()

    one_vs_all_path = PathResolver.output_path_for(PathResolver.ONE_VS_ALL_FOLDER)
    paths = [fname for fname in glob.glob(one_vs_all_path + '/*.blastab')]
    paths.sort()

    files_count = len(paths)

    avg_time = None
    start_time = time.time()

    if Settings.decross.threads.multithreading:
        threads_count = Settings.decross.threads.count
        logger.info("Starting with %s threads\n" % (threads_count))
        pool = Pool(threads_count)

        for _ in tqdm(pool.imap(analyze_blastab, paths), total=len(paths)):
          pass
    else:
        for i, file_path in enumerate(paths):
            info = (file_path.split('/')[-1], i+1, files_count)
            logger.info('---> Working with file %s (%s/%s)' % info)

            local_start_time = time.time()
            analyze_blastab(file_path)
            local_end_time = time.time()

            seconds = int(local_end_time-local_start_time)

            if not avg_time:
                avg_time = seconds
            else:
                avg_time = (avg_time + seconds)/2

            hours_to_go = ((files_count-(i+1))*avg_time)/3600

            logger.info('<--- finished in %i seconds\n\n' % int(local_end_time-local_start_time))
            logger.info('(about %s hours remaining)' % hours_to_go)
            logger.info('')

if __name__ == '__main__':
    main()
