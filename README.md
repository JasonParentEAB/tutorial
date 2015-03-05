# Test-Driven Development with Django

## Initializing the Test Project

Open your terminal and navigate to the directory that contains your Django projects. On my computer, that folder is called Projects.

```bash
macbook:~ carneyadmin$ cd Projects
macbook:Projects carneyadmin$
```

Create a new Django project, _tutorial_, using the _django-admin.py_ utility, and change directories to the newly generated folder.

```bash
macbook:Projects carneyadmin$ django-admin.py startproject tutorial && cd tutorial
```

Create a new virtual environment using the _virtualenvwrapper_ utility.

```bash
macbook:tutorial carneyadmin$ mkvirtualenv tutorial
(tutorial)macbook:tutorial carneyadmin$
```

Start PyCharm and click File > Open in the menu bar. Find and select the _tutorial_ project folder. When prompted, choose to open the project in a new window. Wait for the project to open and then click PyCharm > Preferences > Project Interpreter in the menu bar to open the Project Interpreter panel. Click the gear icon in the upper right corner of the panel; then, select the "Add local..." option. In file explorer, navigate to your virtual environments folder, find the _tutorial_ directory, and select the _python2.7_ file in the _bin_ folder. On my machine, this file is located at _~/Virtualenvs/tutorial/bin_. In PyCharm, close the Preferences window. The virtual environment you just added is now being used by PyCharm for the _tutorial_ project.

Now that we have installed our virtual environment, we must add some dependencies to our project. First, install Django.

```bash
(tutorial)macbook:tutorial carneyadmin$ pip install django
```

Return to PyCharm and run the Django project by selecting Run from the menu bar. PyCharm should start the development server and log the progress in a terminal window. Click the link that PyCharm provides and your browser should open to a default Django page that reads "It worked!"

Next, install the Psycopg Python database adapter, so that we can use PostgreSQL as our database.

```bash
(tutorial)macbook:tutorial carneyadmin$ pip install psycopg2
```

In PyCharm, open the _settings.py_ file in the _tutorial_ app directory. Change the _DATABASES_ attribute to use PostgreSQL instead of SQLite.

```python
# tutorial/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tutorial',
        'USER': 'carneyadmin',
        'PASSWORD': 'password1',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```

Start the pgAdmin III program, and create a new database called _tutorial_. In the window that appears, enter _tutorial_ in the name field and _carneyadmin_ in the owner field. Close the window and then find the newly created database. Notice it does not have any tables yet.

Return to PyCharm and delete the _db.sqlite3_ file that was created when you ran the Django project initially. Migrate the database to create the default Django tables.

```bash
(tutorial)macbook:tutorial carneyadmin$ python manage.py migrate
```

If you examine your database in pgAdmin III, you should see 10 new tables. At this point, we are ready to start tracking our file changes using Git. Initialize a Git repository and commit all of the file changes that we have done up to this point.

```bash
(tutorial)macbook:tutorial carneyadmin$ git init
(tutorial)macbook:tutorial carneyadmin$ git add .
(tutorial)macbook:tutorial carneyadmin$ git commit -m "Initial commit."
```

## Beginning the Test-Driven Development Process

In general, the test-driven development workflow follows these steps:

1. Wireframe a simple model of our application or feature.
2. Write a story that narrates a user experience.
3. Write a functional test that follows the actions taken in the user story.
4. Write unit tests to evaluate the operability of low-level code.
5. Write code that satisfies the tests.

These are the critical tenets of test-driven development:

* Always write a failing test before you program any functional code.
* Write the **minimum** amount of code necessary to make a test pass.
* When a test passes, restart the process or refactor the code if necessary.

### Wireframing Our Application

Our application is going to be a simple two-screen program that allows users to create and view a list of organizations. I've created a wireframe in MockFlow. (See attachment)

### Writing Our User Story

Using our wireframes, let's imagine how the typical user is going to interact with our application. Here's a general outline of our expected user experience:

John goes to the home page. He sees an empty table with a single cell that says 'No organizations'. He also sees a button labelled 'Create organization'. He clicks the create button. The page refreshes and John sees a form with a single input: name. John enters an organization name and clicks the submit button. The page refreshes and John notices that the table now has a single row with the details of the organization that he added.

### Writing a Functional Test

Our next step is to create a functional test that follows the actions narrated by the user story. Our functional test will leverage the Selenium library to virtually open a browser and interact with the components on the screen as if it were a human user. Functional tests are extremely helpful because they allow us to mimic the actual behavior of a real user, and their actions are consistent every time. We do not need to write exhaustive functional tests to address every single on-screen interaction and scenario. In fact, when developing an application, functional tests should be written the least of any test type. Aim to write functional tests that encompass the most popular and direct set of actions that a user is expected to follow. A separate team of QA testers should check the application for any uncaught bugs when the user deviates from the expected path.

Let's implement functional tests in our Django project. Create a new Python directory called functional_tests in the tutorial project folder. Open the project's settings.py file and change the INSTALLED_APPS attribute as shown below.

```python
# tutorial/settings.py

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'functional_tests',
)

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS
```


Install the Selenium package in the terminal.

```bash
(tutorial)macbook:tutorial carneyadmin$ pip install selenium
```


Create a new Python file in the functional_tests folder and call it test_organizations. Set up a simple test case.

```python
# functional_tests/test_organizations.py

from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase


class OrganizationsTest(LiveServerTestCase):
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()
```


When run, each test in this test suite will open a web browser, execute some behaviors and assertions, and then close the browser as the test completes. These steps form the basis of every functional test. Let's see what happens when we run our functional tests.

```bash
(tutorial)macbook:tutorial carneyadmin$ python manage.py test functional_tests
```


The tests ran with no failures! We haven't actually programmed any tests yet, but at least we can see that the Django commands are running correctly. Let's create a runnable functional test using our user story. Notice how the text from the user story is broken into digestible instructions that guide our development.

```python
# functional_tests/test_organizations.py

def test_new_organizations_are_shown_in_list(self):
    # John goes to the home page. 
    self.browser.get(self.live_server_url)

    # He sees an empty table with a single cell that says 'No organizations'. 
    # He also sees a button labelled 'Create organization'. He clicks the create button. 
    cell = self.browser.find_element_by_xpath('//table/tbody/tr/td')
    self.assertEqual(cell.text, 'No organizations')
    create_button = self.browser.find_element_by_id('create-button')
    self.assertEqual(create_button.text, 'Create organization')
    create_button.click()

    # The page refreshes and John sees a form with a single input: name. 
    name_input = self.browser.find_element_by_name('name')
    self.assertEqual(name_input.get_attribute('placeholder'), 'Organization name')

    # John enters an organization name and clicks the submit button. 
    name_input.send_keys('TDD Organization')
    submit_button = self.browser.find_element_by_id('submit')
    self.assertEqual(submit_button.text, 'Submit')
    submit_button.click()

    # The page refreshes and John notices that the table now has a single row with 
    # the details of the organization that he added.
    row = self.browser.find_element_by_xpath('//table/tbody/tr')
    self.assertIn('TDD Organization', row.text)
```


Our functional test is pretty simple: 14 lines of code and 5 assertions. Selenium gives us some pretty useful methods to interact with the elements on the page. Let's quickly walkthrough what's happening in this test:

* The home page opens in the browser.

* The HTML content is searched for a <td> element and we check to make sure it says "No organizations".

* The HTML content is searched for the create button. We check to make sure it exists and then we click it.

* We expect the browser to navigate to a new page. When it refreshes, we check for the form elements, a text input control and a submit button. We also confirm that the text field has a placeholder that says "Organization name".

* We enter an organization name into the text field and submit the form.

* At this point, we expect the browser to return to the home page and we check to make sure our table contains a row with the name of our organization.

Notice how this test function covers the narrative of the user story and uses the elements drawn out in the wireframe. Let's run the unit test again and see what happens.

```bash
(tutorial)macbook:tutorial carneyadmin$ python manage.py test functional_tests
```


You should see a web browser open, wait 5 seconds, and then close with a failure. This is good! In fact, our tests should always initially fail. Now, we begin the process of making the test pass. Notice that the test failed with the message "Unable to locate element". It cannot find the <td> element in the rendered HTML. You might have also observed that the web page itself could not be found when it opened in the browser. In order to address these failures we need to write our first unit test!

### Writing a Unit Test

While a functional test mimics a real user interacting with an application, a unit test ensures that the functionality of the bits of code themselves work as expected. Our web application failed to load because we don't have anything to load yet. We're missing the fundamental elements of a Django web application: URLs, views, and templates.

Let's create a new Django app called organizations. We're creating a new app instead of using the default project app in reaction to the guidelines laid out by the creators of Django. The idea is that Django apps should be autonomous from the project, so that they can be packaged and distributed easily as individual modules.

```bash
(tutorial)macbook:tutorial carneyadmin$ python manage.py startapp organizations
```


You'll notice that your Django project is updated in PyCharm. Open your project settings and add organizations as an installed local app. This action configures and registers the module with Django, so that the URLs, views, forms, models, etc. are accessible throughout the project.

```python
# tutorial/settings.py

LOCAL_APPS = (
    'functional_tests',
    'organizations',
)
```


Inside the organizations folder, delete the tests.py file and create a Python directory called tests. Create a new Python file called test_views and place it in the tests folder. This is where our unit tests will live. Add the code shown below to create a unit test class for our views.

```python
# organizations/tests/test_views.py

from django.test import Client
from django.test import TestCase


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
```


This class creates a test case and sets up each test method to use a fake client that will interact with the framework as if it were real. Remember, this is the basic way that Django works:

1. A web client sends an HTTP request to the server.

2. The server passes the request to the Django web framework.

3. Django parses the URL from the request and resolves it to an associated view method.

4. The view processes some code that usually involves communicating with a database and then returns an HTTP response.

5. The response typically contains a string of HTML text, which is usually rendered from a template.

6. The web client receives the response and displays the content as a web page.

Let's test out our new unit test.

```bash
(tutorial)macbook:tutorial carneyadmin$ python manage.py test organizations
```


Our tests are working.

Let's add some actual logic to our unit test. At this point, we can reasonably expect that a user should be shown a web page when he or she enters a URL into the browser. Thus, our first unit test is very straightforward.

```python
# organizations/tests/test_views.py

def test_view_renders_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'organizations/home.html')
```


In this test, we are simulating a call to the home page and are confirming that we are rendering the expected template. When we run the unit tests, they fail. Remember that's a good thing! Now, let's write the minimum amount of code necessary to make this test pass. The first thing we need is a template. Create a templates/organizations directory in your organizations folder. Create a simple HTML file in the new directory and name it home.

```html
<!-- organizations/templates/organizations/home.html -->

<!DOCTYPE html>

<html>

<head lang="en">
    <meta charset="utf-8">
    <title>Tutorial</title>
</head>

<body></body>

</html>
```


Next, open the views.py file from the organizations folder. Add the minimum amount of code necessary to render the template.

```python
# organizations/views.py

def home_view(request):
    return render(request, 'organizations/home.html')
```


Lastly, open the urls.py folder in the tutorial folder and adjust the URL configuration as shown.

```python
# tutorial/urls.py

from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('organizations.views',
    url(r'^$', 'home_view', name='home'),
)
```


Run the unit tests again. They pass! Let's try the functional tests again. They fail with the same error as before, but at least we're actually rendering the expected web page. This is a good time for a commit. Look at the status of the project and then add and commit all of our new and modified files.

```bash
(tutorial)macbook:tutorial carneyadmin$ git status
(tutorial)macbook:tutorial carneyadmin$ git add .
(tutorial)macbook:tutorial carneyadmin$ git commit -m "Added functional tests and organizations."
```


## Exploring the Test-Driven Development Process

At this point, we've gotten a taste of how the basic flow of TDD works. We've created our functional test, which is driving the entire workflow. We've created our very first unit test in order to push through our functional test failures. The process is iterative: run the functional test until it breaks, create a failing unit test, write a small amount of code to make it pass, and repeat until no more errors exist. At this point, our functional test is failing because it cannot find a table cell. Let's remedy that by adding it to the template.

```html
<body>
    <table>
        <tbody>
            <tr>
                <td>No organizations</td>
            </tr>
        </tbody>
    </table>
</body>
```


Run the functional tests. They fail again, but notice that we have a new error! We've moved a step forward. Now, the create button cannot be found. Let's return to the template.

```html
<body>
    <a id="create-button" href="#">Create organization</a>
    <table>
        <tbody>
            <tr>
                <td>No organizations</td>
            </tr>
        </tbody>
    </table>
</body>
```


Run the functional tests. We've progressed a little more! Now, the test cannot find the text input control, but if we look at the user story, we realize the test fails because the page never changes. If we look at our wireframe, we can see that we need a second page, the create page. Let's follow the same steps as when we created the home page. First, create a unit test. Notice how we use a new test case for a new view.

```python
# organizations/tests/test_views.py

class HomeViewTest(TestCase): ...

class CreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_renders_template(self):
        response = self.client.get('/create/')
        self.assertTemplateUsed(response, 'organizations/create.html')
```


Next, we follow the same steps for creating the URL, view, and template as we did for the home page. Create a new HTML file in the organization templates folder called create.

```html
<!-- organizations/templates/organizations/create.html -->

<!DOCTYPE html>

<html>

<head lang="en">
    <meta charset="utf-8">
    <title>Tutorial</title>
</head>

<body></body>

</html>
```


Create the other Django files.

```python
# organizations/views.py

def home_view(request): …

def create_view(request):
    return render(request, 'organizations/create.html')
```


```python
# tutorial/urls.py

urlpatterns = patterns('organizations.views',
    url(r'^$', 'home_view', name='home'),
    url(r'^create/$', 'create_view', name='create'),
)
```


Run the unit tests. They passed! Now that we have a working web page, we can link to it in the home template.

```html
<!-- organizations/templates/organizations/create.html -->

<a id="create-button" href="{% url 'create' %}">Create organization</a>
```


Run the functional tests again. We can see the browser navigate to the create page, so we've passed one more hurdle. The tests fail because the text input field cannot be found. Let's add it.

```html
<!-- organizations/templates/organizations/create.html -->

<input type="text" name="name" placeholder="Organization name">
```


Remember, we just want the minimum amount of code necessary to move forward in the test. Don't get ahead of yourself! The functional tests fail, but we've progressed one more step. We need the submit button.

```html
<!-- organizations/templates/organizations/create.html -->

<button id="submit">Submit</button>
```


We've taken another step! Again the test is failing because it cannot find an element, but we know that the real reason is because the page hasn't navigated back home yet. Before we do anything else, let's commit our changes.

```bash
(tutorial)macbook:tutorial carneyadmin$ git add .
(tutorial)macbook:tutorial carneyadmin$ git commit -m "Home and create pages rendering correctly."
```


We need our application to return to the home page after a post request. Let's create a new unit test.

```python
# organizations/tests/test_views.py

class CreateViewTest(TestCase):
    ...

    def test_view_redirects_home_on_post(self):
        response = self.client.post('/create/')
        self.assertRedirects(response, '/')
```


The unit test fails, so let's make it pass.

```python
# organizations/views.py

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

...

def create_view(request):
    if request.method == 'POST':
        return redirect(reverse('home'))

    return render(request, 'organizations/create.html')
```


The unit test passes. The functional tests are still failing because we haven't actually added any posting behavior to our controls yet. Let's upgrade our template, so that it actually uses a form. Remember that all post calls need a CSRF token.

```html
<!-- organizations/templates/organizations/create.html -->

<form action="{% url 'create' %}" method="post">
    {% csrf_token %}
    <input type="text" name="name" placeholder="Organization name">
    <button id="submit" type="submit">Submit</button>
</form>
```


That gets the functional test moving ahead to the next failure. The new organization we created should be displayed in the list, but its not. It's time for some more advanced testing. We need to employ the use of models if we want to save our organizations. We'll have to pull the name of an organization from the post data that comes in when the form is submitted. Next, we'll need to save the organization with the given name. Lastly, we'll have to supply the home page with a list of organizations. That's a tall order. Let's get started with some unit tests.

```python
# organizations/tests/test_views.py

from ..models import Organization

class HomeViewTest(TestCase):
    ...

    def test_view_returns_organization_list(self):
        organization = Organization.objects.create(name='test')
        response = self.client.get('/')
        self.assertListEqual(response.context['organizations'], [organization])
```


PyCharm already warns us that it cannot find the model, but let's run the unit test anyway. Of course, we get an import error. Let's create the model. Open the models.py file in the organizations folder and add the following code.

```python
# organization/models.py

from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=250)
```


PyCharm stops complaining, but what happens when we run the unit test? We get a programming error! We need to add the Organization model as a table to the database. Luckily, Django makes it really easy to do this via the terminal.

```bash
(tutorial)macbook:tutorial carneyadmin$ python manage.py makemigrations organizations
(tutorial)macbook:tutorial carneyadmin$ python manage.py migrate organizations
```


Our unit tests are still failing, but the programming error is taken care of. Let's make our test pass with minimal code.

```python
# organizations/views.py

from .models import Organization


def home_view(request):
    return render(request, 'organizations/home.html', {
        'organizations': list(Organization.objects.all())
    })
```


That gets our unit tests passing. Organizations are being passed to the home page, but they are not being saved yet. Let's write another unit test to our create view.

```python
# organizations/tests/test_views.py

class CreateViewTest(TestCase):
    ...

    def test_view_creates_organization_on_post(self):
        self.client.post('/create/', data={'name': 'test'})
        self.assertEqual(Organization.objects.count(), 1)
        organization = Organization.objects.last()
        self.assertEqual(organization.name, 'test')
```


This test sends a post request to the create view with some data. The test then checks to make sure an organization is created and that it has the same name as the data sent. The unit test fails as expected. Let's write some code to make it pass.

```python
# organizations/views.py

def create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        Organization.objects.create(name=name)
        return redirect(reverse('home'))

    return render(request, 'organizations/create.html')
```


The unit tests pass. Let's try the functional tests. We're close, I can feel it. The functional test cannot find our organization, so we just need to adjust our home template.

```html
<!-- organizations/templates/organizations/home.html -->

<table>
    <tbody>
        {% for organization in organizations %}
            <tr>
                <td>{{ organization.name }}</td>
            </tr>
        {% empty %}
            <tr>
                <td>No organizations</td>
            </tr>
        {% endfor %}
    </tbody>
</table>
```


Our functional tests pass! Everything works! Let's commit our changes.

```bash
(tutorial)macbook:tutorial carneyadmin$ git add .
(tutorial)macbook:tutorial carneyadmin$ git commit -m "Added organization model. All tests passing."
```


## Refactoring Our Code

Let's take a look at our website. Wow, it's functional, but it's really ugly. Also, even though its functional, it's not functioning the most efficiently. We should be using forms to handle the data transfers and the template rendering. Let's make this site look pretty and let's add forms.

### Adding Forms

We want to utilize Django forms in our application. On the front-end, we want the forms to render the controls that we expect (the input text field). We need to pass an instance of the form to the template. We also want to replace the clunky code that is extracting the post data and manually saving the model with something smoother. Let's handle the view first.

```python
# organizations/tests/test_views.py

from ..forms import OrganizationForm

class CreateViewTest(models.Model):
    ...

    def test_view_returns_organization_form(self):
        response = self.client.get('/create/')
        self.assertIsInstance(response.context['form'], OrganizationForm)
```


As expected, the unit tests fail with an import error. Let's create the form. Add a new Python file forms.py to the organization folder and add the following code.

```python
# organizations/forms.py

from django import forms


class OrganizationForm(forms.Form): pass
```


The unit tests fail, but we don't get the import error. Add code to make the test pass.

```python
# organizations/views.py

from .forms import OrganizationForm


def create_view(request):
    ...

    return render(request, 'organizations/create.html', {
        'form': OrganizationForm()
    })
```


The unit test passes. Let's test the form to make sure that it renders the controls we want. Create a new Python file in the organization/tests directory and call it test_forms.py. Add a test that checks to see if the text input control is present.

```python
# organizations/tests/test_forms.py

from django.test import TestCase
from ..forms import OrganizationForm


class OrganizationFormTest(TestCase):
    def test_form_has_required_fields(self):
        form = OrganizationForm()
        self.assertIn('id="id_name"', form.as_p())

```


Run the unit tests and see that one fails. We need to make the form use the Organization model. Adjust the Organization form like the following.

```python
# organizations/forms.py
from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
```


The unit test passes, however, you might see a warning regarding ModelForms. Fix the form to get rid of that warning.

```python
# organizations/forms.py

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)
```


Return to our view unit tests. We need to replace the current logic, so that the form handles all of the data transfers. We need to add a couple of tests, but first let's install a new Python library.

```bash
(tutorial)macbook:tutorial carneyadmin$ pip install mock
```


Let's add a couple new unit tests for the create view.

```python
# organizations/tests/test_views.py

from mock import patch
from django.test import RequestFactory
from ..views import create_view


class CreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    ...

    @patch('organizations.views.OrganizationForm')
    def test_passes_post_data_to_form(self, mock_organization_form):
        request = self.factory.post('/create/', data={'name': 'test'})
        create_view(request)
        mock_organization_form.assert_any_call(data=request.POST)

    @patch('organizations.views.OrganizationForm')
    def test_saves_organization_for_valid_data(self, mock_organization_form):
        mock_form = mock_organization_form.return_value
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = None
        request = self.factory.post('/create/', data={'name': 'test'})
        create_view(request)
        self.assertTrue(mock_form.save.called)
```


Let's break down our changes. Notice that we are using a different strategy for these tests. Instead of using the Django client, we are using the RequestFactory to manufacture a Django HttpRequest and passing it to the view itself. In these new tests, our goal is not to test the functionality of the forms. We only want to test that the view is interacting with the form in the way it should. Our focus is on the view. 

Our first test is confirming that the request data is being passed to the form. Before, we handled the data ourselves, so now we want to make sure that the form is actually being given the chance to handle it instead. We do this by temporarily overwriting the real for with a fake form. The patch function does this and passes the fake form object to unit test to use. The only thing we need to know is that the form in our view is being called with the post parameters.

Our second test requires a little more work. Again, we are mocking the form with a fake object, but this time, we have to add some fake functions to reflect the structure of the real form. When a form is used in a view, it has to validate the input and then save, in order to successfully create a new model object. In this unit test, we are mocking the is_valid and save methods, so that they operate the way we expect them to. We are then checking to make sure that the save function is called on the form.

The unit tests fail as expected. Let's add the code to make them pass.

```python
# organizations/views.py

def create_view(request):
    form = OrganizationForm()

    if request.method == 'POST':
        form = OrganizationForm(data=request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('home'))

    return render(request, 'organizations/create.html', {
        'form': form
    })
```


We adjust the create_view so that an empty form is created on every request, and the post data is passed to the form on a post request. We also add functionality to check that the form is valid and then to save it. The unit tests pass. Our last step is to adjust the create template, so that is uses the Django form to render the controls. We replace the hard-coded HTML with the form context.

```html
<!-- organizations/templates/organizations/create.html -->

<form action="{% url 'create' %}" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button id="submit" type="submit">Submit</button>
</form>
```


When we run the functional tests, we see that they fail. We need to add a placeholder attribute to the name field. Let's adjust our form.

```python
# organizations/forms.py

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Organization name'
            })
        }
```


Both the functional tests and the unit tests are passing. We've successfully implemented forms in our project! Let's commit our code.

```bash
(tutorial)macbook:tutorial carneyadmin$ git add .
(tutorial)macbook:tutorial carneyadmin$ git commit -m "Replaced template and view code with forms."
```


### Making the Application Look Pretty

Our code is now more efficient. Using forms allows us to avoid having to edit the template and the view every time we add more fields to the form. The code is solid, but the application still looks ugly. Let's spruce it up using Bootstrap components and styles. While we're at it, let's make a base template that the home and create templates can inherit from, so we avoid duplicate code. Create a new HTML file in the organizations templates files and name it base.

```html
<!-- organizations/templates/organizations/base.html -->

<!DOCTYPE html>

<html>

<head lang="en">
    <meta charset="utf-8">
    <title>Tutorial</title>
    <meta name="viewport"
          content="user-scalable=no, width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootswatch/3.3.2/yeti/bootstrap.min.css">
</head>

<body>
    <div class="container">
        {% block page-content %}{% endblock page-content %}
    </div>

    <script src="//code.jquery.com/jquery-2.1.3.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
</body>

</html>
```


We've added a <meta> element to control for the scaling that happens when a mobile device attempts to render a full page in the viewport. We've imported Bootstrap CSS and JS files and a jQuery dependency, and we've also opted to use a free Bootstrap theme to make our page look less generic. Within the body of the HTML, we've added a block template tag that can be overridden by templates that extend this base. Let's adjust the other templates.

```html
<!-- organizations/templates/organizations/home.html -->

{% extends 'organizations/base.html' %}

{% block page-content %}
    <div class="row">
        <div class="col-md-offset-3 col-md-6">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">Organizations</h4>
                </div>
                <div class="panel-body">
                    <a id="create-button" class="btn btn-default" href="{% url 'create' %}">
                        Create organization
                    </a>
                </div>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <td><strong>Name</strong></td>
                        </tr>
                    </thead>
                    <tbody>
                        {% for organization in organizations %}
                            <tr>
                                <td>{{ organization.name }}</td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td>No organizations</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
{% endblock page-content %}
```


We spruce up the home page so that everything fits in a nice panel in the center of the screen. The table has a more interesting look with the striped style.

```html
<!-- organizations/templates/organizations/create.html -->

{% extends 'organizations/base.html' %}

{% block page-content %}
    <div class="row">
        <div class="col-md-offset-3 col-md-6">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">Create an organization</h4>
                </div>
                <div class="panel-body">
                    <form action="{% url 'create' %}" method="post">
                        {% csrf_token %}
                        {% for field in form %}
                            <div class="form-group">
                                {{ field.label_tag }}
                                {{ field }}
                            </div>
                        {% endfor %}
                        <button id="submit" class="btn btn-default" type="submit">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
{% endblock page-content %}
```


We've given a similar treatment to the create template, putting the form into a panel. In order to get our form to render with Bootstrap styling, we have a couple options. Once choice is to use a third-party library like Crispy Forms. I've chosen to implement it manually, by adding a mixin to the form class.

```python
# organizations/forms.py

class BootstrapMixin(object):
    def __init__(self, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })


class OrganizationForm(BootstrapMixin, forms.ModelForm): ...
```


Let's run all of our functional and unit tests one last time. They pass as expected. Let's visit our page and take a look. It's a lot prettier. Commit the visual changes to Git.

```bash
(tutorial)macbook:tutorial carneyadmin$ git add .
(tutorial)macbook:tutorial carneyadmin$ git commit -m "Made the templates prettier with Bootstrap."
```


 

Visit your website and try out the functionality. If you want to deploy your site or share it with others, make sure to add a remote Git repository and push your code. Also, freeze your requirements and include them in a document to make duplication of your virtual environment easier.

```bash
(tutorial)macbook:tutorial carneyadmin$ pip freeze > requirements.txt
(tutorial)macbook:tutorial carneyadmin$ git add .
(tutorial)macbook:tutorial carneyadmin$ git commit -m "Added requirements document."
(tutorial)macbook:tutorial carneyadmin$ git remote add origin git@your_git_repository
(tutorial)macbook:tutorial carneyadmin$ git push -u origin master
```
