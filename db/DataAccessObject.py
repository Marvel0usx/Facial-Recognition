import pymongo
from pymongo.errors import *
import numpy
import pandas


class DataAccessObject:
    """Class that wraps APIs to access MongoDB in a nicer way."""

    def __init__(self, client: pymongo.MongoClient, database="", collection=""):
        self.client = client
        # Basic assertion to ensure valid client.
        assert client is not None
        assert type(database) is str
        assert type(collection) is str
        try:
            self.database = self.client.get_database(database)
            self.collection = self.database.get_collection(collection)
        except InvalidURI as e:
            raise e(f"Database {self.database} is not available")
        except CollectionInvalid as e:
            raise e(f"Collection {self.collection} is not available")
        except PyMongoError as e:
            raise e(f"Could not open database {self.database} collection {self.collection}")

    def get_num_image(self, num):
        return self.collection.find({}).limit(num)

    def get_all_image_by_key(self, key):
        return self.collection.find({str(key), key})

    def get_num_image_by_keys(self, num=100, **keys):
        return self.collection.find(keys).limit(num)

    def partition_dataset(self, training, testing):
        count = self.collection.count_documents({})
        assert training + testing <= 1
        training_size = round(count * training)
        testing_size = round(count * testing)

        return self.collection.find({}).limit(training_size),\
                self.collection.find({}).skip(training_size).limit(testing_size)


if __name__ == "__main__":
    client = pymongo.MongoClient(host="mongodb://127.0.0.1", port=27017)
    dao = DataAccessObject(client, "local", "faceData")
    ins = DataAccessObject(client, "local", "faceData")
    print("get 10 images")
    print([i for i in ins.get_num_image(10)])

    print("\nget 10 of adult age")
    print([i for i in ins.get_num_image_by_keys(10, age="adult")])

    print("partition dataset")
    train, test = ins.partition_dataset(0.7, 0.3)

    print("trainging: " + str(len(list(train))) + "\ntesting: " + str(len(list(test))))
