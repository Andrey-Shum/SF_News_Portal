from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm
# Create your views here (Создайте свои представления здесь).


# Расширим эту форму, добавив другие значимые поля — электронная почта, имя и
# фамилия нового пользователя.
class SignUp(CreateView):
    model = User  # модель формы, инстанс которой будет создавать дженерик;
    form_class = SignUpForm  # форма, которая будет заполняться пользователем;
    success_url = '/accounts/login'
    # URL, на которой нужно направить пользователя после успешной обработки формы;
    template_name = 'registration/signup.html'
    # шаблон, в котором будет отображена форма.
