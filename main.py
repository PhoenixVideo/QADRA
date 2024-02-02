# Copyright (C) 2024 Amritha Premkumar, Prajit T Rajendran, Vignesh V Menon
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


def main():
    """
    The main entry point of the program.
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Process video segment with a specified encoder.")

    # Add arguments
    parser.add_argument("--maxTime", help="Maximum acceptable time")
    parser.add_argument("--codec", help="Encoder name- vvenc")
    parser.add_argument("--ladreCsv", help="Output csv with optimized bitrate ladder")
    parser.add_argument("--rmax", help="Maximum supported resolution")
    parser.add_argument("--maxQuality", help="Maximum Quality (vvenc:XPSNR)")
    parser.add_argument("--jnd", help="JND in terms of XPSNR")

    # Parse the arguments
    args = parser.parse_args()

    # Access the parsed arguments
    max_time = float(args.maxTime)
    codec = args.codec
    r_max = args.rmax
    ladre_csv = args.ladreCsv
    max_quality = args.maxQuality
    jnd = args.jnd
    bitrates = [145, 300, 600, 900, 1600, 2400, 3400, 4500, 5800, 8100, 11600, 16800]
    dataset_path = "dataset/Sequences.csv"
    resolutions_list = [360, 540, 720, 1080, 1440, 2160]
    resolutions = []
    for resolution in resolutions_list:
        resolutions.append(resolution)
        if resolution == r_max:
            break
    l_gen = ladder_generation.LadderGenerator(max_time, codec, ladre_csv, bitrates, dataset_path, resolutions, r_max,
                                              max_quality, jnd)
    l_gen.load_models()
    l_gen.generate_ladder()


# Execute the main function
if __name__ == "__main__":
    main()
