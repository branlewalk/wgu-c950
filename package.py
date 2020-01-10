from datetime import timedelta, datetime
import hashtable

# Globals that are used in both classes
EOD = timedelta(hours=17)
BOD = timedelta(hours=8)


# Packages will hold on to all data that is relevant to each unique package
class Package:

    def __init__(self, package_id, location, city, zip_code, weight, deadline, truck, delay, deliver_with,
                 wrong_address):
        self.package_id = package_id
        self.location = location
        self.address = location.address
        self.city = city
        self.zip_code = zip_code
        self.package_weight = weight
        self.deadline = deadline
        self.truck = truck
        self.delay = delay
        self.deliver_with = deliver_with
        self.wrong_address = wrong_address
        self.estimated_delivery_time = timedelta()
        self.hours_to = timedelta()
        self.miles_to = 0
        self.delivery_status = 'At Hub'

    # Used to print package information when using various messages
    def __str__(self):
        return '   Package ID - {}, Location - {}, ETA - {}, '.format(self.package_id,
                                                                      self.location.address,
                                                                      self.estimated_delivery_time)

    # Used for debugging purposes
    def __repr__(self):
        return '   Package ID - {}, Address: {}, Delay: {}, Deadline - {} at ETA: {} '.format(self.package_id, self.location.address,
                                                                                              self.delay,
                                                                                              self.deadline,
                                                                                              self.estimated_delivery_time)

    # Check if package has any constraints
    def has_constraint(self):
        return len(self.deliver_with) > 0 or self.truck != '' or self.deadline != EOD or self.delay != BOD or self.wrong_address != ''


# Package warehouse holds onto all of the packages and their corresponding hash tables
class PackageWarehouse:

    def __init__(self, g):
        self.g = g
        self.packages = self.load_packages('package.csv')
        self.packages_by_id = hashtable.HashTable()
        self.packages_by_address = hashtable.HashTable()
        self.packages_by_deadlines = hashtable.HashTable()
        self.packages_by_city = hashtable.HashTable()
        self.packages_by_zip_code = hashtable.HashTable()
        self.packages_by_weight = hashtable.HashTable()
        self.packages_by_delivery_status = hashtable.HashTable()
        self.packages_by_truck = hashtable.HashTable()
        self.packages_by_location = hashtable.HashTable()
        self.packages_by_deliver_with = hashtable.HashTable()
        self.packages_by_delay = hashtable.HashTable()
        self.packages_by_wrong_address = hashtable.HashTable()
        self.packages_by_no_constraint = hashtable.HashTable()

        # O(n)
        # Initializing hash tables
        for p in self.packages:
            self.packages_by_id.put(p.package_id, p)
            self.packages_by_address.put(p.address, list())
            if p.deadline != EOD:
                self.packages_by_deadlines.put(p.deadline, list())

            self.packages_by_city.put(p.city, list())
            self.packages_by_zip_code.put(p.zip_code, list())
            self.packages_by_weight.put(p.package_weight, list())
            self.packages_by_delivery_status.put(p.delivery_status, list())

            self.packages_by_location.put(p.location, list())
            if p.truck != '' and p.truck not in self.packages_by_truck.keys:
                self.packages_by_truck.put(p.truck, list())
            if p.wrong_address != '':
                self.packages_by_wrong_address.put(p.wrong_address, list())
            if p.deadline == EOD and p.truck == '' and len(
                    p.deliver_with) == 0 and p.wrong_address == '' and p.delay == BOD:
                self.packages_by_no_constraint.put(p.package_id, list())

        # O(n)
        # Adding packages and package information to hash table
        for p in self.packages:
            self.packages_by_address.get(p.address).append(p)
            if p.deadline != EOD:
                self.packages_by_deadlines.get(p.deadline).append(p)
            self.packages_by_city.get(p.city).append(p)
            self.packages_by_zip_code.get(p.zip_code).append(p)
            self.packages_by_weight.get(p.package_weight).append(p)
            self.packages_by_delivery_status.get(p.delivery_status).append(p)

            self.packages_by_location.get(p.location).append(p)
            if p.truck != '':
                self.packages_by_truck.get(p.truck).append(p)
            if p.wrong_address != '':
                self.packages_by_wrong_address.get(p.wrong_address).append(p)
            if p.deadline == EOD and p.truck == '' and len(
                    p.deliver_with) == 0 and p.wrong_address == '' and p.delay == BOD:
                self.packages_by_no_constraint.get(p.package_id).append(p)

    # O(n)
    # Access list of 'deliver with' packages from hash table
    def get_packages_deliver_together(self, id_list):
        deliver_with_packages = list()
        for package_id in id_list:
            deliver_with_packages.append(self.packages_by_id.get(package_id))
        return deliver_with_packages

    # O(1)
    # Access total number of packages in warehouse
    def get_num_packages(self):
        return len(self.packages)

    # O(n)
    # Load packages from data file (CSV) - package.csv
    def load_packages(self, filename):
        with open(filename) as f:
            pac_list = []
            packages = [line.split(',') for line in f]
            for i, x in enumerate(packages):  # print the list items
                time = datetime.strptime(x[5].strip(), "%H:%M")
                deadline = timedelta(hours=time.hour, minutes=time.minute)
                pac_id = int(x[0].strip())
                address = x[1].strip()
                city = x[2].strip()
                zip_code = x[4].strip()
                weight = int(x[6].strip())
                truck = x[7].strip()
                d = x[8].strip()
                if x[8].strip():
                    time = datetime.strptime(d, "%H:%M")
                    delay = timedelta(hours=time.hour, minutes=time.minute)
                else:
                    delay = BOD
                dw = x[9].strip() + '/' + str(pac_id)
                if x[9].strip():
                    deliver_with = map(int, dw.split('/'))
                    deliver_with.sort()
                else:
                    deliver_with = []
                wrong_address = x[10].strip()
                package = Package(pac_id, self.g.get_location(address), city, zip_code, weight, deadline, truck, delay,
                                  deliver_with,
                                  wrong_address)
                pac_list.append(package)
            return pac_list

    def verify_packages(self):
        print('{} packages are in the warehouse.'.format(len(self.packages_by_id.keys)))
