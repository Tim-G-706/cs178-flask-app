# Restaurant Database Website

**CS178: Cloud and Database Systems — Project #1**
**Author:** Tim Groth
**GitHub:** Tim-G-706

---

## Overview

This project contains two databases, with one being a SQL database storing information such as general restaurant data and another NoSQL database containing visit infomation including who went and what they ordered. The project implements CRUD by letting you create both visits and restaurants, read menus and visit information, update restaurant notes, and delete restaurants. 

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py                  # Main Flask application — routes and app logic
├── dbCode.py                    # Database helper functions (MySQL connection + queries)
├── creds.py                     # Credentials file
├── templates/
│   ├── home.html                # Landing page with general information on each restaurant
│   ├── add_restaurant.html      # Page to allow the creation of a restaurant by providing name, city, food type, price, and notes
│   ├── add_visit.html           # Page to allow the recording of visits by providing the restaurant, rating, who went and what they ordered
│   ├── delete_restaurant.html   # Page to allow the deletion of a restaurant by selecting the restaurant to be deleted
│   ├── display_visit.html       # Page to view all visits for a selected restaurant showing information for each visit
│   ├── update_notes.html        # Page to update the notes attached to restaurants
│   ├── view_menu.html           # Page to view menu items for selected restaurant
├── .gitignore                   # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://98.93.83.190:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

My relational database had two tables that were used, with one storing restaurants and the other storing the menu items for the restaurants. The tables were connected with a restaurant_id connecting the items to their respective restaurants. 
<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->

**Example:**

- `restaurants` — stores general restaurant information like name, cuisine, price, location, if it has been visited, and notes; primary key is `restaurant_id`
- `menu_items` — stores menu items for restuarants with information like their names and prices; foreign key links to `restaurants`

The JOIN query used in this project: joins restaurants and menu_items using restaurant_id to display all menu_items and the restaurant name for a given restaurant. 

### DynamoDB

My DynamoDB table is created with the partition key being Restaurant, which is a string that stores the name of the restaurant. It then has a sort key of VisitID, which is a string of the current time as that should stay unique, so that it can store multiple visits for each restaurant. This is then used to store values such as the rating of the restaurant, who went, what each person ordered, and the rating of each item ordered. This connects to the app by allowing the visits of each restaurant recorded in the database to be viewed.
<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `ProjectOne`
- **Partition key:** `Restaurant`
- **Sort key:** `VisitID`
- **Used for:** Storing visits for each restaurant with information such as the restaurant, rating, who went, and what each person ordered.

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/add-restaurant` | Contains text boxes to create a restaurant for the SQL table |
| Create    | `/add-visit` | Creates a visit for the DynamoDB table that can have any number of people and items ordered for each visit |
| Read      | `/display-visit` | Displays all visits from the restaurant selected in the drop down|
| Read      | `/view-menu` | Views all menu items (included in the table) from the  restaurant selected in the drop down|
| Update    | `/update-notes` | Updates the notes for the restaurant with the text entered |
| Delete    | `/delete-restaurant` | Deletes the selected restaurant from the SQL table |

---

## Challenges and Insights

The hardest part for me was working with html and understanding both how to set up the webpages as well as how those pages then interact with python code. I learned a lot about the different formats that the data can be read from the webpages and how those have to be handled with python to then interact with both SQL and DynamoDB tables. 

---

## AI Assistance

I used ChatGPT with assistance on html code for many pages such as instances of dropdown menus or text boxes being added from buttons. I also used it to handle some data reading from the html using python. All instances of use are mentioned in the code files where it was used. Some updates were made to the AI code to ensure that it works and functions how I want but the base structure of those parts are from ChatGPT and then edited and made functional by me. I also used ChatGPT throughout when dealing with errors or error messages but this often was more to understand error messages rather than rewriting the code using AI. 
<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
