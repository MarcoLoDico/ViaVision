class SharedData:
    def __init__(self):
        self.data = None

    def update_data(self, new_data):
        self.data = new_data

    def get_data(self):
        return self.data
