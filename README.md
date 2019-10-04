# Rent-books-app

[![Build Status](https://travis-ci.org/kafuuma/Rent-books-app.svg?branch=develop)](https://travis-ci.org/kafuuma/Rent-books-app)

Book Rent app is an application for borrowing books from book store

The application is hosted on AWS here [Go](http://ec2-54-88-110-193.compute-1.amazonaws.com/graphql/)

How the application works

- Create a customer request

```
mutation createCustomer{
  createCustomer(username:"arkafuuma"){
    customer{
      id
    }
    errors
    success
  }
}

```

- Request to create a book

```
mutation CreateBook{
  createBook(title:"How to learn C++ in 24 hrs", totalNumber:5 bookKind:fiction){
    book{
      id
      title
      totalNumber
      totalRented
      bookKind
    }
    errors
    success
  }
}
```

- Request to get all books

```
query getAllBooks{
  books{
    id
    title
    totalNumber
    totalRented
    borrowedbooksSet{
      id
      returnedOn
      borrower{
        id
        username
      }
    }
  }
}

```

- Request to get all customers

```
query getAllcustomers{
  customers{
    id
    username
    borrowedbooksSet{
      id
      books{
        id
        title
      }
    }
  }
}

```

- Borrow books

```
- The number of book ids should match the items in the list. Each item
in the list is the number of days correspond to book id in the book id
list

mutation BorrowBooks{
  lendBooks(borrowerId:1, booksIds:[1,2,5],rentedDays:[5,5,6]){
    borrowedBooks{
      id
      books{
        id
        title
        totalNumber
        totalRented
      }
    }
    price
    success
    errors
  }
}

```

# Project requirements

- Django
- python
- graphene-python
- graphene-django
- Docker
- Docker-compose

## PROJECT SETUP

## PROJECT SETUP WITH DOCKER

```
- Install Docker and Docker-compose
- Run Server
  docker-compose -f docker/docker-compose.yml up --build -d


- Run tests
  docker-compose -f docker/docker-compose.yml exec books tox
```
