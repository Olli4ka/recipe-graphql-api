# 🥗 Recipe GraphQL API

A GraphQL API for managing recipes, ingredients, categories, reviews, and favorites.

---

The project is built with Django and Graphene-Django and uses PostgreSQL as the database. 
Authentication is implemented with JWT, while Docker Compose provides a production-oriented 
setup with Gunicorn and Nginx.

### Backend

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)
![GraphQL](https://img.shields.io/badge/GraphQL-API-E10098?logo=graphql&logoColor=white)
![Graphene](https://img.shields.io/badge/Graphene--Django-3.2.3-E10098?logo=graphql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?logo=jsonwebtokens&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-12.3.0-3776AB?logo=python&logoColor=white)

### Infrastructure

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-26.2.0-499848?logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-1.29-009639?logo=nginx&logoColor=white)

### Development & Testing

![Pytest](https://img.shields.io/badge/Pytest-9.1.1-0A9EDC?logo=pytest&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-7.15.4-43B02A?logo=coverage&logoColor=white)
![Factory Boy](https://img.shields.io/badge/Factory_Boy-3.3.3-3776AB?logo=python&logoColor=white)
![Black](https://img.shields.io/badge/Black-26.5.1-000000?logo=python&logoColor=white)
![isort](https://img.shields.io/badge/isort-9.0.1-3776AB?logo=python&logoColor=white)


![Test Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen)
![Tests](https://img.shields.io/badge/tests-62%20passed-brightgreen)

---

## Features

- GraphQL-only API
- JWT authentication
- Custom user model with avatar and bio
- Recipe management
- Categories and ingredients
- Recipe ingredients with amount and measurement units
- Cooking steps with ordering
- Reviews with ratings from 1 to 5
- Favorites
- Recipe filtering, searching, ordering, and pagination
- Django Admin for data management
- Image uploads for recipes and user avatars
- PostgreSQL database
- Docker Compose setup
- Gunicorn application server
- Nginx reverse proxy
- Static and media files served through Docker volumes
- Automated tests with pytest

---

## Project Structure

```text
recipe-graphql-api/
├── src/
│   ├── app_recipe/
│   │   ├── admin/                    #Django Admin configuration for application models
│   │   │   ├── category.py
│   │   │   ├── favorite.py
│   │   │   ├── ingredient.py
│   │   │   ├── recipe.py
│   │   │   ├── recipe_ingredient.py
│   │   │   ├── review.py
│   │   │   ├── step.py
│   │   │   └── user.py
│   │   │
│   │   ├── graphql/                  #GraphQL schema, types, queries, mutations, inputs, enums, and utility functions
│   │   │   ├── enums.py
│   │   │   ├── inputs.py
│   │   │   ├── mutations.py
│   │   │   ├── queries.py
│   │   │   ├── schema.py
│   │   │   ├── types.py
│   │   │   └── utils.py
│   │   │
│   │   ├── migrations/
│   │   │
│   │   ├── models/                   #Django models for users, recipes, categories, ingredients, steps, reviews, and favorites
│   │   │   ├── category.py
│   │   │   ├── favorite.py
│   │   │   ├── ingredient.py
│   │   │   ├── recipe.py
│   │   │   ├── recipe_ingredient.py
│   │   │   ├── review.py
│   │   │   ├── step.py
│   │   │   └── user.py
│   │   │
│   │   └── tests/                    #pytest test suite covering authentication, models, queries, and mutations
│   │       ├── conftest.py
│   │       ├── factories.py
│   │       ├── test_auth.py
│   │       ├── test_models.py
│   │       ├── test_mutations.py
│   │       └── test_queries.py
│   │
│   ├── config/                       #Django project configuration, settings, URLs, ASGI, and WSGI    
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── manage.py
│
├── nginx/                            #Nginx reverse proxy configuration
│   └── nginx.conf
│
├── Dockerfile                        #Docker image for the Django application
├── docker-compose.yml                #Docker services for PostgreSQL, Django/Gunicorn, and Nginx
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .env.example
├── .env.docker
├── .dockerignore
├── .gitignore
└── README.md
```

---

## Installation & Setup

### Prerequisites

Before running the project, install the following software:

* Python 3.12+ (for local development)
* Git
* Docker Desktop (includes Docker Compose)


### 1. Clone the repository
```bash
git clone https://github.com/Olli4ka/recipe-graphql-api.git
cd recipe-graphql-api
```


### 2. Configure environment variables
Create a local environment file based on .env.example.

macOS and Linux
```bash
cp .env.example .env
```
Windows PowerShell
```bash
Copy-Item .env.example .env
```
Windows Command Prompt
```bash
copy .env.example .env
```

Fill in the required values inside .env.

Example:
```env
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=recipe_graphql_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Docker Compose uses a separate `.env.docker` file for container configuration.

> **Important:** Never commit `.env` files containing real secrets or passwords.


### 3. Build and start the containers

Build the application image and start all services.
```bash
docker compose up --build
```

Run containers in the background:
```bash
docker compose up -d --build
```

Check that all containers are running:
```bash
docker compose ps
```

Expected services:

| Service   | Description                                  |
| --------- | -------------------------------------------- |
| **web**   | Django application served by Gunicorn        |
| **db**    | PostgreSQL database                          |
| **nginx** | Reverse proxy serving static and media files |


### 4. Apply database migrations

Run Django migrations inside the `web` container.
```bash
docker compose exec web python manage.py migrate
```


### 5. Create a Django superuser

Create an administrator account for Django Admin.
```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to enter:
* username
* email
* password


### 6. Collect static files

Collect Django static files into the Docker volume used by Nginx.
```bash
docker compose exec web python manage.py collectstatic --noinput
```

This command copies all static assets into `/app/staticfiles`, where Nginx serves them.


### 7. Access the application

After all containers are running, open:

| URL                         | Description                                                     |
| --------------------------- | --------------------------------------------------------------- |
| `http://localhost/graphql/` | GraphiQL interface for executing GraphQL queries and mutations. |
| `http://localhost/admin/`   | Django Admin panel.                                             |

GraphiQL is enabled in development mode and supports schema exploration, JWT headers, queries, and mutations.


### Docker volumes

The project uses Docker volumes to persist application data.

| Volume          | Purpose                                        |
| --------------- | ---------------------------------------------- |
| `postgres_data` | PostgreSQL database files.                     |
| `static_volume` | Collected Django static files served by Nginx. |
| `media_volume`  | Uploaded recipe images and user avatars.       |

Uploaded media files remain available after container restarts because they are stored in `media_volume`.


### Stop the application

Stop running containers:
```bash
docker compose down
```

Stop containers **and remove Docker volumes**:
```bash
docker compose down -v
```

> Removing volumes deletes the PostgreSQL database and uploaded media files stored in Docker volumes.


### Quick Check

Open GraphiQL:

```graphql
query {
  __typename
}
```

Expected response:

```json
{
  "data": {
    "__typename": "Query"
  }
}
```

---

## GraphQL API

The project provides a GraphQL-only API powered by Graphene-Django.

### GraphQL Endpoint

The GraphQL endpoint is available at:
```text
http://localhost/graphql/
```

GraphiQL is enabled for interactive API exploration and testing.

The GraphQL schema is organized into separate modules:

- `types.py` — GraphQL object types
- `queries.py` — query resolvers
- `mutations.py` — mutation resolvers
- `inputs.py` — mutation input types
- `enums.py` — GraphQL enums
- `utils.py` — shared GraphQL utilities
- `schema.py` — root GraphQL schema


### Authentication

The API uses JWT (JSON Web Token) authentication.

Authentication mutations are provided by `django-graphql-jwt`.

#### Obtain a token

```graphql
mutation {
  tokenAuth(
    username: "your_username"
    password: "your_password"
  ) {
    token
    refreshToken
  }
}
```

The response contains an access token and a refresh token:

```json
{
  "data": {
    "tokenAuth": {
      "token": "your_access_token",
      "refreshToken": "your_refresh_token"
    }
  }
}
```

Use the access token in the `Authorization` header:

```text
Authorization: JWT <your_access_token>
```

#### Verify a token

```graphql
mutation {
  verifyToken(
    token: "your_access_token"
  ) {
    payload
  }
}
```

#### Refresh a token

```graphql
mutation {
  refreshToken(
    token: "your_refresh_token"
  ) {
    token
    refreshToken
  }
}
```

Protected mutations require an authenticated user.

The current user is determined from the JWT token and is automatically assigned as the author of newly created recipes, reviews, and favorites.

---

## Queries

The API provides queries for retrieving recipes, categories, ingredients, and users.

### Recipes

Retrieve a paginated list of recipes:

```graphql
query {
  recipes(
    limit: 10
    offset: 0
    orderBy: TITLE
  ) {
    totalCount
    hasNextPage
    items {
      id
      title
      slug
      cookingTime
      category {
        name
        slug
      }
      author {
        username
      }
    }
  }
}
```

The `recipes` query supports:

- `category` — filter recipes by category slug
- `author` — filter recipes by username
- `search` — search recipes by title
- `orderBy` — order recipes by a supported field
- `limit` — limit the number of returned recipes
- `offset` — skip a number of recipes


The `orderBy` argument supports ascending and descending ordering:

* `TITLE` - Sort by title in ascending order. 
* `TITLE_DESC` - Sort by title in descending order. 
* `COOKING_TIME` - Sort by cooking time in ascending order. 
* `COOKING_TIME_DESC` - Sort by cooking time in descending order. 
* `CREATED` - Sort by creation date in ascending order. 
* `CREATED_DESC` - Sort by creation date in descending order. 

The response includes:

- `totalCount` — total number of matching recipes
- `hasNextPage` — indicates whether more recipes are available
- `items` — returned recipes

 Get a recipe by slug:

```graphql
query {
  recipe(slug: "creamy-chicken-pasta") {
    id
    title
    slug
    description
    cookingTime
    image

    category {
      name
      slug
    }

    author {
      username
      avatar
    }

    ingredients {
      id
      name
    }

    steps {
      id
      order
      instruction
    }

    reviews {
      id
      rating
      comment
      createdAt
      user {
        username
      }
    }

    favorites {
      id
      createdAt
      user {
        username
      }
    }
  }
}
```

### Categories

Retrieve all categories:

```graphql
query {
  categories {
    id
    name
    slug
  }
}
```

Retrieve a category by slug:

```graphql
query {
  category(slug: "main-dishes") {
    id
    name
    slug
  }
}
```

### Ingredients

Retrieve all ingredients:

```graphql
query {
  ingredients {
    id
    name
  }
}
```

Retrieve an ingredient by name:

```graphql
query {
  ingredient(name: "Chicken") {
    id
    name
  }
}
```

### Users

Retrieve all users:

```graphql
query {
  users {
    id
    username
    avatar
    bio
  }
}
```

Retrieve a user by username:

```graphql
query {
  user(username: "Olivia") {
    id
    username
    avatar
    bio
  }
}
```

---

## Mutations

The API provides mutations for managing recipes, reviews, and favorites.

### Recipes

#### Create a recipe

Create a new recipe for the authenticated user:

```graphql
mutation {
  createRecipe(
    input: {
      title: "Creamy Chicken Pasta"
      description: "Pasta with chicken in a creamy parmesan sauce."
      cookingTime: 30
      categorySlug: "main-dishes"
    }
  ) {
    recipe {
      id
      title
      slug
      description
      cookingTime
      category {
        name
        slug
      }
      author {
        username
      }
    }
  }
}
```

The recipe author is automatically assigned from the authenticated JWT user.

#### Update a recipe

Only the recipe owner can update their recipe:

```graphql
mutation {
  updateRecipe(
    input: {
      slug: "creamy-chicken-pasta"
      title: "Creamy Chicken Pasta with Parmesan"
      cookingTime: 35
    }
  ) {
    recipe {
      id
      title
      slug
      cookingTime
    }
  }
}
```

#### Delete a recipe

Only the recipe owner can delete their recipe:

```graphql
mutation {
  deleteRecipe(
    slug: "creamy-chicken-pasta"
  ) {
    success
    message
  }
}
```


### Reviews

#### Create a review

An authenticated user can leave one review per recipe:

```graphql
mutation {
  createReview(
    input: {
      recipeSlug: "creamy-chicken-pasta"
      rating: 5
      comment: "Absolutely delicious!"
    }
  ) {
    review {
      id
      rating
      comment
      createdAt
      user {
        username
      }
    }
  }
}
```

The rating must be between **1 and 5**.

A user cannot create more than one review for the same recipe.

#### Update a review
Users can update their own review:

```graphql
mutation {
  updateReview(
    input: {
      recipeSlug: "creamy-chicken-pasta"
      rating: 4
      comment: "Very tasty and easy to make."
    }
  ) {
    review {
      id
      rating
      comment
      createdAt
    }
  }
}
```

#### Delete a review

Users can delete their own review:

```graphql
mutation {
  deleteReview(
    input: {
      recipeSlug: "creamy-chicken-pasta"
    }
  ) {
    success
    message
  }
}
```


### Favorites

#### Add a recipe to favorites

An authenticated user can add a recipe to their favorites:

```graphql
mutation {
  createFavorite(
    input: {
      recipeSlug: "creamy-chicken-pasta"
    }
  ) {
    favorite {
      id
      createdAt
      recipe {
        title
        slug
      }
      user {
        username
      }
    }
  }
}
```

A recipe cannot be added to the same user's favorites more than once.

#### Remove a recipe from favorites

```graphql
mutation {
  deleteFavorite(
    input: {
      recipeSlug: "creamy-chicken-pasta"
    }
  ) {
    success
    message
  }
}
```


### Authorization

The following operations require JWT authentication:

| Operation | Authentication | Ownership |
|-----------|----------------|-----------|
| Create recipe | Required | — |
| Update recipe | Required | Recipe owner |
| Delete recipe | Required | Recipe owner |
| Create review | Required | — |
| Update review | Required | Review author |
| Delete review | Required | Review author |
| Add favorite | Required | — |
| Remove favorite | Required | Favorite owner |

Unauthenticated users can access public queries but cannot perform protected mutations.

---

## Testing

The project uses **pytest** and **pytest-django** for automated testing.

The test suite covers:

- authentication and JWT
- Django models
- GraphQL queries
- GraphQL mutations
- authorization and ownership rules
- recipe management
- reviews
- favorites

### Test Suite

Run all tests with:
```bash
pytest
```

For verbose output:
```bash
pytest -v
```

Run tests inside the Docker container:
```bash
docker compose exec web pytest
```

### Test Coverage

The project has **97% test coverage**.

Generate a coverage report:
```bash
pytest --cov=app_recipe
```

Generate a detailed terminal report:
```bash
pytest --cov=app_recipe --cov-report=term-missing
```

Generate an HTML coverage report:
```bash
pytest --cov=app_recipe --cov-report=html
```

The HTML report will be generated in the `htmlcov/` directory.

### Test Results

Current test suite:
```text
62 passed
97% coverage
```

---

## Django Admin & Media Files

The project includes a customized **Django Admin** interface for managing application data.

### Django Admin

The admin panel provides management interfaces for:
- Users
- Categories
- Ingredients
- Recipes
- Recipe ingredients
- Cooking steps
- Reviews
- Favorites

The admin interface is customized with:
- user-friendly list displays
- filtering and search
- pagination
- recipe image previews
- convenient management of recipe ingredients and cooking steps

Django Admin is available at:
```text
http://localhost/admin/
```

### Media Files

The application supports image uploads for:
* recipe images
* user avatars

Uploaded files are stored in Django's media directory:
```text
media/
├── recipes/
└── avatars/
```

In Docker, media files are stored in the persistent `media_volume`.

Nginx serves uploaded media files through:
```text
/media/
```
This allows uploaded images to remain available after container restarts.

> **Note:** Media files are stored in a Docker volume and are not included in the Git repository.

---

## Docker Architecture

The application is fully containerized using **Docker Compose**.

The project consists of three main services:

```text
                        ┌─────────────────┐
                        │     Client      │
                        │    Browser      │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │      Nginx      │
                        │  Reverse Proxy  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │     Django      │
                        │    Gunicorn     │
                        │   GraphQL API   │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   PostgreSQL    │
                        │    Database     │
                        └─────────────────┘


        ┌──────────────────┐
        │  static_volume   │
        │  Static files    │
        └────────┬─────────┘
                 │
                 ▼
               Nginx


        ┌──────────────────┐
        │   media_volume   │
        │ Uploaded images  │
        └────────┬─────────┘
                 │
                 ▼
               Nginx
```

### Services

| Service | Description |
|---------|-------------|
| **nginx** | Reverse proxy and web server. Serves static and media files and forwards application requests to Django. |
| **web** | Django application running with Gunicorn. Provides the GraphQL API and Django Admin. |
| **db** | PostgreSQL database used for persistent application data. |

### Request Flow

1. The client sends a request to Nginx.
2. Nginx serves static or media files directly when requested.
3. Application requests are forwarded to the Django container.
4. Gunicorn runs the Django application.
5. Django processes GraphQL queries or mutations.
6. PostgreSQL is used for database operations.
7. The response is returned to the client through Nginx.

### Docker Volumes

The application uses named Docker volumes for persistent data:

| Volume | Purpose |
|---------|---------|
| `postgres_data` | PostgreSQL database files. |
| `static_volume` | Django collected static files. |
| `media_volume` | Uploaded recipe images and user avatars. |

Using volumes allows persistent data to survive container restarts.

### Container Communication

The services communicate through the Docker Compose network using service names.

Django connects to PostgreSQL using:
```env
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Nginx connects to Django through the web service:
```env
proxy_pass http://web:8000;
```
This keeps the database and application services internal to the Docker network while Nginx exposes the application to the host.

### Production Stack

The Docker setup uses the following architecture:
```text
Nginx
  ↓
Gunicorn
  ↓
Django + Graphene-Django
  ↓
PostgreSQL
```
Static and uploaded media files are served directly by Nginx from Docker volumes.

---

## Author

**Olga Panayot**

Python Developer focused on backend development with **Django, Django REST Framework, GraphQL, and PostgreSQL**.

This project was created as a portfolio project to practice building a production-style backend application with GraphQL, JWT authentication, automated testing, Docker, and Nginx.

---