import re
import datetime

from django import forms
from vcg.util.forms import HorizontalRadioRenderer
from django.utils.translation import ugettext as _

from vcg.client_management.models import ClientIntakeForm1, ClientIntakeForm2, ClientIntakeForm3 
from vcg.config.forms import terms_conditions

class ClientIntakeFormForm1(forms.ModelForm):
    class Meta:
        model = ClientIntakeForm1    

    def __init__(self, *args, **kw):
        super(ClientIntakeFormForm1, self).__init__(*args, **kw)

#Personal
        self.fields['name'].widget.attrs['class']                       = 'form-text'
        self.fields['birth_name'].widget.attrs['class']                 = 'form-text'
        self.fields['first_name'].widget.attrs['class']                 = 'form-text'
        self.fields['nick_name'].widget.attrs['class']                  = 'form-text'
        self.fields['address'].widget.attrs['class']                    = 'form-textarea'
        self.fields['postal_code_city'].widget.attrs['class']           = 'form-text'
        self.fields['phone_number'].widget.attrs['class']               = 'form-text'
        self.fields['email'].widget.attrs['class']                      = 'form-text'
        self.fields['dob'].widget.attrs['class']                        = 'form-text'
        self.fields['gender'].widget.attrs['class']                     = 'form-dropdownfield'
        self.fields['marital_status'].widget.attrs['class']             = 'form-dropdownfield'
        self.fields['home'].widget.attrs['class']                       = 'form-text'
        self.fields['citizen_service_number'].widget.attrs['class']     = 'form-text'
        self.fields['health_insurance_number'].widget.attrs['class']    = 'form-text'
        self.fields['doctor_name'].widget.attrs['class']                = 'form-text'
        self.fields['telephone_gp'].widget.attrs['class']               = 'form-text'

#Living conditions
        self.fields['live'].widget.attrs['class']                       = 'form-dropdownfield'
        self.fields['change_living_environment'].widget.attrs['class']  = 'form-dropdownfield'
 
#Current relationships
        self.fields['partner_details'].widget.attrs['class']            = 'form-textarea'
        self.fields['children_details'].widget.attrs['class']           = 'form-textarea'
        self.fields['about_relationship'].widget.attrs['class']         = 'form-textarea'
        self.fields['friends_details'].widget.attrs['class']            = 'form-textarea'
        self.fields['main_name'].widget.attrs['class']                  = 'form-textarea'
#Current activities
        self.fields['profession'].widget.attrs['class']                 = 'form-text'
        self.fields['working_hours'].widget.attrs['class']              = 'form-text'
        self.fields['steady_income'].widget.attrs['class']              = 'form-text'
        self.fields['benefit'].widget.attrs['class']                    = 'form-text'
        self.fields['provides_other_people'].widget.attrs['class']      = 'form-text'
        self.fields['household_chores'].widget.attrs['class']           = 'form-text'
        self.fields['free_time'].widget.attrs['class']                  = 'form-text'
        self.fields['free_time_hobbies'].widget.attrs['class']          = 'form-text'

#Problem
        self.fields['problem'].widget.attrs['class']                    = 'form-textarea'
        self.fields['problem_duration'].widget.attrs['class']           = 'form-textarea'
        self.fields['event_advance'].widget.attrs['class']              = 'form-textarea'

#Causes of your problem        
        self.fields['cause_problem'].widget.attrs['class']              = 'form-textarea'
        self.fields['people_involved'].widget.attrs['class']            = 'form-text'
        self.fields['your_share'].widget.attrs['class']            = 'form-textarea'
        self.fields['their_share'].widget.attrs['class']                = 'form-textarea'
        
#Perception of your problem        
        self.fields['suffer_problem_count'].widget.attrs['class']       = 'form-textarea'
        self.fields['feel_location'].widget.attrs['class']              = 'form-textarea'
        self.fields['like_to_change'].widget.attrs['class']             = 'form-textarea'
        self.fields['genaral_feel_number'].widget.attrs['class']        = 'form-dropdownfield'

#Impact on your daily life        
        self.fields['way_of_thinking'].widget.attrs['class']            = 'form-textarea'
        self.fields['emotional_life'].widget.attrs['class']             = 'form-textarea'
        self.fields['behaviour'].widget.attrs['class']                  = 'form-textarea'

#Problem Handling        
        self.fields['already_tried'].widget.attrs['class']              = 'form-textarea'
        self.fields['differnce'].widget.attrs['class']                  = 'form-textarea'
        self.fields['want_to_try'].widget.attrs['class']                = 'form-textarea'

#Earlier Assistance
        self.fields['therapy'].widget.attrs['class']                    = 'form-textarea'
        self.fields['duration'].widget.attrs['class']                   = 'form-text'
        self.fields['who_was_that'].widget.attrs['class']               = 'form-text'
        self.fields['what_problem'].widget.attrs['class']               = 'form-textarea'
        self.fields['therapy_outcome'].widget.attrs['class']            = 'form-text'
        self.fields['finding_solution'].widget.attrs['class']           = 'form-textarea'

#Supportive conditions        
        self.fields['keeps_on_leg'].widget.attrs['class']               = 'form-text'
        self.fields['get_energy'].widget.attrs['class']                 = 'form-text'
        self.fields['where_satisfied'].widget.attrs['class']            = 'form-text'
        self.fields['good_in_your_life'].widget.attrs['class']          = 'form-text'
        
#Social support to your problem
        self.fields['someone_your_problem'].widget.attrs['class']       = 'form-text'        
        self.fields['anyone_you_support'].widget.attrs['class']         = 'form-text'
        self.fields['height_of_problem'].widget.attrs['class']          = 'form-text'
        self.fields['you_smoke'].widget.attrs['class']                  = 'form-text'
        
#Current function
        self.fields['carry_out_work'].widget.attrs['class']             = 'form-text'
        self.fields['relation_with_others'].widget.attrs['class']       = 'form-text'
        self.fields['meaning_in_life'].widget.attrs['class']            = 'form-text'
        self.fields['interest_in_things'].widget.attrs['class']         = 'form-text'
        self.fields['meet_expectations'].widget.attrs['class']          = 'form-text'
        self.fields['about_future'].widget.attrs['class']               = 'form-textarea'

#Start Validations
#Personal
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return name
    
    def clean_birth_name(self):
        birth_name = self.cleaned_data['birth_name']
        if len(birth_name) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return birth_name
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return first_name
    
    def clean_nick_name(self):
        nick_name = self.cleaned_data['nick_name']
        if len(nick_name) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return nick_name
    
    def clean_address(self):
        address = self.cleaned_data['address']
        if len(address) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return address
    
    def clean_postal_code_city(self):
        postal_code_city = self.cleaned_data['postal_code_city']
        if len(postal_code_city) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return postal_code_city
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return phone_number
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return email
    
    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob != None:
            if dob > datetime.date.today():
                raise forms.ValidationError(_("Date cannot be in future"))
            return dob
    
#    def clean_gender(self):
#        gender = self.cleaned_data['gender']
#        if len(gender) < 1:
#            raise forms.ValidationError(_('Enter minimum 1 character.'))
#        return gender
#    
#    def clean_marital_status(self):
#        marital_status = self.cleaned_data['marital_status']
#        if len(marital_status) < 1:
#            raise forms.ValidationError(_('Enter minimum 1 character.'))
#        return marital_status
#    
    def clean_home(self):
        home = self.cleaned_data['home']
        if len(home) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return home
    
    def clean_citizen_service_number(self):
        citizen_service_number = self.cleaned_data['citizen_service_number']
        if len(citizen_service_number) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return citizen_service_number
    
    def clean_health_insurance_number(self):
        health_insurance_number = self.cleaned_data['health_insurance_number']
        if len(health_insurance_number) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return health_insurance_number
    
    def clean_doctor_name(self):
        doctor_name = self.cleaned_data['doctor_name']
        if len(doctor_name) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return doctor_name
    
    def clean_telephone_gp(self):
        telephone_gp = self.cleaned_data['telephone_gp']
        if len(telephone_gp) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return telephone_gp

#Living conditions    
#    def clean_live(self):
#        live = self.cleaned_data['live']
#        if len(live) < 1:
#            raise forms.ValidationError(_('Enter minimum 1 character.'))
#        return live
#
#    def clean_change_living_environment(self):
#        change_living_environment = self.cleaned_data['change_living_environment']
#        if len(change_living_environment) < 1:
#            raise forms.ValidationError(_('Enter minimum 1 character.'))
#        return change_living_environment

#Current relationships    
    def clean_partner_details(self):
        partner_details = self.cleaned_data['partner_details']
        if partner_details:
            if len(partner_details) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return partner_details
    
    def clean_children_details(self):
        children_details = self.cleaned_data['children_details']
        if children_details:
            if len(children_details) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return children_details
    
    def clean_about_relationship(self):
        about_relationship = self.cleaned_data['about_relationship']
        if about_relationship:
            if len(about_relationship) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return about_relationship
    
    def clean_friends_details(self):
        friends_details = self.cleaned_data['friends_details']
        if friends_details:
            if len(friends_details) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return friends_details
    
    def clean_main_name(self):
        main_name = self.cleaned_data['main_name']
        if main_name:
            if len(main_name) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return main_name

#Current activities
    def clean_profession(self):
        profession = self.cleaned_data['profession']
        if len(profession) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return profession
    
    def clean_working_hours(self):
        working_hours = self.cleaned_data['working_hours']
        if len(working_hours) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return working_hours
    
    def clean_steady_income(self):
        steady_income = self.cleaned_data['steady_income']
        if len(steady_income) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return steady_income
    
    def clean_benefit(self):
        benefit = self.cleaned_data['benefit']
        if len(benefit) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return benefit
    
    def clean_provides_other_people(self):
        provides_other_people = self.cleaned_data['provides_other_people']
        if len(provides_other_people) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return provides_other_people
    
    def clean_household_chores(self):
        household_chores = self.cleaned_data['household_chores']
        if len(household_chores) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return household_chores
    
    def clean_free_time(self):
        free_time = self.cleaned_data['free_time']
        if len(free_time) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return free_time
    
    def clean_free_time_hobbies(self):
        free_time_hobbies = self.cleaned_data['free_time_hobbies']
        if len(free_time_hobbies) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return free_time_hobbies

#Problem
    def clean_problem(self):
        problem = self.cleaned_data['problem']
        if problem:
            if len(problem) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return problem
     
    def clean_problem_duration(self):
        problem_duration = self.cleaned_data['problem_duration']
        if problem_duration:
            if len(problem_duration) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return problem_duration
     
    def clean_event_advance(self):
        event_advance = self.cleaned_data['event_advance']
        if event_advance:
            if len(event_advance) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return event_advance
    
#Causes of your problem
    def clean_cause_problem(self):
        cause_problem = self.cleaned_data['cause_problem']
        if cause_problem:
            if len(cause_problem) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return cause_problem
    
    def clean_people_involved(self):
        people_involved = self.cleaned_data['people_involved']
        if len(people_involved) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return people_involved
    
    def clean_your_share(self):
        your_share = self.cleaned_data['your_share']
        if your_share:
            if len(your_share) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return your_share
        
    def clean_their_share(self):
        their_share = self.cleaned_data['their_share']
        if their_share:
            if len(their_share) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return their_share
    
#Perception of your problem
    def clean_suffer_problem_count(self):
        suffer_problem_count = self.cleaned_data['suffer_problem_count']
        if suffer_problem_count:
            if len(suffer_problem_count) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return suffer_problem_count
    
    def clean_feel_location(self):
        feel_location = self.cleaned_data['feel_location']
        if feel_location:
            if len(feel_location) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return feel_location
    
    def clean_like_to_change(self):
        like_to_change = self.cleaned_data['like_to_change']
        if like_to_change:
            if len(like_to_change) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return like_to_change
    
#    def clean_genaral_feel_number(self):
#        genaral_feel_number = self.cleaned_data['genaral_feel_number']
#        if len(genaral_feel_number) < 1:
#            raise forms.ValidationError(_('Enter minimum 1 character.'))
#        return genaral_feel_number

#Impact on your daily life    
    def clean_(self):
        way_of_thinking = self.cleaned_data['way_of_thinking']
        if len(way_of_thinking) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return way_of_thinking 

    def clean_emotional_life(self):
        emotional_life = self.cleaned_data['emotional_life']
        if emotional_life:
            if len(emotional_life) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return emotional_life

    def clean_behaviour(self):
        behaviour = self.cleaned_data['behaviour']
        if behaviour:
            if len(behaviour) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return behaviour
    
#Problem Handling    
    def clean_already_tried(self):
        already_tried = self.cleaned_data['already_tried']
        if already_tried:
            if len(already_tried) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return already_tried
    
    def clean_differnce(self):
        differnce = self.cleaned_data['differnce']
        if differnce:
            if len(differnce) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return differnce
    
    def clean_want_to_try(self):
        want_to_try = self.cleaned_data['want_to_try']
        if want_to_try:
            if len(want_to_try) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return want_to_try

#Earlier Assistance    
    def clean_therapy(self):
        therapy = self.cleaned_data['therapy']
        if therapy:
            if len(therapy) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return therapy
    
    def clean_duration(self):
        duration = self.cleaned_data['duration']
        if len(duration) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return duration
    
    def clean_who_was_that(self):
        who_was_that = self.cleaned_data['who_was_that']
        if len(who_was_that) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return who_was_that
    
    def clean_what_problem(self):
        what_problem = self.cleaned_data['what_problem']
        if what_problem:
            if len(what_problem) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return what_problem
    
    def clean_therapy_outcome(self):
        therapy_outcome = self.cleaned_data['therapy_outcome']
        if len(therapy_outcome) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return therapy_outcome
    
    def clean_finding_solution(self):
        finding_solution = self.cleaned_data['finding_solution']
        if finding_solution:
            if len(finding_solution) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return finding_solution
    
#Supportive conditions    
    def clean_keeps_on_leg(self):
        keeps_on_leg = self.cleaned_data['keeps_on_leg']
        if len(keeps_on_leg) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return keeps_on_leg
    
    def clean_get_energy(self):
        get_energy = self.cleaned_data['get_energy']
        if len(get_energy) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return get_energy
    
    def clean_where_satisfied(self):
        where_satisfied = self.cleaned_data['where_satisfied']
        if len(where_satisfied) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return where_satisfied
    
    def clean_good_in_your_life(self):
        good_in_your_life = self.cleaned_data['good_in_your_life']
        if len(good_in_your_life) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return good_in_your_life

#Social support to your problem    
    def clean_someone_your_problem(self):
        someone_your_problem = self.cleaned_data['someone_your_problem']
        if len(someone_your_problem) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return someone_your_problem
    
    def clean_anyone_you_support(self):
        anyone_you_support = self.cleaned_data['anyone_you_support']
        if len(anyone_you_support) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return anyone_you_support
    
    def clean_height_of_problem(self):
        height_of_problem = self.cleaned_data['height_of_problem']
        if len(height_of_problem) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return height_of_problem
    
    def clean_you_smoke(self):
        you_smoke = self.cleaned_data['you_smoke']
        if len(you_smoke) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return you_smoke

#Current function    
    def clean_carry_out_work(self):
        carry_out_work = self.cleaned_data['carry_out_work']
        if len(carry_out_work) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return carry_out_work
    
    def clean_relation_with_others(self):
        relation_with_others = self.cleaned_data['relation_with_others']
        if len(relation_with_others) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return relation_with_others
    
    def clean_meaning_in_life(self):
        meaning_in_life = self.cleaned_data['meaning_in_life']
        if len(meaning_in_life) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return meaning_in_life
    
    def clean_interest_in_things(self):
        interest_in_things = self.cleaned_data['interest_in_things']
        if len(interest_in_things) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return interest_in_things
    
    def clean_meet_expectations(self):
        meet_expectations = self.cleaned_data['meet_expectations']
        if len(meet_expectations) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return meet_expectations
    
    def clean_about_future(self):
        about_future = self.cleaned_data['about_future']
        if about_future:
            if len(about_future) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return about_future

class ClientIntakeFormForm2(forms.ModelForm):
    class Meta:
        model = ClientIntakeForm2    

    def __init__(self, *args, **kw):
        super(ClientIntakeFormForm2, self).__init__(*args, **kw)
        
#Current health        
        self.fields['physical_problems'].widget.attrs['class']          = 'form-text'
        self.fields['medical_conditions'].widget.attrs['class']         = 'form-text'
        self.fields['about_medication'].widget.attrs['class']           = 'form-text'
        self.fields['about_drugs'].widget.attrs['class']                = 'form-text'
        self.fields['about_alcohol'].widget.attrs['class']              = 'form-text'
        self.fields['about_smoke'].widget.attrs['class']                = 'form-text'
        self.fields['eating_disorders'].widget.attrs['class']           = 'form-text'
        self.fields['sleep_problem'].widget.attrs['class']              = 'form-text'
        self.fields['sexually_active'].widget.attrs['class']            = 'form-text'

#Therapy goals
        self.fields['accomplish'].widget.attrs['class']                 = 'form-textarea'
        self.fields['effect'].widget.attrs['class']                     = 'form-textarea'
        self.fields['most_important'].widget.attrs['class']             = 'form-textarea'
        self.fields['life_look'].widget.attrs['class']                  = 'form-text'
        self.fields['when_achieved'].widget.attrs['class']              = 'form-text'
        self.fields['what_tasks'].widget.attrs['class']                 = 'form-textarea'
        
#Biography
        self.fields['parents_details'].widget.attrs['class']            = 'form-text'
        self.fields['family_children_details'].widget.attrs['class']    = 'form-text'
        self.fields['chile_in_line'].widget.attrs['class']              = 'form-text'
        self.fields['child_temperament'].widget.attrs['class']          = 'form-text'
        self.fields['easy_contact'].widget.attrs['class']               = 'form-text'
        self.fields['like_as_child'].widget.attrs['class']              = 'form-textarea'
        self.fields['material_conditions'].widget.attrs['class']        = 'form-text'
        self.fields['emotional_conditions'].widget.attrs['class']       = 'form-textarea'
        self.fields['father'].widget.attrs['class']                     = 'form-textarea'
        self.fields['style_of_parenting'].widget.attrs['class']         = 'form-textarea'
        self.fields['father_occupation'].widget.attrs['class']          = 'form-text'
        self.fields['father_relationship'].widget.attrs['class']        = 'form-textarea'
        self.fields['mother'].widget.attrs['class']                     = 'form-textarea'
        self.fields['untitled_element'].widget.attrs['class']           = 'form-textarea'
        self.fields['mother_occupation'].widget.attrs['class']          = 'form-text'
        self.fields['mother_relationship'].widget.attrs['class']        = 'form-textarea'
        self.fields['parents_eye_desires'].widget.attrs['class']        = 'form-textarea'
        self.fields['parents_relationship'].widget.attrs['class']       = 'form-textarea'
        self.fields['important_in_youth'].widget.attrs['class']         = 'form-text'
        self.fields['cultural_background'].widget.attrs['class']        = 'form-text'
        
#Family situation as a child        
        self.fields['family_involvement'].widget.attrs['class']         = 'form-text'
        self.fields['support'].widget.attrs['class']                    = 'form-text'
        self.fields['warmth_love'].widget.attrs['class']                = 'form-text'
        self.fields['home_for_saying'].widget.attrs['class']            = 'form-text'
        self.fields['responsibility'].widget.attrs['class']             = 'form-text'
        self.fields['decisions'].widget.attrs['class']                  = 'form-text'
        self.fields['bepreken'].widget.attrs['class']                   = 'form-text'
        self.fields['religion_role'].widget.attrs['class']              = 'form-text'
        self.fields['about_freedom'].widget.attrs['class']              = 'form-text'
        self.fields['labor_division'].widget.attrs['class']             = 'form-text'
        self.fields['family_tasks'].widget.attrs['class']               = 'form-text'

#Youth Experiences
        self.fields['physical_violence'].widget.attrs['class']          = 'form-text'
        self.fields['mental_violenc'].widget.attrs['class']             = 'form-text'
        self.fields['sexual_violence'].widget.attrs['class']            = 'form-text'
        self.fields['childhood'].widget.attrs['class']                  = 'form-text'
        self.fields['bullied_in_childhood'].widget.attrs['class']       = 'form-text'
        self.fields['adolescence'].widget.attrs['class']                = 'form-text'
        self.fields['accepted_youth'].widget.attrs['class']             = 'form-text'
        self.fields['pleasant_memory'].widget.attrs['class']            = 'form-text'
        self.fields['nastiest_memory'].widget.attrs['class']            = 'form-text'

#Current health    
    def clean_physical_problems(self):
        physical_problems = self.cleaned_data['physical_problems']
        if len(physical_problems) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return physical_problems
    
    def clean_medical_conditions(self):
        medical_conditions = self.cleaned_data['medical_conditions']
        if len(medical_conditions) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return medical_conditions
    
    def clean_about_medication(self):
        about_medication = self.cleaned_data['about_medication']
        if len(about_medication) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return about_medication
    
    def clean_about_drugs(self):
        about_drugs = self.cleaned_data['about_drugs']
        if len(about_drugs) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return about_drugs
    
    def clean_about_alcohol(self):
        about_alcohol = self.cleaned_data['about_alcohol']
        if len(about_alcohol) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return about_alcohol
    
    def clean_about_smoke(self):
        about_smoke = self.cleaned_data['about_smoke']
        if len(about_smoke) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return about_smoke
    
    def clean_eating_disorders(self):
        eating_disorders = self.cleaned_data['eating_disorders']
        if len(eating_disorders) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return eating_disorders
    
    def clean_sleep_problem(self):
        sleep_problem = self.cleaned_data['sleep_problem']
        if len(sleep_problem) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return sleep_problem
    
    def clean_sexually_active(self):
        sexually_active = self.cleaned_data['sexually_active']
        if len(sexually_active) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return sexually_active
    
#Therapy goals    
    def clean_accomplish(self):
        accomplish = self.cleaned_data['accomplish']
        if accomplish:
            if len(accomplish) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return accomplish
    
    def clean_effect(self):
        effect = self.cleaned_data['effect']
        if effect:
            if len(effect) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return effect
    
    def clean_most_important(self):
        most_important = self.cleaned_data['most_important']
        if most_important:
            if len(most_important) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return most_important
    
    def clean_life_look(self):
        life_look = self.cleaned_data['life_look']
        if len(life_look) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return life_look
    
    def clean_when_achieved(self):
        when_achieved = self.cleaned_data['when_achieved']
        if len(when_achieved) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return when_achieved
    
    def clean_what_tasks(self):
        what_tasks = self.cleaned_data['what_tasks']
        if what_tasks:
            if len(what_tasks) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return what_tasks
    
    
#Biography    
    def clean_parents_details(self):
        parents_details = self.cleaned_data['parents_details']
        if len(parents_details) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return parents_details
    
    def clean_family_children_details(self):
        family_children_details = self.cleaned_data['family_children_details']
        if len(family_children_details) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return family_children_details
    
    def clean_chile_in_line(self):
        chile_in_line = self.cleaned_data['chile_in_line']
        if len(chile_in_line) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return chile_in_line
    
    def clean_child_temperament(self):
        child_temperament = self.cleaned_data['child_temperament']
        if len(child_temperament) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return child_temperament
    
    def clean_easy_contact(self):
        easy_contact = self.cleaned_data['easy_contact']
        if len(easy_contact) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return easy_contact
    
    def clean_like_as_child(self):
        like_as_child = self.cleaned_data['like_as_child']
        if like_as_child:
            if len(like_as_child) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return like_as_child
    
    def clean_material_conditions(self):
        material_conditions = self.cleaned_data['material_conditions']
        if len(material_conditions) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return material_conditions
    
    def clean_emotional_conditions(self):
        emotional_conditions = self.cleaned_data['emotional_conditions']
        if emotional_conditions:
            if len(emotional_conditions) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return emotional_conditions

    def clean_father(self):
        father = self.cleaned_data['father']
        if father:
            if len(father) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return father
    
    def clean_style_of_parenting(self):
        style_of_parenting = self.cleaned_data['style_of_parenting']
        if style_of_parenting:
            if len(style_of_parenting) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return style_of_parenting
    
    def clean_father_occupation(self):
        father_occupation = self.cleaned_data['father_occupation']
        if len(father_occupation) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return father_occupation
    
    def clean_father_relationship(self):
        father_relationship = self.cleaned_data['father_relationship']
        if father_relationship:
            if len(father_relationship) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return father_relationship
    
    def clean_mother(self):
        mother = self.cleaned_data['mother']
        if mother:
            if len(mother) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return mother
    
    def clean_untitled_element(self):
        untitled_element = self.cleaned_data['untitled_element']
        if untitled_element:
            if len(untitled_element) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return untitled_element
    
    def clean_mother_occupation(self):
        mother_occupation = self.cleaned_data['mother_occupation']
        if len(mother_occupation) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return mother_occupation
    
    def clean_mother_relationship(self):
        mother_relationship = self.cleaned_data['mother_relationship']
        if mother_relationship:
            if len(mother_relationship) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return mother_relationship
        
    def clean_parents_eye_desires(self):
        parents_eye_desires = self.cleaned_data['parents_eye_desires']
        if parents_eye_desires:
            if len(parents_eye_desires) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return parents_eye_desires
    
    def clean_parents_relationship(self):
        parents_relationship = self.cleaned_data['parents_relationship']
        if parents_relationship:
            if len(parents_relationship) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return parents_relationship
    
    def clean_important_in_youth(self):
        important_in_youth = self.cleaned_data['important_in_youth']
        if len(important_in_youth) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return important_in_youth
    
    def clean_cultural_background(self):
        cultural_background = self.cleaned_data['cultural_background']
        if len(cultural_background) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return cultural_background
    
#Family situation as a child    
    def clean_family_involvement(self):
        family_involvement = self.cleaned_data['family_involvement']
        if len(family_involvement) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return family_involvement
    
    def clean_support(self):
        support = self.cleaned_data['support']
        if len(support) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return support
    
    def clean_warmth_love(self):
        warmth_love = self.cleaned_data['warmth_love']
        if len(warmth_love) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return warmth_love
    
    def clean_home_for_saying(self):
        home_for_saying = self.cleaned_data['home_for_saying']
        if len(home_for_saying) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return home_for_saying
    
    def clean_responsibility(self):
        responsibility = self.cleaned_data['responsibility']
        if len(responsibility) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return responsibility
    
    def clean_decisions(self):
        decisions = self.cleaned_data['decisions']
        if len(decisions) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return decisions

    def clean_bepreken(self):
        bepreken = self.cleaned_data['bepreken']
        if len(bepreken) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return bepreken
    
    def clean_religion_role(self):
        religion_role = self.cleaned_data['religion_role']
        if len(religion_role) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return religion_role
    
    def clean_about_freedom(self):
        about_freedom = self.cleaned_data['about_freedom']
        if len(about_freedom) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return about_freedom
    
    def clean_labor_division(self):
        labor_division = self.cleaned_data['labor_division']
        if len(labor_division) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return labor_division
    
    def clean_family_tasks(self):
        family_tasks = self.cleaned_data['family_tasks']
        if len(family_tasks) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return family_tasks

#Youth Experiences    
    def clean_physical_violence(self):
        physical_violence = self.cleaned_data['physical_violence']
        if len(physical_violence) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return physical_violence
    
    def clean_mental_violenc(self):
        mental_violenc = self.cleaned_data['mental_violenc']
        if mental_violenc:
            if len(mental_violenc) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return mental_violenc
    
    def clean_sexual_violence(self):
        sexual_violence = self.cleaned_data['sexual_violence']
        if len(sexual_violence) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return sexual_violence
    
    def clean_childhood(self):
        childhood = self.cleaned_data['childhood']
        if len(childhood) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return childhood
    
    def clean_bullied_in_childhood(self):
        bullied_in_childhood = self.cleaned_data['bullied_in_childhood']
        if len(bullied_in_childhood) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return bullied_in_childhood
    
    def clean_adolescence(self):
        adolescence = self.cleaned_data['adolescence']
        if len(adolescence) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return adolescence
    
    def clean_accepted_youth(self):
        accepted_youth = self.cleaned_data['accepted_youth']
        if len(accepted_youth) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return accepted_youth
    
    def clean_pleasant_memory(self):
        pleasant_memory = self.cleaned_data['pleasant_memory']
        if len(pleasant_memory) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return pleasant_memory
    
    def clean_nastiest_memory(self):
        nastiest_memory = self.cleaned_data['nastiest_memory']
        if len(nastiest_memory) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return nastiest_memory

class ClientIntakeFormForm3(forms.ModelForm):
    terms_conditions = forms.ChoiceField(initial=0, widget = forms.RadioSelect(renderer = HorizontalRadioRenderer), choices = terms_conditions, label =_('Do you agree with the terms and conditions of the practitioner (see menu item "Terms")?*'))
    
    class Meta:
        model = ClientIntakeForm3    

    def __init__(self, *args, **kw):
        super(ClientIntakeFormForm3, self).__init__(*args, **kw)
            
#Precepts
        self.fields['commandments_youth'].widget.attrs['class']         = 'form-text'
        self.fields['prohibited_youth'].widget.attrs['class']           = 'form-text'
        self.fields['informed_sexually'].widget.attrs['class']          = 'form-text'
        self.fields['handle_conflicts'].widget.attrs['class']           = 'form-text'
        self.fields['affection_shown'].widget.attrs['class']            = 'form-text'
        self.fields['standards_values'].widget.attrs['class']           = 'form-text'

#Training and Opportunities
        self.fields['school'].widget.attrs['class']                     = 'form-text'
        self.fields['highest_education'].widget.attrs['class']          = 'form-text'
        self.fields['training'].widget.attrs['class']                   = 'form-text'
        self.fields['encouraged_parents'].widget.attrs['class']         = 'form-text'
        self.fields['talents'].widget.attrs['class']                    = 'form-text'
        self.fields['forced_direction'].widget.attrs['class']           = 'form-text'
        self.fields['contacts_at_school'].widget.attrs['class']         = 'form-text'
        self.fields['contacts_with_friends'].widget.attrs['class']      = 'form-text'
        self.fields['your_hobbies'].widget.attrs['class']               = 'form-text'
        self.fields['clubs_associations'].widget.attrs['class']         = 'form-text'
        self.fields['satisfied_education'].widget.attrs['class']        = 'form-text'
        self.fields['satisfied_work'].widget.attrs['class']             = 'form-text'

#File formation        
        self.fields['finance_therapy'].widget.attrs['class']            = 'form-text'

#Remaining        
        self.fields['comments'].widget.attrs['class']                   = 'form-textarea'



#Precepts    
    def clean_commandments_youth(self):
        commandments_youth = self.cleaned_data['commandments_youth']
        if len(commandments_youth) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return commandments_youth
    
    def clean_prohibited_youth(self):
        prohibited_youth = self.cleaned_data['prohibited_youth']
        if len(prohibited_youth) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return prohibited_youth
    
    def clean_informed_sexually(self):
        informed_sexually = self.cleaned_data['informed_sexually']
        if len(informed_sexually) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return informed_sexually
    
    def clean_handle_conflicts(self):
        handle_conflicts = self.cleaned_data['handle_conflicts']
        if len(handle_conflicts) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return handle_conflicts
    
    def clean_affection_shown(self):
        affection_shown = self.cleaned_data['affection_shown']
        if len(affection_shown) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return affection_shown
    
    def clean_standards_values(self):
        standards_values = self.cleaned_data['standards_values']
        if len(standards_values) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return standards_values

#Training and Opportunities    
    def clean_school(self):
        school = self.cleaned_data['school']
        if len(school) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return school
    
    def clean_highest_education(self):
        highest_education = self.cleaned_data['highest_education']
        if len(highest_education) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return highest_education
    
    def clean_training(self):
        training = self.cleaned_data['training']
        if len(training) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return training
    
    def clean_encouraged_parents(self):
        encouraged_parents = self.cleaned_data['encouraged_parents']
        if len(encouraged_parents) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return encouraged_parents
    
    def clean_talents(self):
        talents = self.cleaned_data['talents']
        if len(talents) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return talents
    
    def clean_forced_direction(self):
        forced_direction = self.cleaned_data['forced_direction']
        if len(forced_direction) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return forced_direction
    
    def clean_contacts_at_school(self):
        contacts_at_school = self.cleaned_data['contacts_at_school']
        if len(contacts_at_school) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return contacts_at_school

    def clean_contacts_with_friends(self):
        contacts_with_friends = self.cleaned_data['contacts_with_friends']
        if len(contacts_with_friends) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return contacts_with_friends
    
    def clean_your_hobbies(self):
        your_hobbies = self.cleaned_data['your_hobbies']
        if len(your_hobbies) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return your_hobbies
    
    def clean_clubs_associations(self):
        clubs_associations = self.cleaned_data['clubs_associations']
        if len(clubs_associations) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return clubs_associations
    
    def clean_satisfied_education(self):
        satisfied_education = self.cleaned_data['satisfied_education']
        if len(satisfied_education) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return satisfied_education
    
    def clean_satisfied_work(self):
        satisfied_work = self.cleaned_data['satisfied_work']
        if len(satisfied_work) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return satisfied_work

#File formation
#    def clean_terms_conditions(self):
#        terms_conditions = self.cleaned_data['terms_conditions']
#        if len(terms_conditions) < 1:
#            raise forms.ValidationError(_('Enter minimum 1 character.'))
#        return terms_conditions
    
    def clean_finance_therapy(self):
        finance_therapy = self.cleaned_data['finance_therapy']
        if len(finance_therapy) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        return finance_therapy

#Remaining    
    def clean_comments(self):
        comments = self.cleaned_data['comments']
        if comments:
            if len(comments) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return comments
