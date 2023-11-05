# Copyright (C) 2023 Amritha Premkumar, Prajit T Rajendran, Vignesh V Menon
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Import necessary libraries
import argparse
import ladder_generation
import data

def main():
    """
    The main entry point of the program.
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Process video segment with a specified encoder.")

    # Add arguments
    parser.add_argument("--maxTime", help="Maximum acceptable time")
    parser.add_argument("--codec", help="Codec name- x264, x265, av1, vvenc")
    parser.add_argument("--ladreCsv", help="Output csv with optimized bitrate ladder")

    # Parse the arguments
    args = parser.parse_args()

    # Access the parsed arguments
    max_time = float(args.maxTime)
    codec = args.codec
    ladre_csv = args.ladreCsv
    bitrates = [145, 300,600, 900, 1600, 2400, 3400, 4500, 5800, 8100, 11600, 16800]
    dataset_path = "dataset/Sequences.csv"
    resolutions_list = [360, 720, 1080, 2160]

    l_gen = ladder_generation.LadderGenerator(max_time, codec, ladre_csv, bitrates, dataset_path, resolutions_list)
    l_gen.load_models()
    l_gen.generate_ladder()

# Execute the main function
if __name__ == "__main__":
    main()
