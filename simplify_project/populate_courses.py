# File to populate the database
from django.db.models import Q
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'simplify_project.settings')

import django
django.setup()
from simplify_main_app.models import Course, TutorProfile, User, StudentProfile, Profile

def populate():
    tutor_1 = [
        {
            'course_name': 'Official Python Tutorial',
            'material': 'https://docs.python.org/3/tutorial/',
            'introduction': 'abcdef',
            'id': 1
            },
        {
            'course_name':'How to Think like a Computer Scientist',
            'material':'http://www.greenteapress.com/thinkpython/',
            'introduction': 'abcdef',
            'id': 2
            },
        {
            'course_name':'Learn Python in 10 Minutes',
            'material':'http://www.korokithakis.net/tutorials/python/',
            'introduction': 'abcdef',
            'id': 3
            }
    ]
    tutor_2 = [         
        {
            'course_name':'Official Django Tutorial',
            'material':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
            'introduction': 'abcdef',
            'id': 4
            },
            {
            'course_name':'Django Rocks',
            'material':'http://www.djangorocks.com/',
            'introduction': 'abcdef',
            'id': 5
            },
            {
            'course_name':'How to Tango with Django',
            'material':'http://www.tangowithdjango.com/',
            'introduction': 'abcdef',
            'id': 6
            }
    ]
    # tutor_2 = [
    #     {
    #         'course_name':'Official Django Tutorial',
    #         'material':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
    #         'introduction': 'abcdef'
            
    #     },
    #     {
    #         'course_name':'Django Rocks',
    #         'material':'http://www.djangorocks.com/',
    #         'introduction': 'abcdef'
    #     },
    #     {
    #         'course_name':'How to Tango with Django',
    #         'material':'http://www.tangowithdjango.com/',
    #         'introduction': 'abcdef'
    #     }
    # ]

   

    cats = {'Tutor1': {'pages': tutor_1},
            'Tutor2': {'pages': tutor_2}
            }

    current_tutor_id=[]       
    current_student_id=[]
    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    i=0
    for u in User.objects.all().order_by('-role'):
        if (u.role=='TUT'):
            current_tutor_id.append(u.id)
    for u in User.objects.all().order_by('-role'):
        if (u.role=='STD'):
            current_student_id.append(u.id)
    for cat,c in cats.items():
        for p in c['pages']:
            add_page(p['course_name'],p['material'], p['introduction'])
            add_tutor_course(current_tutor_id[i],p['id'])
        i+=1
    # t=User.objects.get(id=2)
    # print(t.first_name)
    # t.first_name='Alan'
    # t.last_name='Smith'
    # print(t.first_name)
    t=Profile.objects.get(id=1)
    print (t.firstname)
    add_student_course()
    
    
        
    

def add_page(course_name,material,introduction):
    c=Course.objects.get_or_create(course_name=course_name)[0]
    c.introduction=introduction
    c.material=material
    c.save()
    return c

def add_tutor_course(i,id):
    
    for u in User.objects.all().order_by('-role'):
        if (u.role=='TUT'):
            if (u.id==i):
                t=TutorProfile.objects.get_or_create(course_id=id,user=u)
                # t.save()
            # TutorProfile.objects.get_or_create(id=i)[0]
            # c=TutorProfile.objects.create(course_id=id,user=u)
    # c=TutorProfile.objects.get_or_create(id=i)[0]
    # c.course_id=id
    
    # print(c.course_id,c)
    # c.save()
    # return c
def add_student_course():
    i=1
    for u in User.objects.all().order_by('-role'):
        if (u.role=='STD'):
            s=StudentProfile.objects.get_or_create(course_id=i,user=u)
            s=StudentProfile.objects.get_or_create(course_id=i+1,user=u)
            i+=1

#start execution here
if __name__ == '__main__':
    print('Starting Rango population script')
    populate()

