# Item Catalog Project
This .zip file contains various files that create a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication.

For this project, I have created a sports jersey catalog. Users who have logged into their Google accounts have the ability to create new jerseys and to edit and delete existing ones using CRUD operations.

## Prerequisites
* [Python2](https://www.python.org/)
* [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)

## Getting Started
Download the .zip file, which has:
* __catalog_project.py__
* __catalog_database.py__
* __lotsofsports.py__
* __client_secrets.json__
* '__templates__' folder which contains HTML files
* '__static__' folder which contains the CSS file, __catalog-stylesheet.css__

Open each file to examine its contents and comments in the code.

## Running The Script
Firing up the VM:
* Run ``` vagrant up ```
* Run ``` vagrant ssh ```
* Run ``` cd /vagrant```

To load the data, use the following commands in the virtual machine in this order:

* ```python catalog_database.py```
* ```python lotsofsports.py```
* ```python catalog_project.py```

After these steps, you may now run: ```http://localhost:8000/``` to access the catalog.

### catalog_project.py
This file contains many functions that utilize Flask in order to create the backend of this website.

App Routes have been created for the purpose of structuring specific pages of this website, such as the list of sports and jerseys, as well as links to adding, editing, and deleting specific jerseys.

In addition, the __gconnect__ and the __gdisconnect__ functions serve to allow third-party authenication using Google accounts. This code and related content has been used from Udacity's solution codes in Lesson 11, "Creating A Google Sign-In" and Lesson 17, "Securing Your APIs".

### catalog_database.py
This python file contains three classes:
* __User__
* __Sport__
* __Jersey__

These classes serve as the backbone of this application and the bridge between __catalog_project.py__ and __lotsofsports.py__.

The User class has four attributes:
* __id__ - Provided by Flask
* __name__
* __email__
* __picture__

The Sport class has two attributes:
* __id__ - Provided by Flask
* __name__

The Jersey class has eight attributes:
* __id__ - Provided by Flask
* __name__
* __description__
* __price__
* __user_id__
* __user__ - Establishes relationship with the User class
* __sport_id__
* __sport__ - Establishes relationship with the Sport class

### lotsofsports.py
This file is essentially the database of this web application. There are instances created from the User, Sports, and Jersey classes which will make up the initial items in the catalog.

## Built With
* [Atom](https://atom.io) - Text editor used to create report_tool.py and README.md
* [Vagrant](https://www.vagrantup.com/) - A tool for building and managing virtual machine environments in a single workflow.
* [VirtualBox](https://www.virtualbox.org/)- VirtualBox is a general-purpose full virtualizer for x86 hardware, targeted at server, desktop and embedded use.

## Contributing
Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors
* **Chris Jeon**

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
* Lorenzo Brown from Udacity
* Abhishek Ghosh from Udacity
* Trish Whetzel from Udacity
