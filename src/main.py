from costumer import Costumer
from reader import read_dataset


DATASET_DIR = 'dataset/Christofides_7_5_0.5.txt'

if __name__ == '__main__':
    depot = Costumer(0,0,0)
    costumers, capacity, days = read_dataset(DATASET_DIR)
