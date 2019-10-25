from package import Package


class Manifest:
    def __init__(self):
        self.packages = []
        self.truck = 0
        self.driver = 0

    def __str__(self):
        return '\n'.join(str(package) for package in self.packages)

    def set_driver(self, driver):
        self.driver = driver

    def get_driver(self):
        return self.driver

    def set_truck(self, truck):
        self.truck = truck

    def get_truck(self):
        return self.truck

    def add_package(self, package):
        if package not in self.packages:
            self.packages.append(package)
        else:
            print('Error adding: ' + str(package) + ', already on Manifest')

    def get_packages(self):
        return self.packages

