from src.client.client import Client

HOST, PORT = "ec2-52-56-46-175.eu-west-2.compute.amazonaws.com", 5000
if __name__ == "__main__":
    client = Client(host=HOST)
    client.start()
