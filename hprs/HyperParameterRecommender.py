import time
from hprs.common.Singleton import Singleton
from hprs.common.thread.KubePodSafetyTermThread import KubePodSafetyTermThread
from hprs.common.Common import Common
from hprs.manager.HPRSManager import HPRSManager


class HyperParameterRecommender(KubePodSafetyTermThread, metaclass=Singleton):
    def __init__(self, job_id: str, job_idx: str):
        KubePodSafetyTermThread.__init__(self)
        self.logger = Common.LOGGER.get_logger()

        self.hprs_manager = HPRSManager(job_id, job_idx)

        self.logger.info("HyperParameterRecommender Initialized!")

    def run(self) -> None:
        while not self.hprs_manager.get_terminate():
            self.hprs_manager.recommend()
            time.sleep(1)

        self.logger.info("HyperParameterRecommender terminate!")


if __name__ == '__main__':
    import sys

    j_id = sys.argv[1]
    j_idx = sys.argv[2]
    hprs = HyperParameterRecommender(j_id, j_idx)
    hprs.start()
    hprs.join()
