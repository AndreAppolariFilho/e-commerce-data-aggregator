import grpc
from concurrent import futures
import time
import sales_pb2_grpc as pb2_grpc
import sales_pb2 as pb2
import sqlite3
import os


class SalesStreamerServicer(pb2_grpc.SalesStreamerServicer):
    def UploadSales(self, request_iterator, context):
        total_sales = 0
        total_revenue = 0.0

        conn = sqlite3.connect(os.environ.get("DB_URL", f'{os.path.join(os.getcwd(), "db", "store.db")}'))

        cursor = conn.cursor()

        # Process each sale in the stream
        for sale in request_iterator:
            cursor.execute('''
                INSERT INTO sale (id, product_name, price, quantity, created_at) 
                VALUES (?, ?, ?, ?, ?)
            ''', (sale.sale_id, sale.product_name, sale.price, sale.quantity, sale.date))
            conn.commit()
            print(f"Received sale: {sale.sale_id}, {sale.product_name}, "
                  f"Quantity: {sale.quantity}, Price: {sale.price}, Date: {sale.date}")
            total_sales += 1
            total_revenue += sale.quantity * sale.price

        conn.close()
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
    conn = sqlite3.connect(os.environ.get("DB_URL", f'{os.path.join(os.getcwd(), "db", "store.db")}'))

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            price REAL(10, 2) NOT NULL,
            quantity INT NOT NULL,
            created_at DATETIME NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    serve()