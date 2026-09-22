from django.db import models

#Create Your models here

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default="user")
    def __str__(self):
        return self.username
    
class Book(models.Model):
    bookid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150)
    quantity = models.IntegerField()
    def __str__(self):
        return self.title
    
class IssueBook(models.Model):
    issueid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    issuedate = models.DateField(auto_now_add=True)
    duedate = models.DateField()
    returndate = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    def __str__(self):
        return f"{self.book.title} - {self.user.username}"
    
class IssueRequest(models.Model):
    requestid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    requestdate = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20,default="Pending")
    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.status}"