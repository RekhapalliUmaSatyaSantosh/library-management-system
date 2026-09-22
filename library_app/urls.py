from django.urls import path
from . import views

urlpatterns=[
    path("signup", views.signup_view, name="signup"),
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("forgot-password", views.forgot_password, name="forgot_password"),
    path("reset-password", views.reset_password, name="reset_password"),
    path('add_book',views.add_book,name='add_book'),
    path('book_list',views.book_list,name='book_list'),
    path("admin-dashboard", views.admin_dashboard, name="admin_dashboard"),
    path("user-dashboard", views.user_dashboard, name="user_dashboard"),
    path("update_book/<int:id>", views.update_book, name="update_book"),
    path("delete_book/<int:id>", views.delete_book, name="delete_book"),
    path("search-book", views.search_book, name="search_book"),
    path("add-user",views.add_user,name="add_user"),
    path("view-users",views.user_list,name="user_list"),
    path("update-user/<int:id>",views.update_user,name="update_user"),
    path("delete-user/<int:id>",views.delete_user,name="delete_user"),
    path("issue-book/", views.issue_book, name="issue_book"),
    path("issued-books/", views.issued_books, name="issued_books"),
    path("return-book/<int:id>/", views.return_book, name="return_book"),
    path("my-issued-books/", views.my_issued_books, name="my_issued_books"),
    path("request-issue/<int:id>/",views.request_issue,name="request_issue"),
    path("issue-requests/",views.issue_requests,name="issue_requests"),
    path("approve-issue-request/<int:id>/",views.approve_issue_request,name="approve_issue_request"),
    path("reject-issue-request/<int:id>/",views.reject_issue_request,name="reject_issue_request"),
]