import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseDriver:
    """Contains generic code that allows for CRUD operations with Firebase Firestore"""
    
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._initialize_firestore()

    def _initialize_firestore(self):
        try:
            cert_str = os.getenv("FIREBASE_CONFIG")
            if cert_str:
                cert = json.loads(cert_str)
                cred = credentials.Certificate(cert)
                app = firebase_admin.initialize_app(cred, {
                    "databaseURL": cert.get("databaseURL", "https://yolo-bbea6.firebaseio.com")
                })
                self.__db = firestore.client()
            else:
                print("FIREBASE_CONFIG environment variable not set")
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError("Invalid JSON format in FIREBASE_CONFIG environment variable") from e
        except firebase_admin.exceptions.FirebaseError as e:
            raise ValueError("Firebase initialization error") from e
        except Exception as e:
            raise ValueError(f"Error initializing Firestore: {str(e)}")

    def create_document(self, collection: str, data=None):
        """
        Creates a document in the provided collection with the provided data (default=None)
        and returns the JSON data saved in Firebase.

        :param collection: collection name
        :param data: document data
        :return: JSON data saved in Firebase
        """
        ref = self.__db.collection(collection)
        doc_ref = ref.add(data)
        ref = self.__db.collection(collection).document(doc_ref[1].id)
        doc = ref.get()
        if doc.exists:
            returnDescription = doc.to_dict()
            returnDescription['doc_id'] = doc_ref[1].id
            return returnDescription
        else:
            return None




    def read_document(self, collection: str, document: str):
        """
        Fetches the contents of a document
        :param collection: collection name
        :param document: document name
        :return: document data or None if document does not exist
        """
        ref = self.__db.collection(collection).document(document)
        doc = ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    
    def get_all_documents(self, collection: str):
        """
        Retrieves all documents from a specified collection.

        :param collection: Collection name
        :return: List of JSON objects containing data from all documents in the collection
        """
        collection_ref = self.__db.collection(collection)
        query_results = collection_ref.get()
        documents = [doc.to_dict() for doc in query_results]
        return documents
        
    def find_by_parameter(self, collection: str, query_params: dict):
        """
        Finds documents in a collection based on query parameters.
        
        :param collection: collection name
        :param query_params: dictionary containing the query parameters
        :return: list of documents matching the query parameters
        """
        collection_ref = self.__db.collection(collection)
        query = collection_ref
        for key, value in query_params.items():
            query = query.where(key, '==', value)
        query_results = query.get()
        documents = [{"doc_id": doc.id, **doc.to_dict()} for doc in query_results]
        return documents


    def update_document(self, collection: str, document: str, data):
        """
        Updates a document with the provided data, merging it with existing data.
        :param collection: collection name
        :param document: document name
        :param data: document data to be merged
        :return: reference to the updated document
        """
        ref = self.__db.collection(collection).document(document)
        ref.update(data)  # Merge the provided data with existing document data
        return ref


    def delete_document(self, collection: str, document: str):
        """
        Deletes the document
        :param collection: collection name
        :param document: document name
        """
        ref = self.__db.collection(collection).document(document)
        ref.delete()
