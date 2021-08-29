import requests, math

q='python' # Enter query keyword here, In my case it's python.

BASE_URL = 'https://www.udemy.com'
headers = {
  "Accept": "application/json, text/plain, */*",
  "Authorization": "Basic {ENTER COMBINATION OF CLIENT KEY AND CLIENT SECRET HERE}",
  "Content-Type": "application/json;charset=utf-8"
}


#Fetching Course List
course_list = requests.get(BASE_URL+f'/api-2.0/courses/?page_size=1&search={q}', headers=headers).json()
course_list_count = int(course_list['count'])
if course_list_count > 400:
    course_list_count = 401
page_size = 20
course_list_pages = math.floor(float(course_list_count/page_size))

if course_list_count%page_size > 0:
    course_list_pages += 1

course_ids = list()

for page in range(1, page_size+1):
    course_list = requests.get(BASE_URL+f'/api-2.0/courses/?page_size={page_size}&page={page}&search={q}', headers=headers).json()
    try:
        __id = [ i['id'] for i in course_list['results'] ]
        course_ids.extend(__id)
    except KeyError:
        pass


#Fetching Course Details and Reviews
course_details = list()
course_reviews = list()

for course_id in course_ids:

    #Details
    course_detail = requests.get(BASE_URL+f'/api-2.0/courses/{course_id}/').json()
    course_details.append(course_detail)

    #Reviews
    review_page_size = 10
    review = requests.get(BASE_URL+f'/api-2.0/courses/{course_id}/reviews/?page_size=1', headers=headers).json()
    review_count = int(review['count'])

    if review_count > 100:
        review_count = 100

    review_no_of_pages = math.floor(float(review_count/review_page_size))

    if review_count%review_page_size > 0:
        review_no_of_pages += 1

    for page in range(1, review_no_of_pages+1):
        reviews_of_course_id = requests.get(BASE_URL+f'/api-2.0/courses/{course_id}/reviews/?page_size={review_page_size}&page={page}', headers=headers).json()
        try:
            course_reviews.extend(reviews_of_course_id['results'])
        except KeyError:
            pass

print('No of courses: ', course_details.__len__())
print('No of Reviews: ', course_reviews.__len__())
    




