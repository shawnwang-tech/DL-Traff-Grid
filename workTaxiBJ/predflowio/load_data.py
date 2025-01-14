import numpy as np
from Param_DMVST_flow import *


def select_topo(i, topo_data):
    loc_x = i // WIDTH
    loc_y = i % WIDTH
    topo_location = (loc_x // grid_size) * (WIDTH // grid_size) + (loc_y // grid_size)
    return topo_data[topo_location]


def data_generator(data_list, temporal_data_list, topo_data, batch_size, timestep, model_name):
    seed = 0
    np.random.seed(seed)
    while True:
        for n_data in range(len(data_list)):
            data = data_list[n_data]
            temporal_data = temporal_data_list[n_data]

            num_time = data.shape[0] - timestep
            num_region = data.shape[1]
            y_location = data.shape[2] // 2


            time_random = np.arange(num_time)
            region_random = np.arange(num_region)
            np.random.shuffle(time_random)
            np.random.shuffle(region_random)

            trainX, temporal, topo, trainY = [], [], [], []
            batch_num = 0

            for t in time_random:
                for i in region_random:
                    x = data[t:t + timestep, i, :, :, :]
                    if model_name == 'density':
                        y = data[t + timestep, i, y_location, y_location, 0]
                    temp_fea = temporal_data[t:t + timestep]
                    topo_fea = select_topo(i, topo_data)
                    trainX.append(x), temporal.append(temp_fea), topo.append(topo_fea), trainY.append(y)
                    batch_num += 1

                    if batch_num == batch_size:
                        trainX, temporal, topo, trainY = np.array(trainX), np.array(temporal), np.array(topo), np.array(
                            trainY)
                        yield [trainX, temporal, topo], trainY
                        batch_num = 0
                        trainX, temporal, topo, trainY = [], [], [], []


def test_generator(data_list, temporal_data_list, topo_data, batch_size, timestep):
    while True:
        for n_data in range(len(data_list)):
            data = data_list[n_data]
            temporal_data = temporal_data_list[n_data]

            num_time = data.shape[0] - timestep
            num_region = data.shape[1]

            time = np.arange(num_time)
            region = np.arange(num_region)

            testX, temporal, topo = [], [], []
            batch_num = 0

            for t in time:
                for i in region:
                    x = data[t:t + timestep, i, :, :, :]
                    temp_fea = temporal_data[t:t + timestep]
                    topo_fea = select_topo(i, topo_data)
                    testX.append(x), temporal.append(temp_fea), topo.append(topo_fea)
                    batch_num += 1

                    if batch_num == batch_size:
                        testX, temporal, topo = np.array(testX), np.array(temporal), np.array(topo)
                        yield [testX, temporal, topo]
                        batch_num = 0
                        testX, temporal, topo = [], [], []


def get_test_true(data_list, timestep, model_name):
    testY = []
    for n_data in range(len(data_list)):
        data = data_list[n_data]
        num_time = data.shape[0] - timestep
        num_region = data.shape[1]
        y_location = data.shape[2] // 2

        for t in range(num_time):
            for i in range(num_region):
                if model_name == 'density':
                    y = data[t + timestep, i, y_location, y_location, 0]
                    testY.append(y)
    testY = np.array(testY)
    return testY
