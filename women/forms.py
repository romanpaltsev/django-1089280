from typing import Any
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.forms import ValidationError

from .models import Category, Husband, Women


class AddPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=255,
    #                         min_length=5,
    #                         label="Заголовок",
    #                         widget=forms.TextInput(attrs={"class": "form-input"}),
    #                         error_messages={
    #                             "min_length": "Слишком короткий заголовок",
    #                             "required": "Без заголовка никак",
    #                         }
    #                         )
    # slug = forms.SlugField(max_length=255,
    #                        label="URL",
    #                        validators=[
    #                            MinLengthValidator(5, message="Минимум 5 символов"),
    #                            MaxLengthValidator(100, message="Максимум 100 символов"),
    #                        ]
    #                        )
    # content = forms.CharField(widget=forms.Textarea(attrs={"cols": 50, "rows": 5}), required=False, label="Контент")
    # is_published = forms.BooleanField(required=False, label="Статус", initial="True")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Муж", empty_label="Не замужем")
    class Meta:
        model = Women
        fields = ["title", "slug", "content", "photo", "is_published", "cat", "husband", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),            
        }
        labels = {
            "slug": "URL",
        }
    
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        
        return title
    
    
class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")