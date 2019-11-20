from datetime import timedelta, datetime
import hashtable


class Package:
    def __init__(self, package_id, location, deadline, truck, delay, deliver_with, wrong_address):
        self.package_id = package_id
        self.location = location
        self.deadline = deadline
        self.truck = truck
        self.delay = delay
        self.deliver_with = deliver_with
        self.wrong_address = wrong_address

        self.estimated_delivery_time = timedelta()
        # TODO Fix 'delivery_status' and 'package_weight'
        # 'At Hub', 'In Transit' or 'Delivered'
        self.delivery_status = 'At Hub'
        self.package_weight = 0

    # TODO print all package data
    def __str__(self):
        return '   Package ID - {0}, Location - {1} '.format(self.package_id, self.location.get_address())

    def __repr__(self):
        return '   Package ID - {}, Deadline - {} at estimated delivery time: {} '.format(self.package_id, self.deadline, self.estimated_delivery_time)

    def get_address(self):
        return self.location.get_address()


def load_packages(filename, graph):
    with open(filename) as f:
        pac_list = []
        packages = [line.split(',') for line in f]
        for i, x in enumerate(packages):  # print the list items
            time = datetime.strptime(x[5].strip(), "%H:%M")
            deadline = timedelta(hours=time.hour, minutes=time.minute)
            address = x[1].strip()
            truck = x[7].strip()
            delay = x[8].strip()
            if x[9].strip():
                deliver_with = map(int, x[9].split('/'))
            else:
                deliver_with = []
            wrong_address = x[10].strip()
            package = Package(int(x[0].strip()), graph.get_location(address), deadline, truck, delay, deliver_with,
                              wrong_address)
            pac_list.append(package)
        return pac_list


if __name__ == '__main__':
    locations = load_packages('package.csv', )


def get_package(hash_entry):
    return hash_entry.item


class PackageWarehouse:

    def __init__(self, g):
        self.g = g
        self.packages = load_packages('package.csv', g)
        self.packages_by_address = hashtable.HashTable()
        self.packages_by_id = hashtable.HashTable()
        self.packages_by_location = hashtable.HashTable()
        self.packages_by_truck = hashtable.HashTable()
        self.packages_by_deadlines = hashtable.HashTable()
        self.packages_by_deliver_with = hashtable.HashTable()
        self.packages_by_delay = hashtable.HashTable()
        self.packages_by_wrong_address = hashtable.HashTable()
        self.packages_by_no_constraint = hashtable.HashTable()

        for p in self.packages:
            self.packages_by_location.put(p.location, list())
            self.packages_by_address.put(p.location.get_address(), list())
            self.packages_by_id.put(p.package_id, p)
            self.packages_by_truck.put(p.truck, list())
            self.packages_by_deliver_with.put(p.package_id, list())
            self.packages_by_delay.put(p.delay, list())
            if p.deadline != timedelta(hours=17):
                self.packages_by_deadlines.put(p.deadline, list())
            self.packages_by_wrong_address.put(p.wrong_address, list())
            if p.deadline == timedelta(hours=17) and p.truck == '' and len(p.deliver_with) == 0 and p.wrong_address == '' and p.delay == '':
                self.packages_by_no_constraint.put(p.package_id, list())

        for p in self.packages:
            self.packages_by_location.get(p.location).append(p)
            self.packages_by_address.get(p.location.get_address()).append(p)
            self.packages_by_truck.get(p.truck).append(p)

            self.packages_by_delay.get(p.delay).append(p)
            if p.deadline != timedelta(hours=17):
                self.packages_by_deadlines.get(p.deadline).append(p)
            self.packages_by_wrong_address.get(p.wrong_address).append(p)
            for deliver_with in p.deliver_with:
                self.packages_by_deliver_with.get(p.package_id).append(self.packages_by_id.get(deliver_with))
            if p.deadline == timedelta(hours=17) and p.truck == '' and len(p.deliver_with) == 0 and p.wrong_address == '' and p.delay == '':
                self.packages_by_no_constraint.get(p.package_id).append(p)

    def get_packages_by_truck(self, truck):
        return map(get_package, self.packages_by_truck.get_bucket(truck))

    def get_packages_deliver_together(self, package):
        return self.packages_by_deliver_with.get(package.package_id)

    def get_packages_with_deadline(self):
        deadline_packages = list()
        for packages in self.packages_by_deadlines.get_table():
            for package in packages:
                deadline_packages.append(package)
        return deadline_packages

    def get_packages_with_delay(self):
        delay_dict = dict()
        for bucket_index in range(len(self.packages_by_delay.get_table())):
            bucket = self.packages_by_delay.get_table()[bucket_index]
            if len(bucket) > 0:
                for entry in bucket:
                    p = entry.item
                    if len(p.get_delay()) > 0:
                        if p.get_delay() not in delay_dict:
                            delay_dict[p.get_delay()] = []
                        delay_dict.get(p.get_delay()).append(p)
        return delay_dict

    #TODO Make 'get_packages_with_wrong_adress' work
    def get_packages_with_wrong_address(self):
        pass