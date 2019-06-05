from .celery_config import celery_app

@celery_app.task(name="task.run_createWordCloud")
def run_createWordCloud(session):
    from word_cloud.wordcloud import run_word_cloud
    refferrer = run_word_cloud(session)
    return refferrer
    