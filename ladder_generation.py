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

# Importing necessary libraries
import pandas as pd
import numpy as np
import pickle
import sys
import os
import warnings

# Disable all warnings
warnings.filterwarnings("ignore")

# Creating a class to handle ladder generation
class LadderGenerator:
    # Constructor
    def __init__(self, max_time, codec, ladre_csv, bitrates, dataset_path, resolutions_list):
        self.models_time = None
        self.models_vmaf = None
        self.models_crf = None
        self.max_time = max_time
        self.actual_max_time = max_time-0.5
        self.codec = codec
        self.ladre_csv = ladre_csv
        self.bitrates_list = bitrates
        self.df_consolidated = pd.read_csv(dataset_path)
        self.resolutions_list = resolutions_list

    # Load corresponding prediction models
    def load_models(self):
        # Set path to model
        if self.codec == "x265":
            model_path = "./models/x265-ultrafast"
        else:
            print("Codec not supported")
            sys.exit()
        # Load models for different resolutions
        self.models_vmaf = {
            360: pickle.load(open(os.path.join(model_path, 'vmaf','Random_forest_vmaf_360p.pkl'), 'rb')),
            720: pickle.load(open(os.path.join(model_path,'vmaf','Random_forest_vmaf_720p.pkl'), 'rb')),
            1080: pickle.load(open(os.path.join(model_path,'vmaf','Random_forest_vmaf_1080p.pkl'), 'rb')),
            2160: pickle.load(open(os.path.join(model_path,'vmaf','Random_forest_vmaf_2160p.pkl'), 'rb')),
        }
        self.models_crf = {
            360: pickle.load(open(os.path.join(model_path,'crf','Random_forest_crf_360p.pkl'), 'rb')),
            720: pickle.load(open(os.path.join(model_path,'crf','Random_forest_crf_720p.pkl'), 'rb')),
            1080:pickle.load(open(os.path.join(model_path,'crf','Random_forest_crf_1080p.pkl'), 'rb')),
            2160: pickle.load(open(os.path.join(model_path,'crf','Random_forest_crf_2160p.pkl'), 'rb')),
        }

        self.models_time = {
            360: pickle.load(open(os.path.join(model_path,'time','Random_forest_time_360p.pkl'), 'rb')),
            720: pickle.load(open(os.path.join(model_path,'time','Random_forest_time_720p.pkl'), 'rb')),
            1080: pickle.load(open(os.path.join(model_path,'time','Random_forest_time_1080p.pkl'), 'rb')),
            2160: pickle.load(open(os.path.join(model_path,'time','Random_forest_time_2160p.pkl'), 'rb')),
        }

    # Get the predicted resolution and crf as a list based on the features and the predicted time
    def get_resolution_and_crf(
        self,
        vmaf_features,
        crf_or_time_features_list,
        bitrate,
        time,
        previous_resolution,
    ):
        log_bitrate = np.log(bitrate)
        resolution_predicted_features_list = self.select_best_resolution(
            vmaf_features, crf_or_time_features_list, log_bitrate, time, previous_resolution,bitrate
        )

        crf = self.predict_crf(crf_or_time_features_list, resolution_predicted_features_list[0], log_bitrate)
        result_list = [resolution_predicted_features_list[0], crf, resolution_predicted_features_list[1],resolution_predicted_features_list[2]]
        return result_list

    # Get the best resolution based the predicted and target time
    def select_best_resolution(
        self, vmaf_features, crf_or_time_features_list, log_bitrate, tl, previous_resolution,bitrate
    ):
        result_list = []
        predicted_resolution = self.resolutions_list[0]
        vmaf = []
        time = []
        for resolution in self.resolutions_list:
            vmaf.append(self.predict_vmaf(vmaf_features, resolution, log_bitrate))
            time.append(
                self.predict_time(crf_or_time_features_list, resolution, log_bitrate)
            )

        highest_vmaf = -1

        for i in range(len(vmaf)):
            if time[i] < tl:
                if vmaf[i] > highest_vmaf:
                    highest_vmaf = vmaf[i]
        if highest_vmaf != -1:
            index = vmaf.index(highest_vmaf)
            predicted_resolution = self.resolutions_list[index]

        resolution = self.get_resolution_based_on_bitrate(predicted_resolution,previous_resolution, bitrate)
        index = self.resolutions_list.index(resolution)
        predicted_vmaf = vmaf[index]
        predicted_time = time[index]
        result_list.extend([resolution,predicted_vmaf,predicted_time])
        return result_list

    def get_resolution_based_on_bitrate(self, predicted_resolution,previous_resolution, bitrate):
        if bitrate < 1000:
            if predicted_resolution == 2160:
                return previous_resolution
            else:
                if predicted_resolution > previous_resolution:
                    return predicted_resolution
                else:
                    return previous_resolution
        else:
            return predicted_resolution

    def predict_time(self, features, resolution, bitrate):
        vector = []
        vector.extend(features)
        vector.append(bitrate)
        test_vector = [vector]
        model = self.models_time[resolution]
        predictions = model.predict(test_vector)
        return predictions[0]

    def predict_vmaf(self, features, resolution, bitrate):
        vector = []
        vector.extend(features)
        vector.append(bitrate)
        test_vector = [vector]
        model = self.models_vmaf[resolution]
        predictions = model.predict(test_vector)
        return predictions[0]

    def predict_crf(self, features, resolution, bitrate):
        vector = []
        vector.extend(features)
        vector.append(bitrate)
        test_vector = [vector]
        model = self.models_crf[resolution]
        predictions = model.predict(test_vector)
        return int(predictions)

    def generate_ladder(self):
        new_features_list = []
        condition1 = self.df_consolidated['Train'] == 0
        df_test = self.df_consolidated[condition1]
        video_names = df_test["VideoName"].unique().tolist()
        for video_name in video_names:
            filter_condition = df_test["VideoName"] == video_name
            filtered_df = df_test[filter_condition]
            vmaf_features_list = filtered_df[["AvgE", "Avgh", "AvgL"]].values.tolist()
            crf_or_time_features_list = filtered_df[
                ["AvgE", "Avgh", "AvgL", "avgU", "energyU", "avgV", "energyV"]
            ].values.tolist()
            previous_resolution = 360
            for bitrate in self.bitrates_list:
                final_parameters = []
                resolution_crf_vmaf_time_list = self.get_resolution_and_crf(
                    vmaf_features_list[0],
                    crf_or_time_features_list[0],
                    bitrate,
                    self.actual_max_time,
                    previous_resolution,
                )
                previous_resolution = resolution_crf_vmaf_time_list[0]
                predicted_resolution = resolution_crf_vmaf_time_list[0]
                predicted_crf = resolution_crf_vmaf_time_list[1]
                final_parameters.append(video_name)
                final_parameters.extend(crf_or_time_features_list[0])
                final_parameters.append(bitrate)
                final_parameters.append(self.max_time)
                final_parameters.append(predicted_resolution)
                final_parameters.append(predicted_crf)
                new_features_list.append(final_parameters)

        final_csv_df = pd.DataFrame(
            new_features_list,
            columns=[
                "VideoName",
                "E_Y",
                "h",
                "L_Y",
                "L_U",
                "E_U",
                "L_V",
                "E_V",
                "targetBitrate",
                "timeLimit",
                "resolution",
                "crf"
            ],

        )

        # Write the DataFrame to a CSV file
        final_csv_df.to_csv(self.ladre_csv, index=False)
