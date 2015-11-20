from flask import Flask, render_template, jsonify, request, redirect
# from flask import jsonify
import requests
import json
import re
import time
import urllib2

app = Flask(__name__)

@app.route('/')
def main_site():
    return render_template('temp.html')
    # 'Hello World!'

@app.route('/results', methods=['POST'])
def handle_data():
    subreddit = request.form['subreddit']
    numof_submissions = request.form['submissions']
    if subreddit == '':
        subreddit = 'earthporn'
    if numof_submissions == '':
        # numof_submissions = '25'

        return redirect('/' + subreddit)
    if int(numof_submissions) > 100:
        return redirect('/' + subreddit + '/' + '100') 
    else:
        return redirect('/' + subreddit + '/' + numof_submissions)

@app.route('/<subreddit>')
def get_default(subreddit):
    return get_pics(subreddit)

@app.route('/<subreddit>/')
def get_default2(subreddit):
    return get_pics(subreddit)

@app.route('/<subreddit>/<submissions>')
def get_pics(subreddit, submissions = '25'):
    try:
        number = int(submissions)
    except ValueError:
        return redirect('/error')
    if number > 100:
        return redirect('/' + subreddit + '/' + '100') 
    # start_time = time.time() #time functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      start_time = time.time() #time functions
    header = {'User-Agent':'Ronak Python Img-Scraper'}
    base_url = 'https://www.reddit.com/r/'
    url = base_url + subreddit + '/.json?limit=' + submissions
    r = requests.get(url, headers = header)
    res = r.json()
    url_to_link = []
    for children in res['data']['children']:
        url_to_link.append(children['data']['url'])
    links = []
    # thumbnails = []
    for link in url_to_link:
        if re.search('(https?://)?(i.)?imgur.com/[A-Za-z0-9]*.(gifv)', link) != None:
            links.append(link[:-1])
        elif re.search('(https?://)?(i.)?imgur.com/[A-Za-z0-9]*.(png|jpg|gif)', link) != None:
            links.append(link)
        elif re.search('(https?://)?(i.)?imgur.com/[A-Za-z0-9]{7}(?!/)',link) != None:
            links.append(link + '.jpg')  
        #----------Gets albums and Gallerys-----------
        elif re.search('(https?://)?(i.)?imgur.com/', link) != None: #need to adjust links
            imgur = requests.get(link)
            proper_links = re.findall('img src="//i.*?"', imgur.text)
            for src in proper_links:
                links.append(src[9:-1])
    return render_template('main.html', urls = links, subreddit = subreddit)

@app.route('/error')
def display_error():
    return render_template('error.html')

if __name__ == '__main__':
    app.debug = True
    app.run()

# TODO
# proper error response on form validation
# make error page
# limit number of submissions to only 3 characters
# format pictures
# create my own html and stuff
# create a download function    