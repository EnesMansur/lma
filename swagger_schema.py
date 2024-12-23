from book.api.serializers import BookListSerilazer, BookBulkDummySerilazer, BookEditionSerializer

swagger_schema_init = {
    "book_list": {
        "tags": ["books"],
        "query_serializer": BookListSerilazer,
        "responses": {
            '200': """{
                "result": True,
                "message": "ok",
                "data": [...]
            }""",
            '400': "Bad Request or known bug",
            '500': "Unknown bug or system errors",
        },
        "operation_description": "List of all books via SQL Pagination",
        "operation_summary": "List of all books via SQL Pagination",
        "operation_id": "list_all_books"
    },
    "book_bulk_create": {
        "tags": ["books"],
        "request_body": BookBulkDummySerilazer,
        "responses": {
            '200': """{
                "result": True,
                "message": "ok",
                "data": [...]
            }""",
            '400': "Bad Request or known bug",
            '500': "Unknown bug or system errors",
        },
        "operation_description": "Dummy data creation as bulk",
        "operation_summary": "create bulk data for test",
        "operation_id": "book_bulk_create"
    },
    "edition_bulk_create": {
        "tags": ["edition"],
        "request_body": BookBulkDummySerilazer,
        "responses": {
            '200': """{
                "result": True,
                "message": "ok",
                "data": [...]
            }""",
            '400': "Bad Request or known bug",
            '500': "Unknown bug or system errors",
        },
        "operation_description": "Dummy data for edition creation as bulk",
        "operation_summary": "create bulk data for test",
        "operation_id": "edition_bulk_create"
    }

}
