from django import forms

class QuizForm(forms.Form):
    identifier = forms.CharField(required=False, label='Your Name (optional)')
    
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.question_text,
                choices=[('a', question.solution.option_a), ('b', question.solution.option_b),
                         ('c', question.solution.option_c), ('d', question.solution.option_d)],
                widget=forms.RadioSelect
            )
