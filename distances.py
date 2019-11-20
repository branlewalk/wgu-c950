def load_locations(filename, g):
    loc_name = []
    with open(filename) as f:
        locations = [line.split(',') for line in f]
        for i, x in enumerate(locations):  # print the list items
            location = x[0].strip()
            g.add_location(location)

            loc_name.append(location)
    return loc_name


def load_distances(filename, g, locations):
    with open(filename) as f:
        distances = [line.split(',') for line in f]
        for i, x in enumerate(distances):  # print the list items
            for l, d in enumerate(x):
                if d.strip() == '0':
                    break
                g.add_path(locations[i].strip(), locations[l].strip(), float(d))

