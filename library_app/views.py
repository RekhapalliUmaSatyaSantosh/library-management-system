from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, User, IssueBook, IssueRequest
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from datetime import date, timedelta
#Create your views here.

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            return render(request,"signup.html",{"error": "Passwords do not match"})
        if User.objects.filter(email=email).exists():
            return render(request,"signup.html",{"error": "Email already registered"})
        User.objects.create(username=username,email=email,password=make_password(password),role="user")
        return redirect("login")
    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request,"Email is not registered. Please sign up first.")
            return redirect("signup")
        if not check_password(password, user.password):
            messages.error(request, "Incorrect password")
            return redirect("login")
        request.session["userid"] = user.userid
        request.session["email"] = user.email
        request.session["username"] = user.username
        request.session["role"] = user.role
        if user.role == "admin":
            return redirect("admin_dashboard")
        else:
            return redirect("user_dashboard")
    return render(request, "login.html")
def admin_dashboard(request):
    if request.session.get("role") != "admin":
        return redirect("login")
    return render(request, "admin_dashboard.html")


def user_dashboard(request):
    if request.session.get("role") != "user":
        return redirect("login")
    return render(request, "user_dashboard.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "Email is not registered.")
            return redirect("forgot_password")
        request.session["reset_email"] = email
        return redirect("reset_password")
    return render(request, "forgot_password.html")

def reset_password(request):
    email = request.session.get("reset_email")
    if not email:
        messages.error(request, "Please enter your email first.")
        return redirect("forgot_password")
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")
        user = User.objects.get(email=email)
        user.password = make_password(password)
        user.save()
        del request.session["reset_email"]
        messages.success(request, "Password reset successfully. Please login.")
        return redirect("login")
    return render(request, "reset_password.html")

def add_book(request):
    if request.session.get("role") != "admin":
        return redirect("login")
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        publisher = request.POST.get("publisher")
        quantity = request.POST.get("quantity")
        Book.objects.create(title=title,author=author,publisher=publisher,quantity=quantity)
        return redirect("book_list")
    return render(request, "add_book.html")

def book_list(request):
    if not request.session.get("userid"):
        return redirect("login")
    books = Book.objects.all()
    return render(request, "book_list.html", {"books": books})

def update_book(request, id):
    if request.session.get("role") != "admin":
        return redirect("login")
    book = get_object_or_404(Book, bookid=id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.publisher = request.POST.get("publisher")
        book.quantity = request.POST.get("quantity")
        book.save()
        return redirect("book_list")
    return render(request, "update_book.html", {"book": book})

def delete_book(request, id):
    if request.session.get("role") != "admin":
        return redirect("login")
    book = get_object_or_404(Book, bookid=id)
    book.delete()
    return redirect("book_list")

def search_book(request):
    if not request.session.get("userid"):
        return redirect("login")
    query = request.GET.get("query", "")
    if query:
        books = (Book.objects.filter(title__icontains=query)| Book.objects.filter(author__icontains=query)| Book.objects.filter(publisher__icontains=query))
    else:
        books = Book.objects.none()
    return render(request, "search_book.html", {"books": books,"query": query})

def add_user(request):
    if request.session.get("role") != "admin":
        return redirect("login")
    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        if User.objects.filter(email=email).exists():
            return render(request,"add_user.html",{"error":"Email already exists"})
        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role="user"
        )
        messages.success(request,"User added successfully")
        return redirect("user_list")
    return render(request,"add_user.html")

def user_list(request):
    if request.session.get("role") != "admin":
        return redirect("login")
    users=User.objects.filter(role="user")
    return render(request,"user_list.html",{"users":users})

def update_user(request,id):
    if request.session.get("role") != "admin":
        return redirect("login")
    user = get_object_or_404(User,userid=id)
    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        if User.objects.filter(email=email).exclude(userid=id).exists():
            return render(request,"update_user.html",{"user":user,"error":"Email already registered"})
        user.username=username
        user.email=email
        if password:
            user.password=make_password(password)
        user.save()
        messages.success(request,"User updated successfully")
        return redirect("user_list")
    return render(request,"update_user.html",{"user":user})

def delete_user(request,id):
    if request.session.get("role") != "admin":
        return redirect("login")
    user=get_object_or_404(User,userid=id)
    user.delete()
    return redirect("user_list")

def issue_book(request):
    if request.session.get("role") != "admin":
        return redirect("login")
    users = User.objects.filter(role="user")
    books = Book.objects.filter(quantity__gt=0)
    if request.method == "POST":
        userid = request.POST.get("userid")
        bookid = request.POST.get("bookid")
        duedate = request.POST.get("duedate")
        user = get_object_or_404(User, userid=userid)
        book = get_object_or_404(Book, bookid=bookid)
        if book.quantity <= 0:
            messages.error(request, "Book is not available.")
            return redirect("issued_books")
        IssueBook.objects.create(user=user,book=book,duedate=duedate)
        book.quantity -= 1
        book.save()
        messages.success(request, "Book issued successfully.")
        return redirect("issued_books")
    return render(request, "issue_book.html", {"users": users,"books": books})

def return_book(request, id):
    if request.session.get("role") != "admin":
        return redirect("login")
    issue = get_object_or_404(IssueBook, issueid=id)
    if issue.returndate:
        messages.error(request, "This book has already been returned.")
        return redirect("issued_books")
    today = date.today()
    issue.returndate = today
    if today > issue.duedate:
        late_days = (today - issue.duedate).days
        issue.fine = late_days * 10
    else:
        issue.fine = 0
    issue.save()
    book = issue.book
    book.quantity += 1
    book.save()
    messages.success(request, "Book returned successfully.")
    return redirect("issued_books")

def issued_books(request):
    if request.session.get("role") != "admin":
        return redirect("login")
    issues = IssueBook.objects.select_related("user", "book").all()
    return render(request, "issued_books.html", {"issues": issues})

def my_issued_books(request):
    if request.session.get("role") != "user":
        return redirect("login")
    userid = request.session.get("userid")
    user = get_object_or_404(User, userid=userid)
    issues = IssueBook.objects.filter(user=user).select_related("book")
    return render(request, "my_issued_books.html", {"issues": issues})

def request_issue(request, id):
    if request.session.get("role") != "user":
        return redirect("login")
    userid = request.session.get("userid")
    user = get_object_or_404(User, userid=userid)
    book = get_object_or_404(Book, bookid=id)
    if book.quantity <= 0:
        messages.error(request, "This book is currently not available.")
        return redirect("book_list")
    existing_request = IssueRequest.objects.filter(user=user,book=book,status="Pending").exists()
    if existing_request:
        messages.warning(request,"You have already requested this book.")
        return redirect("book_list")
    IssueRequest.objects.create(user=user,book=book)
    messages.success(request,"Book issue request sent to admin.")
    return redirect("book_list")

def issue_requests(request):
    if request.session.get("role") != "admin":
        return redirect("login")
    requests = IssueRequest.objects.select_related("user","book").filter(status="Pending")
    return render(request,"issue_requests.html",{"requests": requests})

def approve_issue_request(request, id):
    if request.session.get("role") != "admin":
        return redirect("login")
    issue_request = get_object_or_404(IssueRequest,requestid=id)
    book = issue_request.book
    if book.quantity <= 0:
        messages.error(request,"Book is no longer available.")
        return redirect("issue_requests")
    IssueBook.objects.create(user=issue_request.user,book=book,duedate=date.today() + timedelta(days=14))
    book.quantity -= 1
    book.save()
    issue_request.status = "Approved"
    issue_request.save()
    messages.success(request,"Issue request approved and book issued.")
    return redirect("issue_requests")

def reject_issue_request(request, id):
    if request.session.get("role") != "admin":
        return redirect("login")
    issue_request = get_object_or_404(IssueRequest,requestid=id)
    issue_request.status = "Rejected"
    issue_request.save()
    messages.success(request,"Issue request rejected.")
    return redirect("issue_requests")