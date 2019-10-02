

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
    createBook(title:"{title}", totalNumber:{total_number}){{
    book{{
      id
      title
      totalNumber
      totalRented
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
        numberOfDays:{days}){{
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
