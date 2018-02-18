
from multiprocessing import Process

from matsuo.coordinator_service.service import CoordinatorService
from matsuo.describe_service.service import DescribeService
from matsuo.haiku_service.service import HaikuService
from matsuo.io_service.service import IoService


def main():
    services = [IoService(), CoordinatorService(), HaikuService(), DescribeService()]
    process_pool = list()
    for service in services:
        process_pool.append(Process(target=service.start))
    for process in process_pool:
        process.start()
    for process in process_pool:
        process.join()


if __name__ == "__main__":
    main()

