# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import http.client
import json
import random
from typing import List

from hprs.common.Constants import Constants


class RandomRecommender(object):
    def __init__(self):
        self.http_client: http.client.HTTPConnection = http.client.HTTPConnection(
            Constants.MRMS_SVC, Constants.MRMS_REST_PORT)

    def get_algorithm_params(self, algorithm_id):
        self.http_client.request("GET", "/mrms/get_param_info?alg_id={}".format(algorithm_id))
        response = self.http_client.getresponse()
        str_data = response.read()
        data = json.loads(str_data)
        response.close()
        return data

    # def get_algorithm_info(self):
    #     return {
    #         "KDNN": "20000000000000001", "KCNN": "20000000000000002"
    #     }

    def recommend(self, mars_list, job_id):
        result = list()

        for idx, mars_data in enumerate(mars_list):
            params_list = self.get_algorithm_params(mars_data.get("alg_id"))
            for i in range(random.randint(1, 3)):
                res = dict()
                param_dict = dict()
                for param in params_list:
                    param_nm = param.get("param_code")
                    if param.get("param_type") == "1" and param.get("param_type_value") == "list":
                        param_dict[param_nm] = ",".join([str(random.randint(1, 64)) for i in range(random.randint(1, 3))])
                    elif param.get("param_type") == "1":
                        param_dict[param_nm] = random.randint(1, 16)
                    elif param.get("param_type") == "2":
                        param_dict[param_nm] = random.random()
                    elif param.get("param_type") == "3":
                        param_dict[param_nm] = random.choice(param.get("param_type_value").split(","))

                res["project_id"] = job_id
                res["learn_alg_id"] = mars_data.get("alg_id")
                res["param_json"] = param_dict
                result.append(res)
        return result


if __name__ == '__main__':
    RandomRecommender()
