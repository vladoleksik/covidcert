from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, HiddenField, BooleanField
from wtforms.fields.html5 import DateField, DateTimeLocalField
from wtforms.validators import InputRequired
import gen_function


app = Flask(__name__)
app.config['SECRET_KEY']='11235813'


class GenVacForm(FlaskForm):
    fname_print = StringField('Last name')
    gname_print = StringField('First name')
    birth = DateField('Date of birth', format='%Y-%m-%d')
    cert_type=HiddenField(default='v')
    disease_curr = SelectField('Targeted disease', default='none', choices=[('none', ''),
                                                                            ('COVID-19', 'COVID-19')])
    vaccine_type_curr = SelectField('Vaccine type', default='none', choices=[('none', ''),
                                                                             ('mRNA', 'mRNA Vaccine'),
                                                                             ('antigen', 'Antigen Vaccine'),
                                                                             ('other', 'Other vaccines')])
    manufacturer_curr = SelectField('Vaccine manufacturer', default='none', choices=[('none', ''),
                                                                                     ('Biontech', 'Biontech'),
                                                                                     ('Moderna', 'Moderna'),
                                                                                     ('AstraZeneca', 'AstraZeneca'),
                                                                                     ('Johnson', 'Johnson&Johnson')])
    vaccine_prod_curr = SelectField('Vaccine name', default='none', choices=[('none', ''),
                                                                             ('Pfizer', 'Pfizer (Comirnaty)'),
                                                                             ('Moderna', 'Moderna (Spikevax)'),
                                                                             ('AstraZeneca', 'AstraZeneca (Vaxzevria)'),
                                                                             ('Johnson', 'Johnson (Janssen)')])
    doses_rec = IntegerField('Number of doses received', description='Number of doses received until now')
    doses_tot = IntegerField('Total planned doses', description='Number of doses you are to receive, as known to date')
    dt_last_dose = DateField('Date of last dose', format='%Y-%m-%d')
    emitent = StringField('Issuer', default='UU Ministry of Certificate Signing')
    joke1=BooleanField('I am a human')
    joke2=BooleanField('I am telling the truth')


class GenTestForm(FlaskForm):
    fname_print = StringField('Last name')
    gname_print = StringField('First name')
    birth = DateField('Date of birth', format='%Y-%m-%d')
    cert_type=HiddenField(default='t')
    disease_curr = SelectField('Targeted disease', default='none', choices=[('none', ''),
                                                                            ('COVID-19', 'COVID-19')])
    test_type_curr = SelectField('Test type', default='none', choices=[('none', ''),
                                                                             ('Nucleic', 'NAAT Test (PCR)'),
                                                                             ('Rapid', 'RAT Test (Rapid)')])
    result_test=SelectField('Test type', default='none', choices=[('none', ''),
                                                                  ('Negative', 'Negative'),
                                                                  ('Positive', 'Positive')])
    nucleic_name = StringField('Test kit information', description='Necessary for nucleic tests only')
    rapid_id = StringField('Rapid test ID', description='Necessary for rapid tests only.\nUsually found on your test kit.')
    t_test_ctr = StringField('Test centre')
    test = DateTimeLocalField('Test date and time', format='%Y-%m-%dT%H:%M')
    emitent = StringField('Issuer', default='UU Ministry of Certificate Signing')
    joke1=BooleanField('I am a human')
    joke2=BooleanField('I am telling the truth')
    
    

class GenRecForm(FlaskForm):
    fname_print = StringField('Last name')
    gname_print = StringField('First name')
    birth = DateField('Date of birth', format='%Y-%m-%d')
    cert_type=HiddenField(default='r')
    disease_curr = SelectField('Targeted disease', default='none', choices=[('none', ''),
                                                                            ('COVID-19', 'COVID-19')])
    dt_first_pos = DateField('First positive test', format='%Y-%m-%d')
    emitent = StringField('Issuer', default='UU Ministry of Certificate Signing')
    joke1=BooleanField('I am a human')
    joke2=BooleanField('I am telling the truth')


@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/how_it_works')
def how_it_works():
    return render_template("how_it_works.html")

@app.route('/generate')
def gen_opt():
    return render_template("gen_opt.html")

@app.route('/generate/vac', methods=['GET', 'POST'])
def gen_vac():
    form=GenVacForm()
    if form.validate_on_submit():
        ok=1
        for subfield in form:
            if subfield.data=='' or subfield.data=='none':
                ok=0
        if not (form.joke1.data and form.joke2.data):
            ok=0
        if ok:
            filename=gen_function.generare(gname_print=form.gname_print.data, fname_print=form.fname_print.data, birth=form.birth.data, disease_curr=form.disease_curr.data, country='UU', emitent=form.emitent.data,
                                              cert_type='v', vaccine_type_curr=form.vaccine_type_curr.data, manufacturer_curr=form.manufacturer_curr.data, vaccine_prod_curr=form.vaccine_prod_curr.data,
                                              doses_rec=form.doses_rec.data, doses_tot=form.doses_tot.data, dt_last_dose=form.dt_last_dose.data)
            return redirect(url_for('gen_success', filename=filename))
        else:
            return render_template("gen_vac.html", form=form, err=1)
    return render_template("gen_vac.html", form=form, err=0)



@app.route('/generate/test', methods=['GET', 'POST'])
def gen_test():
    form=GenTestForm()
    if form.validate_on_submit():
        ok=1
        for subfield in form:
            if subfield.data=='' or subfield.data=='none':
                if form.test_type_curr.data=='Nucleic' and subfield==form.rapid_id:
                    continue
                if form.test_type_curr.data=='Rapid' and subfield==form.nucleic_name:
                    continue
                ok=0
        if not (form.joke1.data and form.joke2.data):
            ok=0
        if ok:
            from datetime import datetime, timezone
            import pytz
            filename=gen_function.generare(gname_print=form.gname_print.data, fname_print=form.fname_print.data, birth=form.birth.data, disease_curr=form.disease_curr.data, country='UU', emitent=form.emitent.data,
                                           cert_type='t', test_type_curr=form.test_type_curr.data,result_test=form.result_test.data, nucleic_name=form.nucleic_name.data,rapid_id=form.rapid_id.data,t_test_ctr=form.t_test_ctr.data,
                                           test=datetime(form.test.data.year,form.test.data.month,form.test.data.day,form.test.data.hour,form.test.data.minute,form.test.data.second,tzinfo=pytz.timezone('Etc/GMT-2')))
            return redirect(url_for('gen_success', filename=filename))
        else:
            return render_template("gen_test.html", form=form, err=1)
    return render_template("gen_test.html", form=form, err=0)



@app.route('/generate/rec', methods=['GET', 'POST'])
def gen_rec():
    form=GenRecForm()
    if form.validate_on_submit():
        ok=1
        for subfield in form:
            if subfield.data=='' or subfield.data=='none':
                ok=0
        if not (form.joke1.data and form.joke2.data):
            ok=0
        if ok:
            filename=gen_function.generare(gname_print=form.gname_print.data, fname_print=form.fname_print.data, birth=form.birth.data, disease_curr=form.disease_curr.data, country='UU', emitent=form.emitent.data,
                                           cert_type='r', dt_first_pos=form.dt_first_pos.data)
            return redirect(url_for('gen_success', filename=filename))
        else:
            return render_template("gen_rec.html", form=form, err=1)
    return render_template("gen_rec.html", form=form, err=0)



@app.route('/generate/success/<filename>')
def gen_success(filename):
    return render_template("gen_success.html", filename=filename)


if __name__ == '__main__':
    app.run()
