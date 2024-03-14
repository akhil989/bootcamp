from django import forms
from . import models

class VideoFormModel(forms.ModelForm):
    class Meta:
        model = models.VideoModel
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(VideoFormModel, self).__init__(*args, **kwargs)

        
        self.fields['title'].widget.attrs['class'] = 'form-control rounded-md text-slate-800'
        self.fields['title'].label = 'Title'
        self.fields['title'].widget.attrs['placeholder'] = 'Title'
        self.fields['title'].help_text = ''
        
        self.fields['instructor'].label = 'Instructor'
        self.fields['instructor'].widget.attrs['class'] = 'form-control rounded-md text-slate-800'
        self.fields['instructor'].widget.attrs['placeholder'] = 'Title'
        self.fields['instructor'].help_text = ''
        
        self.fields['price'].label = 'Price'
        self.fields['price'].widget.attrs['class'] = 'form-control  w-1/3 rounded-md text-slate-800'
        self.fields['price'].widget.attrs['placeholder'] = 'Price'
        self.fields['price'].help_text = ''
        
        self.fields['category'].label = 'Category'
        self.fields['category'].widget.attrs['class'] = 'form-control w-1/3 rounded-md text-slate-800'
        self.fields['category'].widget.attrs['placeholder'] = 'Category'
        self.fields['category'].help_text = ''
        
        
        self.fields['description'].label = 'Description'
        self.fields['description'].widget.attrs['class'] = 'form-control rounded-md text-slate-800'
        self.fields['description'].widget.attrs['placeholder'] = 'Describe About Your Tutorial Video'
        self.fields['description'].help_text = ''
        