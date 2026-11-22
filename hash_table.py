"""CSC 225 - Hash table starter. Complete the TODO sections."""

# These prime sizes are provided; you do not need to test for prime numbers.
SIZES = [11, 23, 47, 97, 197, 397]


class HashTable:
    def __init__(self, method="linear", hash_method="mod"):
        self.method = method           # linear, quadratic, or chaining
        self.hash_method = hash_method # mod or digit
        self.capacity = 11
        self.count = 0

        if method == "chaining":
            # Each position must have its OWN list.
            # [[]] * 11 would repeat references to the SAME list.
            self.table = [[] for i in range(self.capacity)]
        else:
            self.table = [None] * self.capacity

    def hash_key(self, key):
        # These two hash functions are already provided.
        if self.hash_method == "mod":
            return key % self.capacity
        total = 0
        for digit in str(abs(key)):
            total += int(digit)
        return total % self.capacity

    def insert(self, key):
        if self.search(key):
            return
        start=self.hash_key(key) 
        if self.method == "chaining":
            self.table[start].append(key)
        elif self.method == "linear":
            for i in range(self.capacity):
                placement = (start + i) % self.capacity
                if self.table[placement] is None:
                    self.table[placement] = key
                    break
        
        elif self.method == "quadratic":
            for i in range(self.capacity):
                placement = (start + i*i) % self.capacity
                if self.table[placement] is None:
                    self.table[placement] = key
                    break
        self.count += 1

        if self.method == "linear" and (self.count + 1) / self.capacity > 0.70:
            self.resize()
        elif self.method == "quadratic" and (self.count + 1) / self.capacity > 0.50:
            self.resize()
        elif self.method == "chaining" and (self.count + 1) / self.capacity > 0.75:
            self.resize()    
        

    def search(self, key):
        
        if self.method == "chaining":
            return key in self.table[self.hash_key(key)]
        elif self.method == "linear":
            start = self.hash_key(key)
            for i in range(self.capacity):
                placement = (start + i) % self.capacity
                if self.table[placement] is None:
                    return False
                if self.table[placement] == key:
                    return True
        elif self.method == "quadratic":
            for i in range (self.capacity):
                placement = (self.hash_key(key) + i*i) % self.capacity
                if self.table[placement] is None:
                    return False
                if self.table[placement] == key:
                    return True
        return False

    def resize(self):
        old_table = self.table

        if self.capacity == SIZES[-1]:
            return 
        next_index = SIZES.index(self.capacity) + 1
        self.capacity = SIZES[next_index]
        if self.method == "chaining":
            self.table = [[] for i in range(self.capacity)]
        else:
            self.table = [None] * self.capacity
        self.count = 0

        if self.method == "chaining":
            for bucket in old_table:
                for key in bucket:
                    self.insert(key)
        else:
            for key in old_table:
                if key is not None:
                    self.insert(key)

    def show(self):
        print("\nMethod:", self.method, "| Hash:", self.hash_method)
        print("Size:", self.capacity, "| Values:", self.count)
        print("Load factor:", round(self.count / self.capacity, 2))
        for i in range(self.capacity):
            print(i, ":", self.table[i])
