import json
from pymongo import MongoClient, errors
from datetime import datetime


class MongoDBHandler:
    """Handles MongoDB operations."""

    def __init__(self, host: str, port: int):
        """Initialize the MongoDB connection."""
        try:
            self.client = MongoClient(host, port)
            print(f"Connected to MongoDB at {host}:{port}")
        except errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def get_database(self, db_name: str):
        """Retrieve a database."""
        return self.client[db_name]


class UserTableHandler:
    """Handles operations for the User table."""

    def __init__(self, db_handler: MongoDBHandler, dbms1: str, dbms2: str):
        """Initialize collections for fragmented User table."""
        self.db1 = db_handler.get_database(dbms1)
        self.db2 = db_handler.get_database(dbms2)
        self.collection1 = self.db1["User"]
        self.collection2 = self.db2["User"]

    def bulk_insert(self, json_file: str, batch_size: int = 1000):
        """
        Bulk inserts user data from a JSON file into the MongoDB collections.
        Data is fragmented based on the 'region' attribute.
        """
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        buffer_db1 = []
        buffer_db2 = []
        count = 0

        for record in data:
            count += 1
            # Fragmentation logic based on 'region'
            if record.get("region") == "Beijing":
                buffer_db1.append(record)
            elif record.get("region") == "HongKong":
                buffer_db2.append(record)

            # Bulk write when buffer reaches batch_size
            if len(buffer_db1) >= batch_size:
                self._write_to_db(self.collection1, buffer_db1)
                buffer_db1 = []

            if len(buffer_db2) >= batch_size:
                self._write_to_db(self.collection2, buffer_db2)
                buffer_db2 = []

        # Final flush of any remaining records
        if buffer_db1:
            self._write_to_db(self.collection1, buffer_db1)
        if buffer_db2:
            self._write_to_db(self.collection2, buffer_db2)

        print(f"Finished processing {count} records.")

    @staticmethod
    def _write_to_db(collection, data):
        """Write data to the specified collection."""
        try:
            result = collection.insert_many(data, ordered=False)
            print(f"Inserted {len(result.inserted_ids)} records into {collection.name}")
        except errors.BulkWriteError as e:
            print(f"Error during bulk insert: {e.details}")


def main():
    # Configuration
    host = "localhost"
    port = 60000
    dbms1 = "DBMS1"
    dbms2 = "DBMS2"
    json_file = "../db-generation/user.dat"  # Replace with your JSON file path
    batch_size = 1000  # Adjust based on your memory constraints

    # Initialize handlers
    db_handler = MongoDBHandler(host, port)
    user_handler = UserTableHandler(db_handler, dbms1, dbms2)

    # Perform bulk insert
    start_time = datetime.now()
    print("Starting bulk insert...")
    user_handler.bulk_insert(json_file, batch_size)
    end_time = datetime.now()
    print(f"Bulk insert completed in: {end_time - start_time}")


if __name__ == "__main__":
    main()