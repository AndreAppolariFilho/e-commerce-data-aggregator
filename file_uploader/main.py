import multiprocessing

from flask import Flask, request, jsonify
import csv
import grpc
import sales_pb2_grpc as pb2_grpc
import sales_pb2 as pb2


app = Flask(__name__)

def read_csv(file):
    reader = csv.reader(file)
    for row in reader:
        yield row


def generate_sales_records(file):
    for row in read_csv(file):
        yield pb2.SalesRecord(
            sale_id=row["sale_id"],
            product_name=row["product_name"],
            quantity=row["quantity"],
            price=row["price"],
            date=row["date"]
        )


def send_data_to_aggregate(file):
    channel = grpc.insecure_channel('data_aggregation:50051')
    stub = pb2_grpc.SalesStreamerStub(channel)

    response = stub.UploadSales(generate_sales_records(file))
    print(f"Server response: Total Sales: {response.total_sales}, "
          f"Total Revenue: {response.total_revenue}, Message: {response.message}")


@app.route("/sales", methods=["POST"])
def sales_list_api_view():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({'error': 'No file sent in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        process = multiprocessing.Process(target=send_data_to_aggregate, args=(file.stream.read()))
        process.start()
        return jsonify({
            'message': 'File successfully uploaded and its being processed',
        }), 200