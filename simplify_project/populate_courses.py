# File to populate the database

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'simplify_project.settings')

import django
django.setup()
from simplify_main_app.models import Course

def populate():
    tutor_1 = [
        {
            'course_name': 'Official Python Tutorial',
            'material': 'https://docs.python.org/3/tutorial/',
            'introduction': 'abcdef',
           
            },
        {
            'course_name':'How to Think like a Computer Scientist',
            'material':'http://www.greenteapress.com/thinkpython/',
            'introduction': 'abcdef',
            
            },
        {
            'course_name':'Learn Python in 10 Minutes',
            'material':'http://www.korokithakis.net/tutorials/python/',
            'introduction': 'abcdef',
            
            },
             {
            'course_name':'Official Django Tutorial',
            'material':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
            'introduction': 'abcdef'
            
            },
            {
            'course_name':'Django Rocks',
            'material':'http://www.djangorocks.com/',
            'introduction': 'abcdef'
            },
            {
            'course_name':'How to Tango with Django',
            'material':'http://www.tangowithdjango.com/',
            'introduction': 'abcdef'
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

   

    cats = {'pages': tutor_1}
            

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    i=0
    
    for p in cats['pages']:
        add_page(p['course_name'],p['material'], p['introduction'])
    

def add_page(course_name,material,introduction):
    # c=Course.objects.get_or_create(course_name=course_name)[0]
    # c.introduction=introduction
    # c.material=material
    # c.save()
    # return c
    c=Course.objects.get_or_create(course_name=course_name)
    print (course_name)

#start execution here
if __name__ == '__main__':
    print('Starting Rango population script')
    populate()

