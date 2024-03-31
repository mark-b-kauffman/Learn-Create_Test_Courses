### Project Title: Learn-Create_Test_Courses
### Description:
They create_courses notebook will create some number of test courses on a Blackboard Learn system and time how long it takes to complete the process. It will show that time and the average time taken per course when complete. NOTE: You MUST have created a data source key (DSK) on the Learn system you run this code against that has an external ID of: ATESTDSK

We have also provided a delete_courses notebook to delete the courses that you create. This is because you cannot run the code to create courses if the courses already exist on the Learn system.

This code is subject to the terms given in the LICENSE.md file included with this project.

### Prerequisites:
* OS: MacOSX 14^ (Windows will require the Windows port of pyenv for Windows.) We explain how to install the following prerequisites in the Installation section below.
* Python version management: pyenv
* Python environment managment: pipx
* Python package management: Poetry
* A REST Application registered on developer.anthology.com
* The REST Application is deployed to a Learn server
* The same Learn server has a datasource key you've created, named ATESTDSK


### Installation:
* Use Git to clone this project to your local machine.
* cd Learn-Create_Test_Courses
* Install pyenv
    * See https://github.com/pyenv/pyenv?tab=readme-ov-file#installation  
* Use pyenv to install and use Python3.11.2 or greater.
    * pyenv install 3.11.2
* Set Python 3.11.2 to be used for this project.
    * pyenv local 3.11.2
* Install pipx
    * python3 -m pip install --user pipx
    * If you get warnings about your the path to your Python bin dir, follow the instructons on how to fix them.
* Ensure pipx is on your path variable
    * python3 -m pipx ensurepath
* Install Poetry
    * pipx install poetry
* Add the necessary Python libraries using Poetry
    * poetry add requests@latest
    * poetry add ipython@latest
    * poetry add nbformat
* Install Jupyter Lab
    * poetry add --dev jupyterlab
* Install ngrok or some other proxy to make the Flask server available on the public internet.
    * For ngrok see: https://ngrok.com/docs/getting-started/
        * (We purchased our own domain for this demo... And we need to run on a system that isn't blocked by any firewall rules...)

### Usage (Launching the project):
* poetry run jupyter lab
* Open the src folder.
* Copy Config_template.py to Config.py and in Config.py set the values specific to your REST application and Learn server.
* Access and run the Python code notebooks in the src/ folder.
* NOTE: Several things to check if you get errors:
    * Did you set up your Config.py with the necessary values?
    * Did you create the ATESTDSK data source key on your Learn system?
    * Did you delete courses if you've already created them?

### Other Useful Things
* For convenience a main.py script has been provided that can be used to run the create_courses and delete_courses code.
    * cd Learn-Create_Test_Courses
    * python main.py create|delete \<n\>
      * Where n is the number of courses to create or delete.
* You can create a bash script using the above to continually create courses, delete them, and see the timing.
* Example:
````
% cd src
% while true
do
  python main.py create 50
  python main.py delete 50
  sleep 200
done
````

* The output will look something like:
````
importing Jupyter notebook from create_courses.ipynb
importing Jupyter notebook from delete_courses.ipynb
learn_auth(): Learn Authentication successful
learn_auth(): Token expires at: 2024-03-31 12:05:40.254077
WARNING: The Learn AMI only allows for 100 courses total!
n is: 50. creating 50 courses
0:00:32.180881 to create 50 courses. 0:00:00.643618 per course.
importing Jupyter notebook from create_courses.ipynb
importing Jupyter notebook from delete_courses.ipynb
learn_auth(): Learn Authentication successful
learn_auth(): Token expires at: 2024-03-31 12:05:40.557343
n is: 50. deleteing 50 courses
0:00:20.200578 to delete 50 courses. 0:00:00.404012 per course.
WARNING: After deleteting courses you will need to WAIT up to 5 minutes before creating again.
importing Jupyter notebook from create_courses.ipynb
importing Jupyter notebook from delete_courses.ipynb
learn_auth(): Learn Authentication successful
learn_auth(): Token expires at: 2024-03-31 12:05:40.944474
WARNING: The Learn AMI only allows for 100 courses total!
n is: 50. creating 50 courses
0:00:31.426035 to create 50 courses. 0:00:00.628521 per course.
````



