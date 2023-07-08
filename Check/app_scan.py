from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet
import scan_to_dict
from datetime import datetime



vaccine_type={
    '1119305005': 'Antigen Vaccine',
    '1119349007': 'mRNA Vaccine',
    'J07BX03': 'Other vaccine'
    }
vaccine_prod={
    'EU/1/20/1528': 'Pfizer (Comirnaty)',
    'EU/1/20/1507': 'Moderna (Spikevax)',
    'EU/1/21/1529': 'AstraZeneca (Vaxzevria)',
    'EU/1/20/1525': 'Johnson (Janssen)',
    'CoronaVac': 'CoronaVac',
    'Covishield': 'Covishield',
    'Covaxin': 'Covaxin',
    'CVnCoV': 'CVnCoV',
    'NVX-CoV2373': 'NVX-CoV2373',
    'Sputnik-V': 'Sputnik-V',
    'Convidecia': 'Convidecia',
    'EpiVacCorona': 'EpiVacCorona',
    'BBIBP-CorV': 'BBIBP-CorV',
    'InactivatedSARS-CoV-2-Vero-Cell': 'InactivatedSARS-CoV-2-Vero-Cell',
    }
disease={
    '840539006': 'COVID-19',
    }
manufacturer={
    'ORG-100030215': 'Biontech',
    'ORG-100031184': 'Moderna',
    'ORG-100001699': 'AstraZeneca',
    'ORG-100001417': 'Johnson',
    }




test_type={
    'LP6464-4': 'Nucleic acid amplification test',
    'LP217198-3': 'Rapid antigen test',
    }
test_res={
    '260415000': 'Negative',
    '260373001': 'Positive',
    }











app = Flask(__name__)
app.config['SECRET_KEY']='aabcehm'
app.config['UPLOADED_IMAGES_DEST']='uploads'

images=UploadSet('images', IMAGES)
configure_uploads(app, images)

class CertUploadForm(FlaskForm):
    cert_file = FileField('Health certificate')

@app.route('/')
def index():
    return redirect(url_for("home"))


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/how_it_works')
def how_it_works():
    return render_template("how_it_works.html")


@app.route('/scan', methods=['GET','POST'])
def upload():
    form = CertUploadForm()
    if form.validate_on_submit():
        ok=0
        try:
            filename=images.save(form.cert_file.data)
            cert_data=scan_to_dict.scan('uploads/'+filename)
            ok=1
        except:
            return render_template("details_err.html", data={'err':'Upload error',
                                                             'status':-1,
                                                             'content':''})
        if cert_data['status'] == -1:
            return render_template("details_err.html", data=cert_data)
        if 'v' in cert_data['payload'][-260][1]:
            return render_template("details_vac.html", datetime=datetime, data=cert_data, vaccine_prod=vaccine_prod, vaccine_type=vaccine_type, manufacturer=manufacturer, disease=disease)
        if 't' in cert_data['payload'][-260][1]:
            return render_template("details_test.html", datetime=datetime, data=cert_data, test_type=test_type, test_res=test_res, disease=disease)
        if 'r' in cert_data['payload'][-260][1]:
            return render_template("details_rec.html", datetime=datetime, data=cert_data, disease=disease)

        return render_template("details_err.html", data={'err':'Parse error',
                                                             'status':-1,
                                                             'content':cert_data})
    return render_template("upload.html", form=form, err=0)


def main():
    app.run()


if __name__ == '__main__':
    main()
