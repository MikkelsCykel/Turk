# -*- coding: utf-8 -*-
from database import database
from random import shuffle

class infrastructure:
    def __init__(self):
        self.dbuser = database()
        self.version = '1.0'

    def prepare_hit(self, hit_id, assignment_id, worker_id):
        if not self.known_worker(worker_id):
            self.insert_worker(worker_id)
        hid = self.insert_hit(hit_id, assignment_id, worker_id)
        return hid

    def select_rnd_preview_images(self, no_rnd_img):
        query = 'SELECT i.ImgId, i.URL, i.IsGold FROM Images i '\
                    'ORDER BY rand() '\
                    'LIMIT %d;'%(no_rnd_img)
        return self.format_response(self.dbuser.query(query))

    def select_rnd_images(self, worker_id, no_gold_img, no_rnd_img):
        set_gold = self.select_rnd_gold(worker_id, no_gold_img)
        query = 'SELECT i.ImgId, i.URL, i.IsGold FROM Images i '\
                    'LEFT JOIN HitImages hi ON hi.ImgId = i.ImgId '\
                    'LEFT JOIN Hits h on h.HId = hi.Hid '\
                    'LEFT JOIN (SELECT * FROM Workers WHERE WorkerId = "%s") w on w.WorkerId = h.WorkerId '\
                    'WHERE i.IsGold = 0 '\
                    'GROUP BY i.ImgId '\
                    'HAVING Count(w.WorkerId) = 0 '\
                    'ORDER BY rand() '\
                    'LIMIT %d;'%(worker_id, no_rnd_img)
        set_img = self.format_response(self.dbuser.query(query))
        set_img = set_img + set_gold
        return shuffle(set_img)

    def select_rnd_gold(self, worker_id, no_gold_img):
        query = 'SELECT i.ImgId, i.URL, i.IsGold, Count(w.WorkerId) views FROM Images i '\
                    'LEFT JOIN HitImages hi ON hi.ImgId = i.ImgId '\
                    'LEFT JOIN Hits h on h.HId = hi.Hid '\
                    'LEFT JOIN (SELECT * FROM Workers WHERE WorkerId = "%s") w on w.WorkerId = h.WorkerId '\
                    'WHERE i.IsGold = 1 '\
                    'GROUP BY i.ImgId '\
                    'ORDER BY views '\
                    'LIMIT %d;'%(worker_id, no_gold_img)
        return  self.format_response(self.dbuser.query(query))

    def insert_worker(self, worker_id):
        query = 'INSERT IGNORE INTO Workers(WorkerId) VALUES("%s");'%(worker_id)
        return self.dbuser.insert(query)

    def known_worker(self, worker_id):
        query = 'SELECT 1 success FROM Workers WHERE WorkerId = "%s";'%(worker_id)
        success = self.dbuser.query(query)
        if not success:
            return False
        return True

    def insert_hit(self, hit_id, assignment_id, worker_id):
        query = 'INSERT INTO Hits(HitId, AssignmentId, WorkerId) VALUES ("%s", "%s", "%s");'%(hit_id, assignment_id, worker_id)
        return self.dbuser.insert(query)

    def insert_hit_response(self, hid, imgid, appealing, course, free):
        query = 'INSERT IGNORE INTO HitImages(Hid, ImgId, Appealing, Course, Free) VALUES ("%s", "%s", %d, %d, "%s");'%(hid, imgid, int(appealing), int(course), free)
        return self.dbuser.insert(query)

    def format_response(self, response):
        return [{'ImageId': int(x['ImgId']), 'IsGold': int(x['IsGold']), 'Url': x['URL']} for x in response]