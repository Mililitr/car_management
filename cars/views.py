from rest_framework import viewsets, permissions, status
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer
from .forms import UserRegistrationForm

class CarViewSet(viewsets.ModelViewSet):
    """
    API ViewSet для работы с автомобилями.
    
    Предоставляет CRUD операции через API.
    Требует аутентификации для создания/изменения/удаления.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Сохраняет владельца при создании автомобиля."""
        serializer.save(owner=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    API ViewSet для работы с комментариями.
    
    Предоставляет CRUD операции для комментариев конкретного автомобиля.
    Требует аутентификации для создания комментариев.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Возвращает комментарии для конкретного автомобиля."""
        return Comment.objects.filter(car_id=self.kwargs['car_pk'])

    def perform_create(self, serializer):
        """Сохраняет автора и привязку к автомобилю при создании комментария."""
        car = get_object_or_404(Car, pk=self.kwargs['car_pk'])
        serializer.save(author=self.request.user, car=car)

class CarListView(ListView):
    """Отображение списка всех автомобилей."""
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    """
    Детальное отображение автомобиля.
    
    Также обрабатывает создание комментариев через POST запрос.
    """
    model = Car
    template_name = 'cars/car_detail.html'

    def post(self, request, *args, **kwargs):
        """Обработка создания нового комментария."""
        car = self.get_object()
        if request.user.is_authenticated:
            Comment.objects.create(
                content=request.POST.get('content'),
                car=car,
                author=request.user
            )
        return redirect('car-detail', pk=car.pk)

class CarCreateView(LoginRequiredMixin, CreateView):
    """
    Создание нового автомобиля.
    
    Доступно только аутентифицированным пользователям.
    """
    model = Car
    template_name = 'cars/car_form.html'
    fields = ['make', 'model', 'year', 'description']
    success_url = reverse_lazy('car-list')

    def form_valid(self, form):
        """Устанавливает текущего пользователя владельцем автомобиля."""
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CarUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование автомобиля.
    
    Доступно только владельцу автомобиля.
    """
    model = Car
    template_name = 'cars/car_form.html'
    fields = ['make', 'model', 'year', 'description']
    success_url = reverse_lazy('car-list')

    def get_queryset(self):
        """Возвращает только автомобили текущего пользователя."""
        return Car.objects.filter(owner=self.request.user)

class CarDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление автомобиля.
    
    Доступно только владельцу автомобиля.
    """
    model = Car
    template_name = 'cars/car_confirm_delete.html'
    success_url = reverse_lazy('car-list')

    def get_queryset(self):
        """Возвращает только автомобили текущего пользователя."""
        return Car.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Выполняет удаление и перенаправляет на список автомобилей."""
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

def register(request):
    """
    Регистрация нового пользователя.
    
    При успешной регистрации выполняет вход и перенаправляет на список автомобилей.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('car-list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})