
from matsuo.coordinator_service.coordinator_service import CoordinatorService
from matsuo.describe_service.describe_service import DescribeService
from matsuo.haiku_service.haiku_service import HaikuService
from multiprocessing import Process


def main():
    services = [CoordinatorService(), HaikuService(), DescribeService()]
    process_pool = list()
    for service in services:
        process_pool.append(Process(target=service.start))
    for process in process_pool:
        process.start()
    for process in process_pool:
        process.join()


if __name__ == "__main__":
    main()

