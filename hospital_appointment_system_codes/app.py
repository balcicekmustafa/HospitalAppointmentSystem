from flask import Flask, request, session, flash, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_guvenlik_anahtari'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:M.mustafa27@localhost/hastane'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Hasta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sifre = db.Column(db.String(100), nullable=False)

    randevular = db.relationship('Randevu', backref='hasta', lazy=True)
    raporlar_receteler = db.relationship('RaporRecete', backref='hasta_owner', lazy=True)

    def __repr__(self):
        return f'<Hasta {self.ad} {self.soyad}>'

class Doktor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sifre = db.Column(db.String(100), nullable=False)
    alan = db.Column(db.String(100))

    randevular = db.relationship('Randevu', backref='doktor', lazy=True)
    raporlar_receteler = db.relationship('RaporRecete', backref='doktor_owner', lazy=True)

    def __repr__(self):
        return f'<Doktor {self.ad} {self.soyad}>'

class Randevu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hasta_id = db.Column(db.Integer, db.ForeignKey('hasta.id'), nullable=False)
    doktor_id = db.Column(db.Integer, db.ForeignKey('doktor.id'), nullable=False)
    tarih = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    durum = db.Column(db.String(50), default='Planlandı')  # 'Planlandı', 'Tamamlandı', 'İptal Edildi'

    def __repr__(self):
        return f'<Randevu {self.id}>'

class RaporRecete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doktor_id = db.Column(db.Integer, db.ForeignKey('doktor.id'), nullable=False)
    hasta_id = db.Column(db.Integer, db.ForeignKey('hasta.id'), nullable=False)
    tip = db.Column(db.String(50), nullable=False)  # 'rapor' veya 'reçete'
    icerik = db.Column(db.Text, nullable=False)
    tarih = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<RaporRecete {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hasta_kayit', methods=['GET', 'POST'])
def hasta_kayit():
    if request.method == 'POST':
        ad = request.form['ad']
        soyad = request.form['soyad']
        email = request.form['email']
        sifre = request.form['sifre']

        yeni_hasta = Hasta(ad=ad, soyad=soyad, email=email, sifre=sifre)
        db.session.add(yeni_hasta)
        db.session.commit()

        flash('Kayıt başarıyla tamamlandı. Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('hasta_giris'))

    return render_template('hasta_kayit.html')

@app.route('/hasta_giris', methods=['GET', 'POST'])
def hasta_giris():
    if request.method == 'POST':
        email = request.form['email']
        sifre = request.form['sifre']

        hasta = Hasta.query.filter_by(email=email, sifre=sifre).first()
        if hasta:
            session['user_id'] = hasta.id
            session['tip'] = 'hasta'
            flash('Başarıyla giriş yaptınız.', 'success')
            return redirect(url_for('hasta_paneli'))

        flash('Geçersiz kullanıcı adı veya şifre. Lütfen tekrar deneyin.', 'danger')

    return render_template('hasta_giris.html')

@app.route('/hasta_paneli')
def hasta_paneli():
    if 'user_id' not in session or session['tip'] != 'hasta':
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('hasta_giris'))

    user_id = session['user_id']
    current_user = Hasta.query.get(user_id)
    randevular = Randevu.query.filter_by(hasta_id=user_id).order_by(Randevu.tarih.desc()).all()
    raporlar_receteler = RaporRecete.query.filter_by(hasta_id=user_id).order_by(RaporRecete.tarih.desc()).all()

    return render_template('hasta_paneli.html', current_user=current_user, randevular=randevular, raporlar_receteler=raporlar_receteler)
@app.route('/doktor_kayit', methods=['GET', 'POST'])
def doktor_kayit():
    if request.method == 'POST':
        ad = request.form['ad']
        soyad = request.form['soyad']
        email = request.form['email']
        sifre = request.form['sifre']
        alan = request.form['alan']

        yeni_doktor = Doktor(ad=ad, soyad=soyad, email=email, sifre=sifre, alan=alan)
        db.session.add(yeni_doktor)
        db.session.commit()

        flash('Doktor kaydı başarıyla tamamlandı. Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('doktor_giris'))

    return render_template('doktor_kayit.html')


@app.route('/doktor_giris', methods=['GET', 'POST'])
def doktor_giris():
    if request.method == 'POST':
        email = request.form['email']
        sifre = request.form['sifre']

        doktor = Doktor.query.filter_by(email=email, sifre=sifre).first()
        if doktor:
            session['user_id'] = doktor.id
            session['tip'] = 'doktor'
            flash('Başarıyla giriş yaptınız.', 'success')
            return redirect(url_for('doktor_paneli'))

        flash('Geçersiz kullanıcı adı veya şifre. Lütfen tekrar deneyin.', 'danger')

    return render_template('doktor_giris.html')

@app.route('/doktor_paneli')
def doktor_paneli():
    if 'user_id' not in session or session['tip'] != 'doktor':
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('doktor_giris'))

    doktor_id = session['user_id']
    current_user = Doktor.query.get(doktor_id)
    randevular = Randevu.query.filter_by(doktor_id=doktor_id).order_by(Randevu.tarih.desc()).all()
    raporlar_receteler = RaporRecete.query.filter_by(doktor_id=doktor_id).order_by(RaporRecete.tarih.desc()).all()

    # Tüm hastaları getir
    patients = Hasta.query.all()

    return render_template('doktor_paneli.html', current_user=current_user, randevular=randevular, patients=patients)
@app.route('/raporlar_receteler/<int:doktor_id>')
def raporlar_receteler(doktor_id):
    if 'user_id' not in session or session['tip'] != 'doktor' or session['user_id'] != doktor_id:
        flash('Bu sayfayı görüntülemek için yetkiniz bulunmamaktadır.', 'warning')
        return redirect(url_for('doktor_giris'))

    raporlar_receteler = RaporRecete.query.filter_by(doktor_id=doktor_id).order_by(RaporRecete.tarih.desc()).all()
    return render_template('raporlar_receteler.html', raporlar_receteler=raporlar_receteler)


@app.route('/rapor_recete_ekle/<int:hasta_id>', methods=['GET', 'POST'])
def rapor_recete_ekle(hasta_id):
    if 'user_id' not in session or session['tip'] != 'doktor':
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('doktor_giris'))

    if request.method == 'POST':
        tip = request.form['tip']
        icerik = request.form['icerik']

        yeni_rapor_recete = RaporRecete(doktor_id=session['user_id'], hasta_id=hasta_id, tip=tip, icerik=icerik)
        db.session.add(yeni_rapor_recete)
        db.session.commit()

        flash('Rapor veya reçete başarıyla eklendi.', 'success')
        return redirect(url_for('doktor_paneli'))

    hastalar = Hasta.query.all()
    return render_template('rapor_recete_ekle.html', hastalar=hastalar)


@app.route('/randevu_al', methods=['GET', 'POST'])
def randevu_al():
    if 'user_id' not in session or session['tip'] != 'hasta':
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('hasta_giris'))

    if request.method == 'POST':
        doktor_id = request.form['doktor_id']
        tarih_str = request.form['tarih']
        tarih = datetime.strptime(tarih_str, '%Y-%m-%dT%H:%M')

        yeni_randevu = Randevu(hasta_id=session['user_id'], doktor_id=doktor_id, tarih=tarih)
        db.session.add(yeni_randevu)
        db.session.commit()

        flash('Randevu başarıyla alındı.', 'success')
        return redirect(url_for('hasta_paneli'))

    doktorlar = Doktor.query.all()
    return render_template('randevu_al.html', doktorlar=doktorlar)


@app.route('/randevu_iptal/<int:randevu_id>', methods=['POST'])
def randevu_iptal(randevu_id):
    if 'user_id' not in session:
        flash('Bu işlemi gerçekleştirmek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('hasta_giris'))  # Redirect to patient login page

    randevu = Randevu.query.get(randevu_id)

    # Check if the logged-in user is either a patient or a doctor
    if session['tip'] == 'hasta':
        # Check if the patient owns the appointment
        if randevu and randevu.hasta_id == session['user_id']:
            randevu.durum = 'İptal Edildi'
            db.session.commit()
            flash('Randevu başarıyla iptal edildi.', 'success')
        else:
            flash('Randevu iptali başarısız. Bu randevuyu iptal etme yetkiniz bulunmamaktadır.', 'danger')

        return redirect(url_for('hasta_paneli'))

    elif session['tip'] == 'doktor':
        # Check if the doctor is assigned to the appointment
        if randevu and randevu.doktor_id == session['user_id']:
            randevu.durum = 'İptal Edildi'
            db.session.commit()
            flash('Randevu başarıyla iptal edildi.', 'success')
        else:
            flash('Randevu iptali başarısız. Bu randevuyu iptal etme yetkiniz bulunmamaktadır.', 'danger')

        return redirect(url_for('doktor_paneli'))

@app.route('/hasta_rapor_receteler/<int:hasta_id>')
def hasta_rapor_receteler(hasta_id):
    if 'user_id' not in session or session['tip'] != 'doktor':
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('doktor_giris'))

    # Check if the logged-in doctor has access to the patient's reports and prescriptions
    doktor_id = session['user_id']
    patient = Hasta.query.get(hasta_id)
    if not patient:
        flash('Geçersiz hasta bilgisi.', 'danger')
        return redirect(url_for('doktor_paneli'))

    # Fetch reports and prescriptions for the patient
    raporlar_receteler = RaporRecete.query.filter_by(hasta_id=hasta_id).order_by(RaporRecete.tarih.desc()).all()

    return render_template('hasta_rapor_receteler.html', patient=patient, raporlar_receteler=raporlar_receteler)

@app.route('/cikis')
def cikis():
    session.pop('user_id', None)
    session.pop('tip', None)
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
