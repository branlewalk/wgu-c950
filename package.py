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

    def __str__(self):
        return 'Package ID - {0}, Location - {1}'.format(self.package_id, self.location.get_address())

    def get_address(self):
        return self.location.get_address()

    def get_package_id(self):
        return self.package_id

    def get_deadline(self):
        return self.deadline

    def get_delay(self):
        return self.delay

    def get_city(self):
        return

    def get_zip_code(self):
        return

    def get_package_weight(self):
        return

    def get_delivery_status(self):
        return

    def get_truck(self):
        return self.truck


def load_packages(filename, graph):
    with open(filename) as f:
        pac_list = []
        packages = [line.split(',') for line in f]
        for i, x in enumerate(packages):  # print the list items
            address = x[1].strip()
            truck = x[7].strip()
            delay = x[8].strip()
            if x[9].strip():
                deliver_with = map(int, x[9].split('/'))
            else:
                deliver_with = []
            wrong_address = x[10].strip()
            package = Package(int(x[0].strip()), graph.get_location(address), x[5].strip(), truck, delay, deliver_with,
                              wrong_address)
            pac_list.append(package)
            # print "Package - {0} = Delivers to {1} by {2} with constraints: {3}, {4}, {5}, {6}".format(package.package_id,
            #                                                                     package.location.get_address(),
            #                                                                     package.deadline, package.truck,
            #                                                                     package.delay, package.deliver_with,
            #                                                                     package.wrong_address)
        return pac_list


if __name__ == '__main__':
     locations = load_packages('package.csv', )


def get_package(hash_entry):
    return hash_entry.item


class PackageWarehouse:

    def __init__(self, g):
        self.g = g
        self.packages = load_packages('package.csv', g)

        self.package_by_address = hashtable.HashTable()
        self.package_by_id = hashtable.HashTable()
        self.package_by_location = hashtable.HashTable()
        self.package_by_truck = hashtable.HashTable()
        self.package_by_deadlines = hashtable.HashTable()
        self.package_by_deliver_with = hashtable.HashTable()
        self.package_by_delay = hashtable.HashTable()
        self.package_by_wrong_address = hashtable.HashTable()

        for p in self.packages:
            self.package_by_location.put(p.location, p)
            self.package_by_address.put(p.location.get_address(), p)
            self.package_by_id.put(p.get_package_id(), p)
            self.package_by_truck.put(p.truck, p)
            self.package_by_delay.put(p.delay, p)
            self.package_by_deadlines.put(p.deadline, p)
            self.package_by_wrong_address.put(p.wrong_address, p)

    def get_packages_by_truck(self, truck):
        return map(get_package, self.package_by_truck.get_bucket(truck))

    def get_packages_deliver_together(self):
        deliver_together = []
        for p in self.packages:
            if len(p.deliver_with) > 0:
                if not self.deliver_together_exists(deliver_together, p):
                    together = []
                    deliver_together.append(together)
                    together.append(p)
                    for package_id in p.deliver_with:
                        package = self.package_by_id.get(package_id)
                        together.append(package)
        return deliver_together

    def deliver_together_exists(self, deliver_together, p):
        for pac_list in deliver_together:
            if pac_list.__contains__(p):
                return True
        return False

    def get_packages_with_deadline(self):
        eod_bucket = self.package_by_deadlines.hash_key('EOD')
        deadline_dict = dict()
        for bucket_index in range(len(self.package_by_deadlines.get_table())):
            if bucket_index is not eod_bucket:
                bucket = self.package_by_deadlines.get_table()[bucket_index]
                if len(bucket) > 0:
                    for entry in bucket:
                        p = entry.item
                        if p.get_deadline() not in deadline_dict:
                            deadline_dict[p.get_deadline()] = []
                        deadline_dict.get(p.get_deadline()).append(p)
        return deadline_dict

    def get_packages_with_delay(self):
        delay_dict = dict()
        for bucket_index in range(len(self.package_by_delay.get_table())):
            bucket = self.package_by_delay.get_table()[bucket_index]
            if len(bucket) > 0:
                for entry in bucket:
                    p = entry.item
                    if len(p.get_delay()) > 0:
                        if p.get_delay() not in delay_dict:
                            delay_dict[p.get_delay()] = []
                        delay_dict.get(p.get_delay()).append(p)
        return delay_dict

