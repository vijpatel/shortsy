import os
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from fetch_details import fetch
from requests import post
from connect import connect
from insert_query import insert_url
from create_hash import encode,decode
from update import update_clicks
from hashids import Hashids
from custom_url_check import check

# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tHiSiSaSeCrEtKeY'
app.config['DEBUG'] = os.getenv('DEBUG')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('PUBLIC_KEY')
app.config['RECAPTCHA_OPTIONS']= {'theme':'white'}
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        url = request.form['url']
        captcha_response = request.form['g-recaptcha-response']
        recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_secret_key = os.getenv('PRIVATE_KEY')
        payload = {
           'secret': recaptcha_secret_key,
           'response': captcha_response,
        }
        response = post(recaptcha_url, data = payload)
        result = response.json()
        predefined_keywords = ('view','success','about')
        if not url:
            flash('The URL is required!')
        elif request.form['urloption'] == 'custom' and request.form['customurl'] == '':
            flash('Please specify the custom URL')
        elif not result.get('success', None):
            flash('Invalid ReCaptcha!')
        else:
            if request.form['urloption'] == 'custom':
                custom_url = request.form['customurl']
                if custom_url in predefined_keywords:
                    flash('Already used by system. Try something different.')
                elif check(custom_url):
                    flag,url_data = insert_url(url,custom_url)
                    return render_template('success.html', short_url = custom_url)
                else:
                    flash('Custom URL already taken :(. Try something unique...')
            else:
                flag,url_data = insert_url(url)
                if flag:
                    hashid = encode(url_data)
                    return render_template('success.html', short_url = hashid)
                else:
                    flash('Something went wrong, please try again later.')
        return render_template('index.html')
    return render_template('index.html')
@app.route('/<id>')
def url_redirect(id):
    url = ''
    url,index,clicks = decode(id,only_url = True)
    if url:
        update_clicks(index,clicks+1)
        return redirect(url)    
    else:
        abort(404)
@app.route('/success')
def success():
    u = request.args.get('short_url')
    #<a href = {{ url_for('find_question' ,question_id=1) }}>Question 1</a>
    return render_template("success.html",
      url = request.args.get('short_url'))
    return render_template('success.html')
@app.route('/view', methods=('GET', 'POST'))
def view():
    if request.method == "POST":
        url = request.form['url']
        if not url:
            flash('The URL is required!')
            return render_template('view.html')
        # url_split = url.split('/')
        short_url = url
        # id = hashids.decode(short_url)
        # if not id:
        #     data = fetch(short_url = short_url)
        # else:
        #     data = fetch(id = id)
        data = decode(short_url)
        if data:
            data['short_url'] = request.url_root + short_url
            return render_template('info.html',data = data)
        else:
            flash('URL Not Found')
    return render_template('view.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def error(e):
    return render_template('error.html')


# @app.route('/stats')
# def stats():
#     conn = get_db_connection()
#     db_urls = conn.execute('SELECT id, created, original_url, clicks FROM urls'
#                            ).fetchall()
#     conn.close()

#     urls = []
#     for url in db_urls:
#         url = dict(url)
#         url['short_url'] = request.host_url + hashids.encode(url['id'])
#         urls.append(url)

#     return render_template('stats.html', urls=urls)
    