class MinimalRegionSet():
    def __init__(self):
        self.local_set = []

    def add(self, region):
        local_set = self.local_set
        add = True

        for region_in_set in local_set:
            if region_in_set.contains(region):
                add = False
                break
            if region.contains(region_in_set):
                local_set.remove(region_in_set)

        if add:
            local_set.append(region)

    def add_all(self, regions):
        for region in regions:
            self.add(region)

    def contains(self, region):
        local_set = self.local_set

        for local_region in local_set:
            if region == local_region:
                return True

        return False

    def to_array(self):
        return self.local_set
