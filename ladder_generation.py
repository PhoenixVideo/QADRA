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
import joblib
import math

# Disable all warnings
warnings.filterwarnings("ignore")


# Creating a class to handle ladder generation
class LadderGenerator:
    # Constructor
    def __init__(self, max_time, codec, ladre_csv, bitrates, dataset_path, resolutions_list, r_max, max_xpsnr, jnd):
        self.models_time = None
        self.models_xpsnr = None
        self.models_qp = None
        self.max_time = max_time
        self.actual_max_time = max_time - 0.5
        self.codec = codec
        self.ladre_csv = ladre_csv
        self.bitrates_list = bitrates
        self.df_consolidated = pd.read_csv(dataset_path)
        self.resolutions_list = resolutions_list
        self.max_resolution = r_max
        self.max_xpsnr = max_xpsnr
        self.jnd = jnd
        
    # Load corresponding prediction models
    def load_models(self):
        # Set path to model
        if self.codec == "vvenc":
            model_path = "./models/vvenc-faster"
        else:
            print("Codec not supported")
            sys.exit()
        # Load models for different resolutions
        self.models_xpsnr = {
            'single': joblib.load(open(os.path.join(model_path, 'xpsnr', 'xpsnr_model.pkl'), 'rb')),
        }
        self.models_qp = {
            'minimum': joblib.load(open(os.path.join(model_path, 'qp', 'qp_10_br_model.pkl'), 'rb')),
            'maximum': joblib.load(open(os.path.join(model_path, 'qp', 'qp_10_br_model.pkl'), 'rb')),
        }

        self.models_enc_time = {
            'minimum': joblib.load(open(os.path.join(model_path, 'enc_time', 'qp_10_enc_time_model.pkl'), 'rb')),
            'maximum': joblib.load(open(os.path.join(model_path, 'enc_time', 'qp_50_enc_time_model.pkl'), 'rb')),
        }

    # Get the predicted resolution and qp as a list based on the features and the predicted time
    def get_resolution_and_qp(
            self,
            xpsnr_features,
            qp_or_time_features_list,
            bitrate,
            time,
            previous_resolution,
    ):
        resolution_predicted_features_list = self.select_best_resolution(
            xpsnr_features, qp_or_time_features_list, time, previous_resolution, bitrate
        )

        qp = self.predict_qp(qp_or_time_features_list, resolution_predicted_features_list[0], bitrate)
        result_list = [resolution_predicted_features_list[0], qp, resolution_predicted_features_list[1],
                       resolution_predicted_features_list[2]]
        return result_list

    # Get the best resolution based the predicted and target time
    def select_best_resolution(
            self, xpsnr_features, qp_or_time_features_list, tl, previous_resolution, bitrate
    ):
        result_list = []
        predicted_resolution = self.resolutions_list[0]
        xpsnr = []
        time = []
        for resolution in self.resolutions_list:
            xpsnr.append(self.predict_xpsnr(xpsnr_features, resolution, bitrate))
            time.append(
                self.predict_time(qp_or_time_features_list, resolution, bitrate)
            )

        highest_xpsnr = -1

        for i in range(len(xpsnr)):
            if time[i] < tl:
                if xpsnr[i] > highest_xpsnr:
                    highest_xpsnr = xpsnr[i]
        if highest_xpsnr != -1:
            index = xpsnr.index(highest_xpsnr)
            predicted_resolution = self.resolutions_list[index]

        resolution = self.get_resolution_based_on_bitrate(predicted_resolution, previous_resolution, bitrate)
        index = self.resolutions_list.index(resolution)
        predicted_xpsnr = xpsnr[index]
        predicted_time = time[index]
        result_list.extend([resolution, predicted_xpsnr, predicted_time])
        return result_list

    @staticmethod
    def get_resolution_based_on_bitrate(predicted_resolution, previous_resolution, bitrate):
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

    def predict_enc_time(self, features, resolution, bitrate):
        vector = []
        vector.extend(features)
        vector.append(resolution/2160)
        test_vector = [vector]
        min_model = self.models_enc_time['minimum']
        max_model = self.models_enc_time['maximum']
        cur_enc_time_10 = min_model.predict(test_vector)[0]
        cur_enc_time_50 = max_model.predict(test_vector)[0]
        x1 = 10
        x2 = 50
        x = self.predict_qp(features, resolution, bitrate)
        m = (cur_enc_time_50 - cur_enc_time_10) / (x2 - x1)
        cur_enc_time = float(cur_enc_time_50 + m * (x - x2))
        return cur_enc_time

    def predict_xpsnr(self, features, resolution, bitrate):
        vector = []
        vector.extend(features)
        vector.append(resolution/2160)
        vector.append(bitrate)
        test_vector = [vector]
        model = self.models_xpsnr['single']
        predictions = model.predict(test_vector)
        return predictions[0]

    def predict_qp(self, features, resolution, bitrate):
        vector = []
        vector.extend(features)
        vector.append(resolution/2160)
        test_vector = [vector]
        min_model = self.models_qp['minimum']
        max_model = self.models_qp['maximum']
        b1 = min_model.predict(test_vector)[0]
        b2 = max_model.predict(test_vector)[0]
        x1 = 10
        x2 = 50
        y = math.log2(bitrate)
        m = (b2 - b1) / (x2 - x1)
        b = b1 - m * x1
        qp_pred = int((y - b)/m)
        if qp_pred > 50:
            qp_pred = 50
        elif qp_pred < 10:
             qp_pred = 10
        return int(qp_pred)

    def jnd_elimination(self, jnd_feature_list):
        bitrate_list_len = len(self.bitrates_list)
        representations = [jnd_feature_list[0]]
        prev_index = 0
        if jnd_feature_list[0][12] > self.max_xpsnr:
            return representations
        index = 1
        while index < bitrate_list_len:
            if (jnd_feature_list[index][12] - jnd_feature_list[prev_index][12]) >= self.jnd:
                representations.append(jnd_feature_list[index])
                prev_index = index
                if jnd_feature_list[index][12] >= self.max_xpsnr:
                    return representations
            index = index + 1
        return representations

    def generate_ladder(self):
        new_features_list = []
        condition1 = self.df_consolidated['Train'] == 0
        df_test = self.df_consolidated[condition1]
        video_names = df_test["VideoName"].unique().tolist()
        for video_name in video_names:
            jnd_feature_list = []
            filter_condition = df_test["VideoName"] == video_name
            filtered_df = df_test[filter_condition]
            xpsnr_features_list = filtered_df[["AvgE", "Avgh", "AvgL", "avgU", "avgV", "energyU", "energyV"]].values.tolist()
            qp_or_time_features_list = filtered_df[
                ["AvgE", "Avgh", "AvgL", "avgU", "avgV", "energyU", "energyV"]
            ].values.tolist()
            previous_resolution = 360
            for bitrate in self.bitrates_list:
                final_parameters = []
                resolution_qp_xpsnr_time_list = self.get_resolution_and_qp(
                    xpsnr_features_list[0],
                    qp_or_time_features_list[0],
                    bitrate,
                    self.actual_max_time,
                    previous_resolution,
                )
                previous_resolution = resolution_qp_xpsnr_time_list[0]
                predicted_resolution = resolution_qp_xpsnr_time_list[0]
                predicted_qp = resolution_qp_xpsnr_time_list[1]
                predicted_xpsnr = resolution_qp_xpsnr_time_list[2]
                final_parameters.append(video_name)
                final_parameters.extend(qp_or_time_features_list[0])
                final_parameters.append(bitrate)
                final_parameters.append(self.max_time)
                final_parameters.append(predicted_resolution)
                final_parameters.append(predicted_qp)
                final_parameters.append(predicted_xpsnr)
                jnd_feature_list.append(final_parameters)

            representations = self.jnd_elimination(jnd_feature_list)
            new_features_list.extend(representations)

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
                "qp",
                "xpsnr"
            ],

        )
        final_csv_df = final_csv_df.drop(columns=['xpsnr'])

        # Write the DataFrame to a CSV file
        final_csv_df.to_csv(self.ladre_csv, index=False)
