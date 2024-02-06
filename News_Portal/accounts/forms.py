from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Импортировали класс формы, который предоставляет allauth, а также модель групп
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.core.mail import EmailMultiAlternatives, mail_admins


# Форма, создания нового пользователя.
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User  # работает с таблицей auth_user в db.sqlite3
        # Поля
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


# В кастомизированном классе формы, в котором мы хотим добавлять пользователя в
# группу, нужно переопределить только метод save(), который выполняется при
# успешном заполнении формы регистрации.
class CustomSignupForm(SignupForm):
    """
    В первой строке метода мы вызываем этот же метод класса-родителя,
    чтобы необходимые проверки и сохранение в модель User были выполнены.
    Далее мы получаем объект модели группы с названием common users.
    И в следующей строке мы добавляем нового пользователя в эту группу.
    Обязательным требованием метода save() является возвращение объекта модели
    User по итогу выполнения функции.
    """

    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="Guest")
        user.groups.add(common_users)

        subject = 'Добро пожаловать!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        return user
