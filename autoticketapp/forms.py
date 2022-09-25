from django import forms
from .models import Ticket

class BootstrapMixin:
    """
    Add the base Bootstrap CSS classes to form elements.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        exempt_widgets = [
            forms.CheckboxInput,
            forms.FileInput,
            forms.RadioSelect,
            forms.Select,
        ]

        for field_name, field in self.fields.items():

            if field.widget.__class__ not in exempt_widgets:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()

            if field.required and not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['required'] = 'required'

            if 'placeholder' not in field.widget.attrs and field.label is not None:
                field.widget.attrs['placeholder'] = field.label

            if field.widget.__class__ == forms.CheckboxInput:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join((css, 'form-check-input')).strip()

            if field.widget.__class__ == forms.Select:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join((css, 'form-select')).strip()

class TicketForm (BootstrapMixin,forms.ModelForm):

    id = forms.CharField(widget=forms.HiddenInput,required=False)

    class Meta:
        model = Ticket
        fields = ["id","numero","titulo","descricao","prioridade"]