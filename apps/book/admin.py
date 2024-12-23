from django.contrib import admin

from book.models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "isbn"]
    search_fields = ["title", "author", "isbn"]


class BookEditionAdmin(admin.ModelAdmin):
    list_display = ["id", "book","edition_number", "published_year", "quantity", "format"]
    raw_id_fields = ("book",)
    search_fields = ["book_title", "book_author", "book_isbn"]
    list_select_related = ["book"]


admin.site.register(Book, BookAdmin)
admin.site.register(BookEdition, BookEditionAdmin)
