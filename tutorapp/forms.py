from django import forms
from . import models

class VideoFormModel(forms.ModelForm):
    class Meta:
        model = models.VideoModel
        fields = ['title','thumbnail','video','price','category','description']
    def __init__(self, *args, **kwargs):
        super(VideoFormModel, self).__init__(*args, **kwargs)

        
        self.fields['title'].widget.attrs['class'] = 'form-control rounded-md text-slate-800'
        self.fields['title'].label = 'Title'
        self.fields['title'].widget.attrs['placeholder'] = 'Title'
        self.fields['title'].help_text = ''
        
        self.fields['thumbnail'].widget.attrs['class'] = 'form-control px-3 rounded-md   h-11 py-2 px-1 text-slate-200'
        self.fields['thumbnail'].widget.attrs.update({'style': 'background-color: #059862;'})
        self.fields['thumbnail'].label = 'Add Thumbnail'
        self.fields['thumbnail'].widget.attrs['placeholder'] = ''
        self.fields['thumbnail'].help_text = ''
        
        self.fields['video'].widget.attrs['class'] = 'form-control px-3 rounded-md   h-11 py-2 px-1 text-slate-200'
        self.fields['video'].widget.attrs.update({'style': 'background-color: #059862;'})
        self.fields['video'].label = 'Add Video File'
        self.fields['video'].widget.attrs['placeholder'] = ''
        self.fields['video'].help_text = ''
        
        # self.fields['instructor'].label = 'Instructor'
        # self.fields['instructor'].widget.attrs['class'] = 'form-control hidden  xs:w-full xm:w-full sm:w-full md:w-1/3 lg:w-1/3 xl:w-1/3 2xl:w-1/3 rounded-md text-slate-800'
        # self.fields['instructor'].widget.attrs['placeholder'] = ''
        # self.fields['instructor'].help_text = ''
        
        self.fields['price'].label = 'Price'
        self.fields['price'].widget.attrs['class'] = 'form-control xs:w-full xm:w-full sm:w-full md:w-1/3 lg:w-1/3 xl:w-1/3 2xl:w-1/3 rounded-md text-slate-800'
        self.fields['price'].widget.attrs['placeholder'] = 'Price'
        self.fields['price'].help_text = ''
        
        self.fields['category'].label = 'Category'
        self.fields['category'].widget.attrs['class'] = 'form-control xs:w-full xm:w-full sm:w-full md:w-1/3 lg:w-1/3 xl:w-1/3 2xl:w-1/3 rounded-md text-slate-800'
        self.fields['category'].widget.attrs['placeholder'] = 'Category'
        self.fields['category'].help_text = ''
        
        
        self.fields['description'].label = 'Description'
        self.fields['description'].widget.attrs['class'] = 'form-control rounded-md text-slate-800'
        self.fields['description'].widget.attrs['placeholder'] = 'Describe About Your Tutorial Video'
        self.fields['description'].help_text = ''
        
        
# class FileUploadForm(forms.ModelForm):
#     class Meta:
#         model = models.FileModel
#         fields = "__all__"
#     def __init__(self, *args, **kwargs):
#         super(FileUploadForm, self).__init__(*args, **kwargs)
#         self.fields['file_name'].widget.attrs['style'] = 'width: 90%; border: 2px solid green; border-radius: 6px;' 
#         # self.fields['file_data'].widget.attrs['style'] = 'width: 30%; border: 2px solid green; border-radius: 6px;'  
#         self.fields['image_data'].widget.attrs['style'] = ''