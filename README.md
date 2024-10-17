# Database for the school of Divinity, History, Philosophy, and Art History of the University of Aberdeen - Codename: Delta
This repository hosts the source code for a webapp based on Django, providing users with the ability to browse through a database of visual research data.

The application can be accessed at [https://t01ql23.pythonanywhere.com](https://t01ql23.pythonanywhere.com). Currently, it is deployed on PythonAnywhere. 
Due to storage limitations, we cannot deploy the full application. Consequently, the RTI-related functionality is not available in the demo version. 
We hope to transition to the university's IT infrastructure for continuous availability and full functionality in the future.


## MVT Architecture
Django follows the MVT (Model-View-Template) architecture, which is a variation of the MVC (Model-View-Controller) pattern. 
Here's a brief overview of how MVT works:

**Model:** This is the data layer. Models define the structure of the data and handle interactions with the database. 
In this application, models are defined in `models.py` and include the data schema and relationships.

**View:** This is the business logic layer. Views handle user requests, process data using the models, and pass the data to the templates. 
Views are defined in `views.py` and are responsible for retrieving data from the model and returning responses to the user.

**Templates:** This is the presentation layer. Templates are used to render the data provided by views into HTML. 
They are located in the `templates` directory and allow for the separation of presentation from business logic.

## Maintenance
### Code structure
The application follows the basic Django structure.

You'll find everything needed to understand how Django works in [its documentation](https://docs.djangoproject.com/en/5.0/).

Included libraries and packages include:
  - [Bootstrap](https://getbootstrap.com/) for easy CSS management
  - [Crispy](https://django-crispy-forms.readthedocs.io/en/latest/index.html) for the form CSS, has to be installed through pip along with [Crispy for Bootstrap 4](https://github.com/django-crispy-forms/crispy-bootstrap4)
  - [Openlime](https://github.com/cnr-isti-vclab/openlime) for RTI visualisation. This is contained within `/homepage/static/js` in the two .js files.
  - [Relightlab](https://vcg.isti.cnr.it/vcgtools/relight) for RTI transformation. Provides the function to convert RTI into the format we need. This is contained within `/homepage/RelightLab-windows`
  - [Pillow](https://pillow.readthedocs.io/en/stable/) for proper handling and displaying of image files fetched from the database

### Code structure overview
```
/digital_humanities
│
├── /homepage
│   ├── /static
│   │   ├── /css
│   │   ├── /js
│   │   │   ├── openlime.js
│   │   ├── /img
│   │
│   ├── /templates
│   │   ├── /homepage
│   │   │   ├── base.html
│   │   │   ...
│   │ 
│   ├──/RelightLab-windows/
│   │ 
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── /djangoBackend
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── manage.py
├── requirements.txt

```

### API
#### Decorators
**@staff_member_required:** Restricts view access to staff members only.

**@user_passes_test:** Allows custom user checks for view access.

**@login_required:** Restricts view access to logged-in users only.

**@csrf_protect:** Enables CSRF protection.

**@csrf_exempt:** Disables CSRF protection.



#### Django Modules and Functions
**django.core.mail:** `EmailMessage` Sends an email message.

**django.core.files:** `File` File object, `ContentFile` File object based on content.

#### RelightLAB
**relight-cli:** provide a script to convert rit files(.ptm,.hsh ...) into folder
```
relight-cli [-bpqy3PnmMwkrsSRBcCeEv]<input folder> [output folder]
```
[RelightLAB document](https://vcg.isti.cnr.it/vcgtools/relight/)

**subprocess:** a module in the Python standard library that provides a way to spawn new processes, used to run external commands and programs from within a Python script.



### Deployment
As any Django application, the server is run in a Python environment and just requires that adjustments are made to the `djangoBackend/settings.py` file, for which [documentation is provided](https://docs.djangoproject.com/en/5.0/topics/settings/).

You will find a simple guide for deploying a Django application in [their documentation](https://docs.djangoproject.com/en/5.0/howto/deployment/).

Before running the server, you will need to install the necessary packages with the following commands:
```
pip install -r requirements.txt
```

If the database is refactored in any way, migrations need to be created an applied.
This is done through running the three following commands:
```
manage.py makemigrations
manage.py makemigrations homepage
manage.py migrate
```
You can then run the server with the following command:
```
manage.py runserver 0.0.0.0:80
```

### CI/CD
### Define a Workflow:

**Create Workflow Files:** Within your repository, create a directory named .github/workflows. Inside this directory, add YAML files that define your CI/CD workflows. Each file represents a workflow and specifies the steps for building, testing, and deploying your code.

### Configure CI/CD Pipelines:
**Specify Triggers:** Define triggers for your workflows, such as push to specific branches or pull_request. This determines when your workflows should run.
**Set Up Jobs:** Jobs are defined within the workflow and include steps to perform tasks like building your code, running tests, or deploying your application. Each job runs on a specified runner, such as ubuntu-latest.

### Manage Dependencies:
**Install Dependencies:** Include steps in your workflows to install necessary dependencies for your project, ensuring that your application can be built and tested correctly.

### Deploy Your Application:
**Automate Deployment:** Define steps to deploy your application to your chosen environment (e.g., a cloud service, your own servers). This can be done directly within the workflow using deployment tools or APIs.

[GitHub Actions Documentation](https://docs.github.com/en/actions): Comprehensive guide to setting up and managing CI/CD workflows with GitHub Actions.

The code hosted in this repository is fit for a Debian server with admin priviledges and an open HTTP port.

The firewall used is [UFW](https://help.ubuntu.com/community/UFW).

### Administration and moderation
Once the Django application is deployed, most of the administration is done through the [django-admin](https://docs.djangoproject.com/en/5.0/ref/django-admin/) environment.
```
python manage.py createsuperuser
```


You can access the database and moderate it through the [django admin page](https://docs.djangoproject.com/en/5.0/#the-admin).

### Sandbox
The sandbox is allowed to be a temporary where administrator users can manage and review user uploads and requests.
  - for moderation of incoming content
  - user authentication to limit uploading to authorized users

## Extending the project
### Optimizing
There are multiple factors that should be optimized to the project:
  - Permanently hosting the application by the university VM
  - Implement 3D modeling of artifacts
  - Optimization of current RTI functions
  - Optimization of current sandbox 


### Refactoring
Currently, the project is small, but it may grow significantly when multiple RTI files are uploaded. The decision to continue using Django and SQLite will require further evaluation.

In terms of refactoring the Django project, the following should be considered:
  - **Follow Django Best Practices:** Ensure the code adheres to Django's coding conventions and best practices.
  - **Code Clarity:** Organize models, forms, and views to improve readability and maintainability.
  - **Views Refactoring:** Move functions in views.py that are not meant to forward HTTP requests to render templates into separate .py files.
  - **Template and Stylesheet Organization:** Clean and structure templates and stylesheets. Implement more Bootstrap elements for a responsive UI.
  - **Upload Form:** Enhance the upload form to reflect changes in the models and improve clarity.


### Team
Michael Nii Nai Nai-Kwade, 

Xin Feng, 

Qiancheng Luo, 

Haichun Wang, 

Xiaofan Chen,

Valentine Akoma
