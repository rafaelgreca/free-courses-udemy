'''
Developed by: Rafael Greca Vieira
GitHub: https://github.com/rafaelgreca
Copyright © 2019 Rafael Greca Vieira. All rights reserved.
'''

import requests
import base64
import re
import argparse
import urllib.parse

'''
SUBCATEGORIES OPTIONS

3D & Animation, Advertising, Affiliate Marketing, Analytics & Automation, Apple,
Architectural Design, Arts & Crafts, Beauty & Makeup, Branding, Business Law, 
Career Development, Commercial Photography, Communications, Content Marketing, Creativity,
Dance, Data & Analytics, Databases, Design Thinking, Design Tools, Development Tools,
Dieting, Digital Marketing, Digital Photography, E-Commerce, Engineering, Entrepreneurship,
Fashion, Finance, Fitness, Food & Beverage, Game Design, Game Development, Gaming,
General Health, Google, Graphic Design, Growth Hacking, Happiness, Hardware, Home Business,
Home Improvement, Human Resources, Humanities, Industry, Influence, Instruments,
Interior Design, IT Certification, Language, Leadership, Management, Marketing Fundamentals,
Math, Media, Meditation, Memory & Study Skills, Mental Health, Microsoft, Mobile Apps,
Motivation, Music Fundamentals, Music Software, Music Techniques, Network & Security,
Nutrition, Online Education, Operating Systems, Operations, Oracle, Other,
Other Teaching & Academics, Parenting & Relationships, Personal Brand Building,
Personal Finance, Personal Transformation, Pet Care & Training, Photography Fundamentals,
Photography Tools, Portraits, Product Marketing, Production, Productivity, 
Programming Languages, Project Management, Public Relations, Real Estate,
Religion & Spirituality, Safety & First Aid, Sales, SAP, Science, Search Engine Optimization,
Self Defense, Self Esteem, Social Media Marketing, Social Science, Software Engineering,
Software Testing, Spanish, Sports, Strategy, Stress Management, Teacher Training, Test Prep,
Travel, User Experience, Video & Mobile Marketing, Video Design, Vocal, Web Design,
Web Development, Yoga
'''

def get_course_average_rating(course_id, header):
    url = 'https://www.udemy.com/api-2.0/courses/'
    full_url = url + course_id + '?fields[course]=avg_rating'

    request = requests.get(full_url, headers = header)
    course_data = request.json()
    return course_data['avg_rating']

def get_course_creation_date(course_id, header):
    url = 'https://www.udemy.com/api-2.0/courses/'
    full_url = url + course_id + '?fields[course]=created'

    request = requests.get(full_url, headers = header)
    course_data = request.json()
    
    #return only the year/month/day from the creation date
    date = re.search(r'\d\d\d\d.\d\d.\d\d', str(course_data))
    return date.group()

def get_course_headline(course_id, header):
    url = 'https://www.udemy.com/api-2.0/courses/'
    full_url = url + course_id + '?fields[course]=headline'
    
    request = requests.get(full_url, headers = header)
    course_data = request.json()
    return course_data['headline']

def get_free_courses(header, subcategory, quantity, page):
    url = 'https://www.udemy.com/api-2.0/courses/?'
    informations = {'page': page, 'page_size': quantity, 'subcategory': subcategory,
                    'price': 'price-free', 'ordering': 'highest-rated'}
    end_url = urllib.parse.urlencode(informations)

    #will check and correct the urlencode with the informations
    #replace every '+' in the url to '%20' to get the right format
    for letter in end_url:
        if ord(letter) == 43:
            url += '%20'
        else:
            url += letter

    request = requests.get(url, headers = header)
    courses_data = request.json()
    
    print("\n{} free courses were found in the subcategory {}\n" .format(courses_data['count'], subcategory))
    
    #initializes the counter according to the page value and the number of items per page
    count = ((page-1)*quantity) + 1

    for course_data in courses_data['results']:
        url_course = 'https://www.udemy.com' + course_data['url']
        print("{}. {}" .format(count,course_data['title']))
        print("Relevancy score: {}" .format(course_data['relevancy_score']))
        print("Headline: {}" .format(get_course_headline(str(course_data['id']), header)))
        print("Creation date: {}" .format(get_course_creation_date(str(course_data['id']), header)))
        print("Average rating: {}" .format(get_course_average_rating(str(course_data['id']), header)))
        print("Link: {}" .format(url_course))
        print()
        print()
        count += 1 

def connect_to_the_Udemy(endpoint, client_id, client_secret, authorization):
    header = {"Authorization": "Basic {}" .format(authorization)}
    request = requests.get(endpoint, headers = header)
    response_code = re.search(r'\d+', str(request))
    
    #return the response error code from the http request
    return int(response_code.group())

def get_authorization(endpoint, client_id, client_secret):
    credentials = client_id + ':' + client_secret
    credentials_bytes = credentials.encode()
    authorization = base64.b64encode(credentials_bytes)
    authorization_decode = authorization.decode()
    
    return authorization_decode

#get the arguments from the terminal
parser = argparse.ArgumentParser()
parser.add_argument("-sc", "--subcategory", help="choose a course subcategory to filter the search", nargs='*')
parser.add_argument("-items", "--quantity", help="choose how many courses will be shown (max 100)", type=int)
parser.add_argument("-p", "--page", help="choose the selected page (if you choose page 1 and 30 itens, will show the first 30. Page 2 will show the 31-60 courses and so on.)", type=int)
parser_args = parser.parse_args()

#if the subcategory's name has a space, it's necessary join the words with a space
#this will create a unique value with the entire subcategory's name
parser_args.subcategory = ' '.join(parser_args.subcategory)

#modify this section with your client_id and client_secret
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
endpoint = 'https://www.udemy.com/api-2.0/courses'

#get the user's authorization
authorization = get_authorization(endpoint, client_id, client_secret)
header = {"Authorization": "Basic {}" .format(authorization)}
request = connect_to_the_Udemy(endpoint, client_id, client_secret, authorization)

#response error code is 200
if request == 200:
    get_free_courses(header, parser_args.subcategory, parser_args.quantity, parser_args.page)
elif request < 500:
    #response error code is 4xx
    print("Oops.. Something went wrong! Please, check if you misspelled any of yours informations.")
else:
    #response error code is 5xx
    print("Oops.. Looks like there is something wrong with the Udemy's servers. Check again later.")