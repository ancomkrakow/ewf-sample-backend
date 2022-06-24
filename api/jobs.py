import falcon


class Jobs:
    def __init__(self, db):
        self.cur = db.cur

    async def on_get(self, req, resp):
        q = '''
            SELECT job_id, job
            FROM jobs
            ORDER BY job
        '''
        self.cur.execute(q)
   
        resp.media = self.cur.fetchall() 
        resp.status = falcon.HTTP_200
