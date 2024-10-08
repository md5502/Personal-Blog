# Personal Blog

This project is a simple personal blog that allows you to write and publish articles. The blog has two main sections: a guest section accessible to everyone and an admin section accessible only to the blog's owner.

## Features

### Guest Section

- **Home Page**: Displays a list of all published articles with a title, publication date, and a short description.
- **Article Page**: Displays the full content of a selected article along with its publication date.

### Admin Section

- **Dashboard**: Displays a list of all articles with options to add new articles, edit existing ones, or delete articles.
- **Add Article Page**: Contains a form for creating and publishing a new article with fields for the title, content, and publication date.
- **Edit Article Page**: Contains a form for editing an existing article with fields pre-filled with the current title, content, and publication date.

## Technologies Used

- **HTML**: Used to structure the content of the web pages.
- **CSS**: Used to style the web pages.

## How to Use

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/your-username/personal-blog.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd personal-blog
   ```

3. **Open in a Browser**:
   - Open the `index.html` file in your preferred web browser to view the guest section.
   - Open the `dashboard.html` file in your preferred web browser to access the admin section.

4. **Edit and Publish Articles**:
   - Use the `Add Article` page to create new articles.
   - Use the `Edit Article` page from the `Dashboard` to modify existing articles.

## Project Structure

```plaintext
/Personal-Blog/
.
├── app
│   ├── config.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── permissions.py
│   ├── routes
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── blog.py
│   │   ├── __init__.py
│   │   └── user.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   ├── templates
│   │   ├── admin
│   │   │   ├── add-article.html
│   │   │   ├── article_list.html
│   │   │   ├── base.html
│   │   │   ├── dashboard.html
│   │   │   ├── delete_article.html
│   │   │   └── edit-article.html
│   │   ├── auth
│   │   │   ├── base.html
│   │   │   ├── login.html
│   │   │   └── sign_up.html
│   │   ├── blog
│   │   │   ├── article.html
│   │   │   ├── base.html
│   │   │   └── home.html
│   │   └── user
│   │       ├── base.html
│   │       ├── create.html
│   │       ├── delete.html
│   │       ├── detail.html
│   │       └── list.html
│   └── utils.py
├── instance
│   └── database.db
├── LICENSE

├── README.md
├── run.py
└── tree.txt

15 directories, 49 files

```

## Future Improvements

- **JavaScript Integration**: Add interactivity with JavaScript, such as form validation and dynamic content loading.
- **Backend Integration**: Connect the blog to a backend to store articles in a database.
- **User Authentication**: Implement a login system to secure the admin section.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

For any inquiries or suggestions, feel free to contact me at [your-email@example.com](mailto:your-email@example.com).

---

Feel free to adjust the content, particularly the sections on future improvements and contact information, to match your needs.
