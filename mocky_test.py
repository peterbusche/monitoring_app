# mocky_test
import random

class MockSelector:
    def __init__(self, mocky_urls):
        self.mocky_urls = mocky_urls

    def get_mocky_url(self):
        return random.choice(self.mocky_urls)