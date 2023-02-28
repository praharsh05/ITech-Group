from django.test import TestCase, Client
import os
import importlib
from django.urls import reverse
from django.conf import settings


# Create your tests here.


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


# setup tests for the new simplify project, original taken from https://github.com/tangowithcode/tango_with_django_2_code.git
class SetupTest(TestCase):
    """
    Simple tests to probe the file structure of the project so far.
    Test to check if simplify_main_app is added to the list of INSTALLED_APPS.
    """

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.simplify_app_dir = os.path.join(
            self.project_base_dir, 'simplify_main_app')

    def test_project_created(self):
        """
        Tests whether the simplify_project configuration directory is present and correct.
        """
        directory_exists = os.path.isdir(os.path.join(
            self.project_base_dir, 'simplify_project'))
        urls_module_exists = os.path.isfile(os.path.join(
            self.project_base_dir, 'simplify_project', 'urls.py'))

        self.assertTrue(
            directory_exists, f"{FAILURE_HEADER}Simplify project configuration directory doesn't exist{FAILURE_FOOTER}")
        self.assertTrue(
            urls_module_exists, f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")

    def test_app_created(self):
        """
        Determines whether the simplify_main_app has been created.
        """
        directory_exists = os.path.isdir(self.simplify_app_dir)
        is_python_package = os.path.isfile(
            os.path.join(self.simplify_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(
            os.path.join(self.simplify_app_dir, 'views.py'))

        self.assertTrue(
            directory_exists, f"{FAILURE_HEADER}The simplify app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(
            is_python_package, f"{FAILURE_HEADER}The simplify directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(
            views_module_exists, f"{FAILURE_HEADER}The simplify directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")

    def test_simplify_has_urls_module(self):
        """
        Determines if a seperate urls.py was created for simplify or not
        """
        module_exists = os.path.isfile(
            os.path.join(self.simplify_app_dir, 'urls.py'))
        self.assertTrue(
            module_exists, f"{FAILURE_HEADER}The simplify_main_app app's urls.py module is missing.{FAILURE_FOOTER}")

    def test_is_simplify_app_configured(self):
        """
        Determines if simplify_main_app app was added to the INSTALLED_APPS list.
        """
        is_app_configured = 'simplify_main_app' in settings.INSTALLED_APPS

        self.assertTrue(
            is_app_configured, f"{FAILURE_HEADER}The simplify_main_app app is missing from the setting's INSTALLED_APPS list.{FAILURE_FOOTER}")


class IndexPageTests(TestCase):
    """
    Testing the basic index view and URL mapping.
    Also runs tests to check the response from the server.
    """

    def setUp(self):
        self.views_module = importlib.import_module('simplify_main_app.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module(
            'simplify_project.urls')

    def test_view_exists(self):
        """
        Does the index() view exist in simplify_main_app's views.py module?
        """
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)

        self.assertTrue(
            name_exists, f"{FAILURE_HEADER}The index() view for simplify does not exist.{FAILURE_FOOTER}")
        self.assertTrue(
            is_callable, f"{FAILURE_HEADER}Check that you have created the index() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in simplify's urls.py.
        We have the 'index' view named twice -- it should resolve to '/simplify/'.
        """
        index_mapping_exists = False

        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True

        self.assertTrue(index_mapping_exists,
                        f"{FAILURE_HEADER}The index URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('simplify_main_app:index'), '/simplify/',
                          f"{FAILURE_HEADER}The index URL lookup failed. Check simplify_main_app's urls.py module{FAILURE_FOOTER}")

    def test_response(self):
        """
        Does the response from the server contain the required string?
        """
        response = self.client.get(reverse('simplify_main_app:index'))

        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}Requesting the index page failed. Check your URLs and view.{FAILURE_FOOTER}")

    

class TemplateTests(TestCase):
    """
    Check that the base template exists, and that each page in the templates/simplify_main_app directory has a title block.
    """

    def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file.
        """
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str

    def test_base_template_exists(self):
        """
        Tests whether the base template exists.
        """
        template_base_path = os.path.join(
            settings.TEMPLATE_DIR, 'simplify_main_app', 'base.html')
        self.assertTrue(os.path.exists(template_base_path),
                        f"{FAILURE_HEADER}No base.html template found in the templates/simplify_main_app directory.{FAILURE_FOOTER}")


    def test_template_usage(self):
        """
        Check that each view uses the correct template.
        """

        urls = [reverse('simplify_main_app:index'),]

        templates = ['simplify_main_app/index.html',]

        for url, template in zip(urls, templates):
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)

    def test_for_links_in_base(self):
        """
        There should be hyperlinks in base.html,
        Check for their presence, along with correct use of URL lookups.
        """
        template_str = self.get_template(os.path.join(
            settings.TEMPLATE_DIR, 'simplify_main_app', 'base.html'))

        look_for = [
            '<a href="{% url \'simplify_main_app:index\' %}">Home</a>',
        ]

        for lookup in look_for:
            self.assertTrue(
                lookup in template_str, f"{FAILURE_HEADER}In base.html, we couldn't find the hyperlink '{lookup}'. Check your markup in base.html is correct and as written in the book.{FAILURE_FOOTER}")


#checks for different addition in base template
class TestHtmlPage(TestCase):

    def setUp(self):
        self.client = Client()

    def test_html_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_navbar_links(self):
        response = self.client.get('/')
        self.assertContains(response, 'Home')  # check if Home link is present in navbar 
        self.assertContains(response, 'About Us')  # check if About Us link is present in navbar 
        self.assertContains(response, 'Courses')  # check if Courses link is present in navbar 
        self.assertContains(response, 'Signup/Login')  # check if Signup/Login link is present in navbar 

    def test_footer_links(self):
        response = self.client.get('/')
        self.assertContains(response, 'Home')  # check if Home link is present in footer 
        self.assertContains(response, 'About Us')  # check if About Us link is present in footer  
        self.assertContains(response, 'Courses')  # check if Courses link is present in footer  
        self.assertContains(response, 'Signup/Login')  # check if Signup/Login link is present in footer