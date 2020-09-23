from ckeditor_uploader.widgets import CKEditorWidget, CKEditorUploadingWidget
 
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())