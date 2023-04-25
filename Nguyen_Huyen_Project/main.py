import os
import re
from datetime import datetime, timedelta
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import PIL.Image
import numpy as np
import dlib
from multiprocessing import Process, Queue, Manager

pose_predictor_68_point = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()

class DfaceRecognition:
    @staticmethod
    def locations_rectangles(image, face_locations) -> list:
        result = []
        for face in face_locations:
            top = max(0, face.top())
            bottom = min(face.bottom(), image.shape[0])
            left = max(0, face.left())
            right = min(face.right(), image.shape[1])
            result.append([left, top, right, bottom])
        return result

    @staticmethod
    def open_image(fileio: str, mode: str = 'RGB'):
        im = PIL.Image.open(fileio)
        if mode:
            return im.convert(mode=mode)

    @staticmethod
    def image2numpy(image):
        return np.array(image)

    def load_image_file(self, fileio: str, mode='RGB'):
        return self.image2numpy(self.open_image(fileio, mode=mode))

    @staticmethod
    def face_locations(npimg):
        return detector(npimg, 1)

    @staticmethod
    def face_encodings(npimg, faces, num_jitters: int = 1) -> list:
        raw_landmarks = [pose_predictor_68_point(npimg, face) for face in faces]
        return [np.array(face_encoder.compute_face_descriptor(npimg, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]


class FaceES:
    def __init__(self, folder_avatar: str):
        self.__folder_avatar = folder_avatar
        self.es = Elasticsearch(hosts=['http://localhost:9200'], http_auth=('elastic', 'ugUr6dICC95ZGl-wYV34'))
        self.es_index = 'labfaces'
        self.facerg = DfaceRecognition()

    def del_index(self):
        index_exists = self.es.indices.exists(index=self.es_index)
        if index_exists:
            self.es.indices.delete(index=self.es_index)
            print('delete index', self.es_index)

    def create_index(self):
        self.del_index()
        settings = {'number_of_replicas': 0,
                    'refresh_interval': '1m'}
        mapping = {'properties': {
            'fullname': {'type': 'keyword'},
            'face_encoding': {'type': 'dense_vector', 'dims': 128}}}
        print('MAPPING OK==', self.es_index, self.es.indices.create(index=self.es_index, settings=settings, mappings=mapping))

    def __push2db(self, data: list, refresh: bool = False):
        bulk_data = []
        for i, dr in enumerate(data):
            bulk_data.append(
                {
                    "_index": self.es_index,
                    "_id": i,
                    "_source": {
                        "fullname": dr["name"],
                        "face_encoding": dr["encoding"]
                    }
                }
            )
        if bulk_data:
            bulk(self.es, bulk_data)
        self.es.indices.refresh(index= self.es_index)
        print(self.es.cat.count(index=self.es_index, format="json"))

    def push_avatar_to_es(self):
        known_face_encodings = []
        for r_ in os.listdir(self.__folder_avatar):
            if not r_.startswith('.'):
                r_ = r_.strip()
                print('push_avatar_to_es', r_)
                fileio = os.path.join(self.__folder_avatar, r_)
                imgnp = self.facerg.load_image_file(fileio)
                face_locations = self.facerg.face_locations(imgnp)
                if face_locations:
                    face_encodings = self.facerg.face_encodings(imgnp, face_locations)[0]
                    known_face_encodings.append({'name': r_, 'encoding': face_encodings})
        self.__push2db(data=known_face_encodings, refresh=True)

    def training(self):
        self.del_index()
        self.create_index()
        self.push_avatar_to_es()

    def query(self, vector_encoding: list, delta: float = 0.95) -> str:
        res = []
        if vector_encoding:
            es_result = self.es.search(index=self.es_index, size=1, query={'script_score': {'query': {'match_all': {}},
                                                                                            'script': {'source': "cosineSimilarity(params.query_vector, 'face_encoding')",
                                                                                                       'params': {'query_vector': vector_encoding}}}
                                                                           })
            for dr in es_result['hits']['hits']:
                score = float(dr['_score'])
                if score > delta:
                    res.append(dr['_source']['fullname'][:-4])
        return 'or'.join(res)
        

class HelloFace(FaceES):
    def __init__(self):
        FaceES.__init__(self, folder_avatar='./data/hauiavatar')
        self.b_queue = Queue()
        self._facerg = DfaceRecognition()

    def process_frame(self,frameimg): 
        now = datetime.now()
        face_locations = self._facerg.face_locations(frameimg)
        all_fullname = []
        if face_locations:
            face_encodings = self._facerg.face_encodings(frameimg, face_locations)
            for face_encoding in face_encodings:
                fullname = (self.query(face_encoding.tolist()))
                print('Xin chào %s' % fullname, datetime.now() - now)
                all_fullname.append(fullname)
        return all_fullname


if __name__ == '__main__':
    hf = HelloFace()
    hf.training()

