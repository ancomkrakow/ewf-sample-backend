import falcon


class Educations:
    def __init__(self, db):
        self.cur = db.cur

    async def on_get(self, req, resp):
        q = '''
            SELECT education_id, education
            FROM educations
            ORDER BY seq
        '''
        self.cur.execute(q)
   
        resp.media = self.cur.fetchall() 
        resp.status = falcon.HTTP_200
