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
            for i in range(random.randint(3, 6)):
                res = dict()
                param_dict = dict()
                fixed_size = 0
                for param in params_list:
                    param_nm = param.get("param_code")
                    if param.get("param_type") == "1" and param.get("param_type_value") == "list":
                        if param_nm == "filter_sizes" or param_nm == "pool_sizes":
                            fixed_size = random.randint(1, 3) if fixed_size == 0 else fixed_size
                            param_dict[param_nm] = ",".join([str(random.randint(1, 64)) for i in range(random.randint(fixed_size, fixed_size))])
                        else:
                            param_dict[param_nm] = ",".join([str(random.randint(1, 64)) for i in range(random.randint(1, 3))])
                    elif param.get("param_type") == "1":
                        param_dict[param_nm] = random.randint(1, 16)
                    elif param.get("param_type") == "2":
                        param_dict[param_nm] = random.random()
                    elif param.get("param_type") == "3":
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
