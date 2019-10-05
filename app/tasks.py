import time
import random
import json
from app.models import Movie
from app import celery


@celery.task(bind=True)
def extract_movies(self, movies_list):
    movie_data = {'data':[]}
    extracted_movie = 'None'
    count = 0
    for movie_id in movies_list:
        movie = Movie.query.get(movie_id)
        status = f'Extracted: {extracted_movie}, Extracting: {movie.title}, Remaining: {len(movies_list)-count-1}'
        self.update_state(state='PROGRESS', meta={'progress': str(count)+'/'+str(len(movies_list))})
        movie_dic = {}
        movie_dic['id'] = movie.id
        movie_dic['title'] = movie.title
        movie_dic['industry'] = movie.industry
        movie_dic['writer'] = movie.writer
        movie_dic['director'] = movie.director
        movie_dic['storyline'] = movie.storyline
        movie_dic['country'] = movie.country
        movie_dic['languages'] = movie.languages
        movie_dic['genres'] = movie.genres
        movie_dic['budget'] = movie.budget
        movie_dic['box_office_domestic'] = movie.box_office_domestic
        movie_dic['box_office_gross'] = movie.box_office_gross
        movie_dic['production_company'] = movie.production_company
        movie_dic['rating'] = movie.get_rating()
        movie_dic['run_time'] = movie.run_time
        movie_data['data'].append(movie_dic)
        extracted_movie = movie.title
        count += 1

    filename = str(random.randint(99999, 999999)) + '.json'
    filepath = './app/files/' + filename
    with open(filepath, 'w') as file:
        json.dump(movie_dic, file)
    time.sleep(30)
    return filename


def task_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        return {'state':'PENDING', 'progress':"0"}
    if task.state == 'PROGRESS':
        return task.info
    if task.state == 'SUCCESS':
        return {'state':'SUCCESS', 'progress':"100"}
    else:
        return {'state':'FAILURE', 'status':"0"}

