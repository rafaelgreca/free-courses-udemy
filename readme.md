# Get all udemy's free courses in a subcategory

This program will return a list of udemy's free courses in a subcategory (ordered decreasingly in relation to the relevancy score), containing the following informations: course's name, creation date, average rating, relevancy score, headline and the link.

## Getting Started

### Prerequisites

First of all, you need to get your **CLIENT ID** and the **CLIENT SECRET** from the [Udemy's page](https://www.udemy.com/user/edit-api-clients/). Login with your udemy's account and request a client's API. They will send a response in less than 24 hours. Put your credentials inside the code (lines 128 and 129).

After doing that, you need to install python 3 in your machine. Use the commands below:

```
sudo apt-get update
sudo apt-get install python3.7.2
```

### Installing

To install the program, you need to clone the repository. After that, run the following command to execute the program:

```
python3 free_courses_udemy.py
```

### Notes

You need to pass three variables values with the python3 command: the course's subcategory, the number of courses per page and the current page. All of them are essential to run the code without any errors. You can see all the valid subcategories options inside the code (starts at the line 9) or in the [Udemy's API ocumentation page](https://www.udemy.com/developers/affiliate/models/course-subcategory/). **YES, THERE IS NO PROBLEM USING SUBCATEGORY'S NAME WITH SPACES! WILL WORK ANY WAY!**

The number of courses is how many courses will be shown in one page, this value can not be higher then 100.

The current page will show the courses of the current page. For example: if the number of courses per page is 10 and the current page is 1, will be show the top 10 courses. But, if the current page is 2, will be shown the 21-40 courses. And so on.

You need to pass the arguments as the command below:

```
python3 free_courses_udemy.py -sc="SUBCATEGORY_NAME" -items ITEMS_VALUE -p CURRENT_PAGE
```

or this way:

```
python3 free_courses_udemy.py --subcategory="SUBCATEGORY_NAME" --quantity ITEMS_VALUE --page CURRENT_PAGE
```

The subcategory **MUST CONTAIN** the equal sign and the argument **HAS TO BE** between quotation marks. If hasn't one of them, the code will not work. But if you write without them, the code will only work for the subcategories' names who has one white space or none. Example: Science, Programming Languages. But will not work for 3D & Animation, Social Media Marketing, etc..

If you have any questions, use the command bellow for help:

```
python3 free_courses_udemy.py --help
```

## Authors

* **Rafael Greca** - [GitHub](https://github.com/rafaelgreca)