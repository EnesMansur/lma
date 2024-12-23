import datetime
from math import ceil

from django.db import connections
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from book.models import Book, BookEdition, FormatEnum
from .serializers import BookSerializer, BookListSerilazer, BookBulkDummySerilazer, BookEditionSerializer
from rest_framework import serializers as rest_serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from api.views import CustomResponse
from drf_yasg.utils import swagger_auto_schema
from swagger_schema import swagger_schema_init
from django.db import transaction
from lma.utils import generate_random
from rest_framework import status
import secrets


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @swagger_auto_schema(tags=['books'])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = serializer.data
        response_data['id'] = serializer.instance.id
        return Response(response_data, status=status.HTTP_201_CREATED)


class BookListViewSet(APIView):
    @swagger_auto_schema(**swagger_schema_init["book_list"])
    def get(self, request):
        serializer_class = BookListSerilazer
        response_data_list = []
        detail = "ok"
        total_page = 0
        try:
            get_data = request.GET
            serializer = serializer_class(data=get_data)
            if not serializer.is_valid():
                raise rest_serializers.ValidationError(serializer.errors)
            print(get_data)
            page = get_data.get("page")
            limit = get_data.get("limit")
            title = get_data.get("title")
            author = get_data.get("author")
            isbn = get_data.get("isbn")
            start_date = get_data.get("start_date")
            end_date = get_data.get("end_date")

            if not page or (page and not str(page).isdigit()):
                page = 0
            page = int(page)
            if not limit or (limit and not str(limit).isdigit()):
                limit = 100
            limit = int(limit)
            if limit > 100:
                limit = 100

            sql_where = ""
            if title:
                sql_where += f" and b.title ilike '{title}'"

            if author:
                sql_where += f" and b.author ilike '{author}'"

            if isbn:
                sql_where += f" and b.isbn='{isbn}'"

            if start_date:
                sql_where += f" and b.publication_date>={start_date}"

            if end_date:
                sql_where += f" and b.publication_date<={end_date}"

            sql = f"""select count(*)
                      FROM book_book b
                      WHERE true 
                      {sql_where}
                   """

            cursor = connections["default"].cursor()

            cursor.execute(sql)
            total_count = cursor.fetchone()[0] or 0

            if limit >= total_count:
                total_page = 1
            else:
                total_page = ceil(total_count / limit)

            skip = page * limit
            if skip < 0:
                skip = 0

            if skip >= total_count:
                total_page = 0

            offset_sql = f" offset {skip} limit {limit}"

            status_code = status.HTTP_200_OK

            sql = f"""
            SELECT to_char(b.created_at, 'YYYY-MM-DD HH24:MI')
            ,to_char(b.publication_date, 'YYYY-MM-DD HH24:MI')
            ,b.title
            ,b.author
            ,b.isbn
            ,b.genre
            ,b.quantity
            ,b.id
            FROM book_book b
            WHERE true
            {sql_where}
            ORDER BY b.created_at DESC
            {offset_sql}
            """

            cursor.execute(sql)
            data = cursor.fetchall()

            if data:
                for x in data:
                    response_data_list.append({
                        "created_at": x[0],
                        "publication_date": x[1],
                        "title": x[2],
                        "author": x[3],
                        "isbn": x[4],
                        "genre": x[5],
                        "quantity": x[6],
                        "id": x[7]
                    })

        except rest_serializers.ValidationError as exc:
            response_data_list = {
                "result": False,
                "data": None,
                "detail": str(exc),
                "total_page": 0
            }
            status_code = status.HTTP_400_BAD_REQUEST

        except Exception as exc:
            print(exc)
            """
            sentry olsaydi
            capture_exception(exc)
            DB den gelen hatayi response olarak vermeyiz. 
            hatalari map lemek gerek cilent tarafi ile birlikte.
            """

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = str(exc)

        return CustomResponse(
            data=response_data_list,
            message=detail,
            status_code=status_code,
            total_page=total_page
        )


class BookBulkDummyViewSet(APIView):
    @swagger_auto_schema(**swagger_schema_init["book_bulk_create"])
    def post(self, request):
        serializer_class = BookBulkDummySerilazer
        response_data_list = []
        detail = "ok"
        try:
            post_data = request.data
            serializer = serializer_class(data=post_data)
            if not serializer.is_valid():
                raise rest_serializers.ValidationError(serializer.errors)

            bulk_size = post_data.get("bulk_size")
            with transaction.atomic():
                pre_book = []
                for i in range(bulk_size):
                    _title = generate_random(length=32, only_numbers=False)
                    _author = generate_random(length=8, only_numbers=False)
                    _isbn = generate_random(length=13, only_numbers=False)
                    book = Book(
                        title=_title,
                        author=_author,
                        publication_date=datetime.datetime.now(),
                        isbn=_isbn
                    )
                    pre_book.append(book)

                # bulk create
                result = Book.objects.bulk_create(pre_book)
                response_data_list.extend([b.id for b in result])
                status_code = status.HTTP_200_OK

        except Exception as exc:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = str(exc)

        return CustomResponse(
            data=response_data_list,
            message=detail,
            status_code=status_code
        )


class EditionBookListViewSet(ModelViewSet):
    queryset = BookEdition.objects.all()
    serializer_class = BookEditionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['book__title', 'book__author', 'book__isbn']
    ordering_fields = ['book__publication_date']
    ordering = ['book__publication_date']  # default
    tags = ["edition"]

    @swagger_auto_schema(tags=['edition'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['edition'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['edition'])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = serializer.data
        response_data['id'] = serializer.instance.id
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=['edition'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=['edition'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class EditionBookBulkDummyViewSet(APIView):
    @swagger_auto_schema(**swagger_schema_init["edition_bulk_create"])
    def post(self, request):
        serializer_class = BookBulkDummySerilazer
        response_data_list = []
        detail = "ok"
        try:
            post_data = request.data
            serializer = serializer_class(data=post_data)
            if not serializer.is_valid():
                raise rest_serializers.ValidationError(serializer.errors)

            bulk_size = post_data.get("bulk_size")
            with transaction.atomic():
                pre_book_edition = []
                for i in range(bulk_size):
                    _edition_number = generate_random(length=10)
                    _format = secrets.choice(FormatEnum.choose_list())[0]
                    random_book = Book.objects.order_by('?').first()
                    book_edition = BookEdition(
                        book=random_book,
                        edition_number=_edition_number,
                        published_year=2024,
                        quantity=2,
                        format=_format
                    )
                    pre_book_edition.append(book_edition)

                # bulk create
                result = Book.objects.bulk_create(pre_book_edition)
                response_data_list.extend([b.id for b in result])
                status_code = status.HTTP_200_OK

        except Exception as exc:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = str(exc)

        return CustomResponse(
            data=response_data_list,
            message=detail,
            status_code=status_code
        )
