import time
from hprs.common.Singleton import Singleton
from hprs.common.thread.KubePodSafetyTermThread import KubePodSafetyTermThread
from hprs.common.Common import Common
from hprs.common.Constants import Constants
from hprs.manager.HPRSManager import HPRSManager


class HyperParameterRecommender(KubePodSafetyTermThread, metaclass=Singleton):
    def __init__(self, job_id: str, job_idx: str):
        KubePodSafetyTermThread.__init__(self)
        self.logger = Common.LOGGER.get_logger()

        self.hprs_manager = HPRSManager(job_id, job_idx)
        try:
            self.hprs_manager.initialize()
            self.logger.info("HyperParameterRecommender Initialized!")
        except Exception as e:
            self.logger.error(e, exc_info=True)

    def run(self) -> None:
        while not self.hprs_manager.get_terminate():
            try:
                self.hprs_manager.recommend()
            except Exception as e:
                self.logger.error(e, exc_info=True)
                self.hprs_manager.update_project_status(Constants.STATUS_PROJECT_ERROR)
            finally:
                time.sleep(10)

        self.logger.info("HyperParameterRecommender terminate!")
        self.hprs_manager.terminate()


if __name__ == '__main__':
    import sys

    j_id = sys.argv[1]
    j_idx = sys.argv[2]
    hprs = HyperParameterRecommender(j_id, j_idx)
    hprs.start()
    hprs.join()
