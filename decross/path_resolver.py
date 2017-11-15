import os
from pathlib import Path

from settings import Settings

class PathResolver:
    base_path = Path(os.path.dirname(os.path.realpath(__file__))).parent

    # output folder structure
    DATASETS_FOLDER = 'datasets'
    MAPPINGS_FOLDER = 'coverage'
    BLAST_DB_FOLDER = os.path.join(DATASETS_FOLDER, 'blast_db')
    BLAST_RESULTS_FOLDER = 'blast_results'
    ALL_VS_ALL_FOLDER = os.path.join(BLAST_RESULTS_FOLDER, 'all_vs_all')
    ONE_VS_ALL_FOLDER = os.path.join(BLAST_RESULTS_FOLDER, 'one_vs_all')
    HITSOGRAMS_FOLDER = 'histograms'
    TYPES_FILENAME = 'types.csv'
    RESULTS_FOLDER = 'results'

    @staticmethod
    def abs_path_for(path):
        return os.path.join(str(PathResolver.base_path), str(Path(path)))

    @staticmethod
    def input_path_for(path):
        return os.path.join(Settings.decross.paths.input, path)

    @staticmethod
    def output_path_for(path, *extra_paths):
        return os.path.join(Settings.decross.paths.output, path, *extra_paths)

    @staticmethod
    def datasets_output_path(file=None):
        folder = PathResolver.output_path_for(PathResolver.DATASETS_FOLDER)

        if file:
            return os.path.join(folder, file)
        else:
            return folder

    @staticmethod
    def mappings_output_path(file=None):
        folder = PathResolver.output_path_for(PathResolver.MAPPINGS_FOLDER)

        if file:
            return os.path.join(folder, file)
        else:
            return folder

    @staticmethod
    def pair_types_path():
        return PathResolver.output_path_for(PathResolver.TYPES_FILENAME)


    @staticmethod
    def results_path_for(*paths):
        return PathResolver.output_path_for(PathResolver.RESULTS_FOLDER, *paths)

    @staticmethod
    def assure_path_exists(path):
        if not os.path.isdir(path):
            os.makedirs(path)






