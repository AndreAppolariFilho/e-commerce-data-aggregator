import grpc
from concurrent import futures
import time
import sales_pb2_grpc as pb2_grpc
import sales_pb2 as pb2


class SalesStreamerServicer(pb2_grpc.SalesStreamerServicer):
    def UploadSales(self, request_iterator, context):
        total_sales = 0
        total_revenue = 0.0

        # Process each sale in the stream
        for sale in request_iterator:
            print(f"Received sale: {sale.sale_id}, {sale.product_name}, "
                  f"Quantity: {sale.quantity}, Price: {sale.price}, Date: {sale.date}")
            total_sales += 1
            total_revenue += sale.quantity * sale.price

        # After all sales are processed, return a summary
        return pb2.UploadSummary(
            total_sales=total_sales,
            total_revenue=total_revenue,
            message="Sales data uploaded successfully!"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SalesStreamerServicer_to_server(SalesStreamerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    try:
        while True:
            time.sleep(86400)  # Keep server running for a day
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()