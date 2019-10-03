

create_customer_string = """
    mutation createCustomer{{
    createCustomer(username:"{username}"){{
        customer{{
        id
        }}
        errors
        success
    }}
    }}
"""


create_book_string = """
    mutation CreateBook{{
    createBook(title:"{title}"
    totalNumber:{total_number}
    bookKind:{book_kind}){{
    book{{
      id
      title
      totalNumber
      totalRented
      bookKind
    }}
    errors
    success
  }}
}}

"""


borrow_books_string = """
    mutation BorrowBooks{{
    lendBooks(
        borrowerId:{customer_id}
        booksIds:{books_ids}
        rentedDays:{days}){{
    borrowedBooks{{
      id
      books{{
        id
        title
        totalNumber
        totalRented
      }}
    }}
    price
    success
    errors
  }}
}}
"""


query_book_string = """
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
"""

query_cutomer_string = """
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
"""
