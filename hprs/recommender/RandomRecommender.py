# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

import requests as rq
import json
import random

from hprs.common.Constants import Constants


class RandomRecommender(object):
    def __init__(self):
        self.rest_root_url = f"http://{Constants.MRMS_SVC}:{Constants.MRMS_REST_PORT}"
        self.image_conv_fn_set = ["Conv2D"]
        self.image_pooling_fn_set = ["Max2D", "Average2D"]

    def get_algorithm_params(self, algorithm_id):
        response = rq.get(f"{self.rest_root_url}/mrms/get_param_info?alg_id={algorithm_id}")
        str_data = response.text
        data = json.loads(str_data)
        response.close()
        return data

    def get_uuid(self):
        response = rq.get(f"{self.rest_root_url}/mrms/get_uuid")
        return response.text.replace("\n", "")

    def recommend(self, mars_list, job_id):
        result = list()

        for idx, mars_data in enumerate(mars_list):
            params_list = self.get_algorithm_params(mars_data.get("alg_id"))
            for i in range(random.randint(Constants.RCMD_MIN_COUNT, Constants.RCMD_MAX_COUNT)):
                res = dict()
                param_dict = dict()
                fixed_size = 0
                for param in params_list:
                    param_nm = param.get("param_code")
                    if param.get("param_type") == "1" and param.get("param_type_value") == "list":
                        if param_nm == "filter_sizes" or param_nm == "pool_sizes":
                            fixed_size = random.randint(1, 3) if fixed_size == 0 else fixed_size
                            param_dict[param_nm] = ",".join([str(random.randint(2, 8)) for i in range(random.randint(fixed_size, fixed_size))])
                        else:
                            param_dict[param_nm] = ",".join([str(random.randint(3, 1024)) for i in range(random.randint(1, 3))])
                    elif param.get("param_type") == "1":
                        if param_nm == "n_neighbors":
                            param_dict[param_nm] = random.randint(2, 3)
                        else:
                            param_dict[param_nm] = random.randint(1, 16)
                    elif param.get("param_type") == "2":
                        if param_nm == "dropout_prob":
                            param_dict[param_nm] = random.uniform(0, 0.5)
                        elif param_nm == "learning_rate":
                            param_dict[param_nm] = random.uniform(0, 0.8)
                        else:
                            param_dict[param_nm] = random.random()
                    elif param.get("param_type") == "3":
                        if int(mars_data.get("dataset_format")) == 2:  # case image dataset
                            if param_nm == "conv_fn":
                                param_dict[param_nm] = random.choice(self.image_conv_fn_set)
                            elif param_nm == "pooling_fn":
                                param_dict[param_nm] = random.choice(self.image_pooling_fn_set)
                            else:
                                param_dict[param_nm] = random.choice(param.get("param_type_value").split(","))
                        else:
                            param_dict[param_nm] = random.choice(param.get("param_type_value").split(","))

                res["project_id"] = job_id
                res["alg_anal_id"] = mars_data.get("alg_anal_id")
                res["dp_analysis_id"] = mars_data.get("dp_analysis_id")
                res["param_id"] = self.get_uuid()
                res["alg_id"] = mars_data.get("alg_id")
                res["param_json"] = param_dict
                result.append(res)
        return result


if __name__ == '__main__':
    RandomRecommender()
