from __future__ import annotations
from concurrent import futures
from realtime_kiwoom.rt_kiwoom import *
from realtime_kiwoom.agent import *
from miscs.time_manager import TimeManager
from miscs.config_manager import ConfigManager
import grpc
import grpc_python.prediction_pb2 as prediction_pb2
import grpc_python.prediction_pb2_grpc as prediction_pb2_grpc
from models.baseline_model import InputBuilder_BaselineModel
import sys
import pickle
import logging

class PredictionServer(prediction_pb2_grpc.PredictorServicer):

    def Predict(self, request, context):
        # dummy implementation for just testing
        input_builder = InputBuilder_BaselineModel(request)
        logging.getLogger().info(f"{input_builder.X_test}")
        return prediction_pb2.PredictResponse(actions={'X':0.9, 'Y':0.05, 'Z':0.05})


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prediction_pb2_grpc.add_PredictorServicer_to_server(PredictionServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    # cm = ConfigManager('config/.config.xml')
    # with open( "./jupyter/.grpc_reqest_sample.pkl", "rb" ) as file:
    #     serialized_buf = pickle.load(file)
    # req = prediction_pb2.PredictRequest.FromString(serialized_buf)
    # input_builder = InputBuilder_BaselineModel(req)
    # x = input_builder.X_test
    # print(x)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    serve()


