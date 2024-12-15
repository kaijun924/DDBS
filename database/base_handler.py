import json
from pymongo import MongoClient, errors
from datetime import datetime
import time
from functools import wraps

def log_execution_time(func):
    """A decorator to log the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        print(f"Execution time: {end_time - start_time}")
        return result
    return wrapper

def handle_exceptions(func):
    """A decorator to handle exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
        except Exception as e:
            print(f"Error occurred in '{func.__name__}': {e}")
    return wrapper

class MongoDBHandler:
    """Handles MongoDB operations."""

    def __init__(self, host: str, port: int):
        """Initialize the MongoDB connection."""
        try:
            self.client = MongoClient(host, port)
            print(f"Connected to MongoDB at {host}:{port}")
            
            self.user_collection = self.client["userDatabase"]["User"]
            self.article_collection = self.client["articleDatabase"]["Article"]
            self.read_collection = self.client["readDatabase"]["Read"]
            self.be_read_collection = self.client["beReadDatabase"]["BeRead"]
            self.popular_rank_collection = self.client["popularRankDatabase"]["PopularRank"]
            
        except errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def get_database(self, db_name: str):
        """Retrieve a database."""
        return self.client[db_name]

class TableHandler:
    """Base class for handling common database operations."""    
    def __init__(self, collection):
        """Initialize with a MongoDB collection."""
        self.collection = collection
    
    @handle_exceptions
    @log_execution_time
    def bulk_insert(self, json_file: str, batch_size: int = 5000):
        """
        Bulk inserts data from a JSON file into the MongoDB collection.
        Uses the duplication_logic method for optional record transformation.
        """
        with open(json_file, 'r', encoding='utf-8') as file:
            buffer = []
            count = 0
            for line in file:
                record = json.loads(line)
                # Apply duplication logic (can be overridden in subclasses)
                records = self._process_record(record)
                buffer.extend(records)
                count += 1
                # if count % 100 == 0:
                #     self._write_to_db(buffer)
                #     buffer = []
                #     break
                # Bulk write when buffer reaches batch_size
                if len(buffer) >= batch_size:
                    self._write_to_db(buffer)
                    buffer = []
            # Final flush of any remaining records
            if buffer:
                self._write_to_db(buffer)
        print(f"Finished processing {count} records.")

    def _process_record(self, record):
        """
        Default process record logic: No special handling.
        Override this method in subclasses for custom logic.
        """
        return [record]
    
    def _write_to_db(self, data):
        """Write data to the specified collection."""
        try:
            result = self.collection.insert_many(data, ordered=False)
            print(f"Inserted {len(result.inserted_ids)} records into {self.collection.name}")
        except errors.BulkWriteError as e:
            print(f"Error during bulk insert: {e.details}")