from django_countries.countries import COUNTRIES
attrs_dict = {'class': 'required'}
USERNAME_RE = r'^[\.\w]+$'

# to give the label of country field
COUNTRIES  = list(COUNTRIES)
COUNTRIES.insert(0, ('0', 'Country'))

list_per_page = 10

continents = (
              ('0','Continents',),
              ('Asia','Asia',),
              ('Africa','Africa',),
              ('Europe','Europe',),
              ('North America','North America',),
              ('South America','South America',),
              ('Antarctica','Antarctica',),
              ('Europe','Europe',),
              ('Australia','Australia',),
              )

company = (
           ('0', 'Select Company',),
           ('1', 'Company1',),
           ('2', 'Company2',)
           )

gender = (
          ('Male', 'Male',),
          ('Female', 'Female',)
          )

roles  =[
          ['Company', 'Company'],
          ['Manager', 'Manager'],
          ['Analyst', 'Analyst'],
          ]

answer_type  =[
          ['0', 'Choose Your Answer Type'],
          ['1', 'Text'],
          ['2', 'Radio'],
          ['3', 'Checkbox'],
          ['4', 'Slider'],
          ]



diary_choices  =[
          ['0', 'Diary1'],
          ['1', 'Diary1'],
          ['2', 'Diary1'],
          ['3', 'Diary1'],
          ['4', 'Diary1'],
          ]


recipient= (
           ('0', 'Select Recipient'),
           ('1', 'Caregiver1'),
           ('2', 'Caregiver2'),
           ('3', 'Client1'),
           ('4', 'Client2'),
           )


caregiver_choices= (
           ('0', 'Select Caregiver'),
           ('1', 'Caregiver1'),
           ('2', 'Caregiver2'),
           )

treatment_module = (
                    ('0', 'Select Module',),
                    ('1', 'Panic',),
                    ('2', 'Food',)
                    )

treatment_guidence = (
                    ('1', 'Follow with Guidence',),
                    ('2', 'Follow without Guidence',),
                    )

diary_intervel = (
                    ('0', 'Daily',),
                    ('1', 'Weekly',),
                    )

treatment_sessions = (
                    ('0', 'Select Session',),
                    ('1', 'Session1',),
                    ('2', 'Session2',),
                    ('3', 'Session3',),
                    ('4', 'Session4',),
                    ('5', 'Session5',),
                    ('6', 'Session6',),
                    )


caregivers_role = (
                    ('0', 'Select Role',),
                    ('1', 'Therapist',),
                    ('2', 'Secretary',),
                    ('3', 'Controller',),
                    ('4', 'Application Manager',),
                    ('5', 'Analyst',),
                   )

motivation_plans = (
                   ('0', 'Select Motivation Plan',),
                   ('1', 'Mplan1',),
                   ('2', 'Mplan2',),
                  )

practise_plans = (
                   ('0', 'Select Practise Plan',),
                   ('1', 'Plan1',),
                   ('2', 'Plan2',),
                  )