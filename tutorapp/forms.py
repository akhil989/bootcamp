import decimal
from django import forms
from . import models


class VideoFormModel(forms.ModelForm):
    class Meta:
        model = models.VideoModel
        fields = ['title','thumbnail','video','price','category','description','free_course']
        
    def __init__(self, *args, **kwargs):
        super(VideoFormModel, self).__init__(*args, **kwargs)

        
        self.fields['title'].widget.attrs['class'] = 'form-control rounded-md text-slate-800'
        self.fields['video'].widget.attrs.update({'style': 'background-color: #059862;'})
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
        
        self.fields['free_course'].label = 'Free Corse? [Unselect field for ur paid videos]'
        self.fields['free_course'].widget.attrs['class'] = 'form-control rounded-md text-slate-800 w-6 h-6 border border-green-500'
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None:
            price_decimal = decimal.Decimal(str(price))  # Convert float to string and then to Decimal
            return price_decimal * decimal.Decimal('1.2')
        return price
class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control rounded-md text-slate-800',
                                      'placeholder': 'Write your feedback here (maximum 200 characters)',
                                      'rows': 4})  # Set the number of rows for the text area
    )
    class Meta:
        model = models.CommentTutorial
        fields = ['comment']
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        
        self.fields['comment'].label = 'Comment'
        self.fields['comment'].widget.attrs['class'] = 'form-control rounded-md text-slate-800 '
        self.fields['comment'].widget.attrs['placeholder'] = 'Write your feedback here(maximum 200 characters)'
        self.fields['comment'].help_text = ''
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = '__all__'