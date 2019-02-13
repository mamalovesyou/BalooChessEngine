# -*- coding: utf-8 -*-

"""
Pre-process the PGN files
"""
import re
import os
import json
import chess
import multiprocessing
import numpy as np

from valuator import Valuator
from node import Node


class GameParser:
    """
    Process data and convert them into numpy arrays
    All files must be PGN files
    """
    def __init__(self, data_path, destination):
        """
        Verify all paths and init processed list.
        """

        if not os.path.exists(data_path):
            raise Exception("Couldn't found data_path: %s" % data_path)

        if not os.path.exists(destination):
            raise Exception("Couldn't found destination: %s" % destination)

        self.data_path = data_path
        self.destination_path = destination

        self.processed = []

    def _to_result(self, str_result):
        """
        Return a game result from a string
        """
        if str_result == '1-0':
            return 0.
        if str_result == '0-1':
            return 1.
        return 0.5

    def _parse_games(self, data_file):
        """
        Process PGN file. Avoid all game winned by disconnection"
        """
        disconnection = "by disconnection"
        with open(data_file, 'r') as data:
            print("Parsing %s" % data_file)
            for line in data:
                if line[:2] == "1." or disconnection in line:
                    end_idx = line.index('{')
                    result_idx = line.index('}') + 1
                    game_line = line[:end_idx]
                    # clean line
                    # game_line = game_line.replace('#', '').replace('+', '')
                    game_line = re.sub(r'[1-9][0-9]*\.\s', '', game_line)
                    result_str = line[result_idx:].replace(' ',
                            '').replace('\n', '')
                    game_result = self._to_result(result_str)
                    parsed_game = game_line.strip().split(' ')
                    if parsed_game[-1] == '':
                        del parsed_game[-1]

                    self.processed.append({'game': parsed_game,
                        'result': game_result})

    def _save_processed_games(self, destination):
        """
        Save processed games into json file.
        """
        with open(destination, 'w') as output:
            json.dump(self.processed, output)
            print("Saved %d processed games." % len(self.processed))
            self.processed = []


    def run(self):
        """
        Parse all game for all pgn files in data_path
        """
        if os.path.isfile(self.data_path) and self.data_path.endswith('.pgn'):
            output_file = self.destination_path.replace('pgn', 'json')
            self._parse_games(self.data_path)
            self._save_processed_games(output_file)
        else:
            for f in os.listdir(self.data_path):
                path = os.path.join(self.data_path, f)
                if os.path.isfile(path) and f.endswith('pgn'):
                    output_file = os.path.join(self.destination_path,
                            f.replace('pgn', 'json'))

                    self._parse_games(path)
                    self._save_processed_games(output_file)

class DataSetBuilder:
    """
    Build data set from parsed game
    """

    # Available features types to extract
    RESULT = "result"
    MATERIAL = "material"
    PIECE_SQUARE = "square"
    LEGAL_MOVES = "moves"

    def __init__(self, data_path, destination_path):
        if not os.path.exists(data_path):
            raise Exception("data path %s does not exist." % data_path)

        self.datapath = data_path
        self.destination_path = destination_path
        self.valuator = Valuator()

    def _result_to_label(self, result):
        if result == 1:
            return np.array([1, 0, 0])
        elif result == 0:
            return np.array([0, 0, 1])
        return np.array([0-1-0])

    def _moves_to_label(self, node):
        val = self.valuator.get_number_of_legal_moves_value(node.board)
        if val < 0:
            return np.array([0, 0, 1])
        if val > 0:
            return np.array([1, 0, 0])
        return np.array([0, 1, 0])

    def _material_to_label(self, node):
        val = self.valuator.get_material_value(node.board)
        if val < 0:
            return np.array([0, 0, 1])
        if val > 0:
            return np.array([1, 0, 0])
        return np.array([0, 1, 0])

    def _square_to_label(self, node):
        val = self.valuator.get_all_masks_value(node.board, node.board.turn)
        if val < 0:
            return np.array([0, 0, 1])
        if val > 0:
            return np.array([1, 0, 0])
        return np.array([0, 1, 0])


    def _extract_label(self, node, result, feature_type):
        """
        Extract the label for a specific feature
        node: nnode with a board
        result: result of the game 1, 0 or 0.5
        feature_type: Look at available features types

        return: [1-0-0] or [0-0-1] or [0-1-0] if white wins, black wins or
        even
        """
        if feature_type == self.RESULT:
            return self._result_to_label(result)

        if feature_type == self.MATERIAL:
            return self._material_to_label(node)

        if feature_type == self.LEGAL_MOVES:
            return self._moves_to_label(node)

        if feature_type == self.PIECE_SQUARE:
            return self._square_to_label(node)


    def _node_to_feature(self, node):
        """
        Serialize a node into a numpy array
        return: 1*64 numpy array
        """
        feature = np.zeros(64)
        pieces = node.board.piece_map()
        for idx in pieces:
            p = pieces[idx]
            feature[idx] = self.valuator.piece_to_value(p.piece_type, p.color)
        return feature

    def _game_to_dataset(self, process_id, data, feature_type, features,
            labels):
        """
        Transform a game to a dataset
        process_id: process id
        game: array of moves
        result: result of the game

        return features, labels
        """
        print("Starting extrating %s features with process %d" % (feature_type,
            process_id))

        node = Node()
        board = node.board
        tfeatures = []
        tlabels = []
        count = 0
        for game in data:
            if count % 500 == 0:
                print("Process %d completed %d/%d game" % (process_id, count,
                    len(data)))

            moves = game['game']
            result = game['result']
            board.reset()

            for m in moves:
                board.push_san(m)
                tfeatures.append(self._node_to_feature(node))
                tlabels.append(self._extract_label(node, result, feature_type))

            count += 1

        features.append(tfeatures)
        labels.append(tlabels)

    def _chunk(self, l, n):
        """
        Split a list into evenly sized chunk
        l: list to split
        n: chunk_size
        return: list of slice
        """
        slices = [l[i:i+n] for i in range(0, len(l), n)]
        return slices

    def _dispatch_job(self, feature_type, data, process_number):
        """
        Dispatch a job on a list of data
        feature_type: type of feature to extract
        data: list
        process_number: number of jobs

        return: list of jobs result
        """
        chunk_size = len(data)//process_number
        slices = self._chunk(data, chunk_size)
        features = []
        labels = []
        jobs = []
        for i, chunk in enumerate(slices):
            process = multiprocessing.Process(target=self._game_to_dataset,
                    args=(i, chunk, feature_type, features, labels))
            jobs.append(process)

        for j in jobs:
            j.start()

        # flatten list
        all_features = np.array(features).flatten()
        all_labels = np.array(labels).flatten()

        features_path = os.path.join(self.destination_path,
                "feature-{}".format(feature_type))
        np.save(features_path, all_features)

        labels_path = os.path.join(self.destination_path,
                "labels-{}".format(feature_type))
        np.save(labels_path, all_labels)




    def build(self, workers=1):
        features_type = [self.MATERIAL]
        print("Building dataset from {}".format(self.datapath))
        print("Using %d workers" % workers)
        with open(self.datapath, 'r') as f:
            data = json.load(f)
            for ftype in features_type:
                print("Proceeding feature type: {}".format(ftype))
                self._dispatch_job(features_type, data, workers)



if __name__ == "__main__":
    # processor = GameParser('data', 'data')
    # processor.run()
    workers = int(os.getenv('WORKERS', default=1))
    builder = DataSetBuilder('data/ficsgames_2018.json', 'data/raw')
    builder.build(workers)

