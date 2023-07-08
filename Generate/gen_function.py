from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime, timezone, timedelta
import pytz

#UVCI gen start
def genUVCI():
    import random
    import string

    prefix='URN:UVCI:01:UU:'
    prefix_no_colon='URNUVCI01UU'
    pop=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    letters=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    #MAKE SURE IT GETS SEEDED WITH THE CURRENT TIME!!!
    opaque_list=random.choices(population=pop,k=30)
    uvci=''
    for i in opaque_list:
        uvci=uvci+i

    cardNo=prefix_no_colon+uvci
    nDigits = len(cardNo)
    nSum = 0
    isSecond = True
    for i in range(nDigits-1,-1,-1):
        if cardNo[i] in letters:
                d=ord(cardNo[i])-ord('A')
        else:
            d=ord(cardNo[i])-ord('0')+26
        if isSecond:
            d=d*2
        nSum+=d//36
        nSum+=d%36
        isSecond = not isSecond
    dif=(36-nSum%36)%36

    uvci=prefix+uvci+'#'+pop[dif]
    return uvci
#UVCI gen end





def generare(gname_print='Ion-Teodor',fname_print='Ionescu',birth=date(2002,10,12),disease_curr='COVID-19',country='UU',emitent='UU Ministry of Certificate Signing',
             cert_type='v',
             vaccine_type_curr='mRNA',manufacturer_curr='Biontech',vaccine_prod_curr='Pfizer',doses_rec=4,doses_tot=7,dt_last_dose=date(2023,7,11),
             test_type_curr='Rapid',result_test='Negative',nucleic_name='Utopia SARS-CoV-2 Test Kit',rapid_id='1242',t_test_ctr='Utopia COVID-19 Test Centre 148',
             test=datetime(2022,9,15,16,2,19,tzinfo=pytz.timezone('Etc/GMT-2')),
             r_test_ctr='Utopia COVID-19 Test Centre 148',dt_first_pos=date(2022,12,25)):
    #personal data start
    gname=gname_print#
    fname=fname_print#
    fnamet=fname.upper().replace(' ','<').replace('-','<')#
    gnamet=gname.upper().replace(' ','<').replace('-','<')#
    dob_print=birth.strftime('%d-%m-%Y')#
    dob=birth.strftime('%Y-%m-%d')#
    cert_id=genUVCI()
    dt_sgn=datetime.now(tz=pytz.timezone('Etc/GMT-2')).replace(microsecond=0)
    sgn=int(datetime.timestamp(dt_sgn))
    validity=timedelta(770)
    dt_exp=dt_sgn+validity
    exp=int(datetime.timestamp(dt_exp))
    #exp=1788602711
    #sgn=1678014311


    #Vaccine only
    vaccine_type_print=vaccine_type_curr+' Vaccine'#
    last_dose_print=dt_last_dose.strftime('%d-%m-%Y')#
    ult_doza=dt_last_dose.strftime('%Y-%m-%d')#


    vaccine_type={
        'antigen': '1119305005',
        'mRNA': '1119349007',
        'other': 'J07BX03'
        }
    vaccine_prod={
        'Pfizer': 'EU/1/20/1528',
        'Moderna': 'EU/1/20/1507',
        'AstraZeneca': 'EU/1/21/1529',
        'Johnson': 'EU/1/20/1525',
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
        'COVID-19': '840539006',
        }
    manufacturer={
        'Biontech': 'ORG-100030215',
        'Moderna': 'ORG-100031184',
        'AstraZeneca': 'ORG-100001699',
        'Johnson': 'ORG-100001417',
        }
    #Vaccine only


    #Test only
    
    sample_coll_date=test.strftime('%Y-%m-%dT%H:%M:%S%z')#
    sample_coll_date_print=test.strftime('%d-%m-%Y, %H:%M:%S UTC%Z')#

    test_type={
        'Nucleic': 'LP6464-4',
        'Rapid': 'LP217198-3',
        }
    test_res={
        'Negative': '260415000',
        'Positive': '260373001',
        }
    #Test only


    #Recovery only
    imm_start_td=timedelta(11)
    imm_end_td=timedelta(180)
    dt_immun_start=dt_first_pos+imm_start_td
    dt_immun_end=dt_immun_start+imm_end_td
    first_pos_print=dt_first_pos.strftime('%d-%m-%Y')#
    immun_start_print=dt_immun_start.strftime('%d-%m-%Y')#
    immun_end_print=dt_immun_end.strftime('%d-%m-%Y')#
    first_pos=dt_first_pos.strftime('%Y-%m-%d')#
    immun_start=dt_immun_start.strftime('%Y-%m-%d')#
    immun_end=dt_immun_end.strftime('%Y-%m-%d')#
    #Recovery only

    #personal data end


    #Code gen start

    import json
    import zlib
    import cbor2
    from base45 import b45encode
    import qrcode

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

    from cose.messages import Sign1Message

    from cose.keys.curves import P256
    from cose.algorithms import Es256, EdDSA
    from cose.keys.keyparam import KpKty, KpAlg, EC2KpD, EC2KpX, EC2KpY, EC2KpCurve
    from cose.headers import Algorithm, KID
    from cose.keys import CoseKey
    from cose.keys.keytype import KtyEC2

    if cert_type=='v':
        payload={1: country,
                 4: exp,
                 6: sgn,
                 -260:
                     {1:
                        {'v': [{'ci': cert_id,
                                'co': country,
                                'dn': doses_rec,
                                'sd': doses_tot,
                                'dt': ult_doza,
                                'is': emitent,
                                'ma': manufacturer[manufacturer_curr],
                                'mp': vaccine_prod[vaccine_prod_curr],
                                'vp': vaccine_type[vaccine_type_curr],
                                'tg': disease[disease_curr]}],
                         'dob': dob,
                         'nam': {'fn': fname,
                                 'gn': gname,
                                 'fnt': fnamet,
                                 'gnt': gnamet},
                         'ver': '1.3.0'}
                      }
                 }
    elif cert_type=='t':
        if test_type_curr=='Nucleic':
            payload={1: country,
                     4: exp,
                     6: sgn,
                     -260:
                         {1:
                            {'t': [{'ci': cert_id,#
                                    'co': country,#
                                    'tc': t_test_ctr,#
                                    'tr': test_res[result_test],#
                                    'is': emitent,#
                                    'sc': sample_coll_date,#
                                    'nm': nucleic_name,#
                                    'tg': disease[disease_curr],#
                                    'tt': test_type[test_type_curr]}],#
                             'dob': dob,
                             'nam': {'fn': fname,
                                     'gn': gname,
                                     'fnt': fnamet,
                                     'gnt': gnamet},
                             'ver': '1.3.0'}
                          }
                     }
        else:
            payload={1: country,
                     4: exp,
                     6: sgn,
                     -260:
                         {1:
                            {'t': [{'ci': cert_id,#
                                    'co': country,#
                                    'tc': t_test_ctr,#
                                    'tr': test_res[result_test],#
                                    'is': emitent,#
                                    'sc': sample_coll_date,#
                                    'ma': rapid_id,#
                                    'tg': disease[disease_curr],#
                                    'tt': test_type[test_type_curr]}],#
                             'dob': dob,
                             'nam': {'fn': fname,
                                     'gn': gname,
                                     'fnt': fnamet,
                                     'gnt': gnamet},
                             'ver': '1.3.0'}
                          }
                     }
    else:
        payload={1: country,
                 4: exp,
                 6: sgn,
                 -260:
                     {1:
                        {'r': [{'ci': cert_id,#
                                'co': country,#
                                'df': immun_start,#
                                'fr': first_pos,#
                                'is': emitent,#
                                'du': immun_end,#
                                'tg': disease[disease_curr]}],#
                         'dob': dob,
                         'nam': {'fn': fname,
                                 'gn': gname,
                                 'fnt': fnamet,
                                 'gnt': gnamet},
                         'ver': '1.3.0'}
                      }
                 }


    payload=cbor2.dumps(payload)

    with open('cert.pem','rb') as file:
        pem=file.read()
    cert = x509.load_pem_x509_certificate(pem)
    fingerprint = cert.fingerprint(hashes.SHA256())
    key_id=fingerprint[0:8]

    with open('cert.key','rb') as file:
        pem=file.read()
    keyfile=keyfile = load_pem_private_key(pem, password=None)
    priv = keyfile.private_numbers().private_value.to_bytes(32, byteorder="big")


    cose_msg = Sign1Message(phdr={Algorithm: Es256, KID: key_id}, payload=payload)


    cose_key = {
        KpKty: KtyEC2,
        KpAlg: Es256,
        EC2KpCurve: P256,
        EC2KpD: priv,
    }
    cose_msg.key = CoseKey.from_dict(cose_key)
    out = cose_msg.encode()
    out = zlib.compress(out,9)
    out = (b'HC1:'+b45encode(out))
    out = out.decode('ascii')
    if __name__ == '__main__':
        print(out)

    qr=qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
    qr.add_data(out)
    qr.make(fit=True)
    img=qr.make_image(fill_color='#6153ae', back_color='white').convert()
    #print(type(img))
    img.save('coduri/self-sgn-res.png')


    #Code gen end




    #Write image start
    font=ImageFont.truetype('static/fonts/Open_Sans/OpenSans-Light.ttf', size=70)

    if cert_type=='v':
        im1 = Image.open('static/V_cert_template.png')
    elif cert_type=='t':
        im1 = Image.open('static/T_cert_template.png')
    else:
        im1 = Image.open('static/R_cert_template.png')
    cod = Image.open('coduri/self-sgn-res.png').resize((780,780), Image.ANTIALIAS)
    im1.paste(cod, (1517,25,2297,805))

    draw = ImageDraw.Draw(im1)

    draw.text((1138,1440), text=gname_print, anchor='rm', align='right', font=font, fill='black')
    draw.text((2253,1440), text=fname_print, anchor='rm', align='right', font=font, fill='black')
    draw.text((1138,1580), text=dob_print, anchor='rm', align='right', font=font, fill='black')


    draw.text((1138,1970), text=disease_curr, anchor='rm', align='right', font=font, fill='black')

    if cert_type=='v':
        #Vaccine only
        draw.text((2253,1970), text=vaccine_type_print, anchor='rm', align='right', font=font, fill='black')
        draw.text((1138,2110), text=manufacturer_curr, anchor='rm', align='right', font=font, fill='black')
        draw.text((2253,2110), text=vaccine_prod_curr, anchor='rm', align='right', font=font, fill='black')

        draw.text((1043,2255), text=str(doses_rec), anchor='rm', align='right', font=font, fill='black')
        draw.text((1138,2255), text=str(doses_tot), anchor='rm', align='right', font=font, fill='black')
        draw.text((2253,2260), text=last_dose_print, anchor='rm', align='right', font=font, fill='black')
        #Vaccine only
    elif cert_type=='t':
        #Test only
        draw.text((2253,1970), text=test_type_curr, anchor='rm', align='right', font=font, fill='black')
        if test_type_curr=='Nucleic':
            draw.text((2253,2090), text=nucleic_name, anchor='rm', align='right', font=font, fill='black')
        else:
            draw.text((2253,2090), text='Rapid antigen test - id: '+rapid_id, anchor='rm', align='right', font=font, fill='black')

        draw.text((2253,2205), text=t_test_ctr, anchor='rm', align='right', font=font, fill='black')
        draw.text((2253,2320), text=sample_coll_date_print, anchor='rm', align='right', font=font, fill='black')
        #Test only
    else:
        draw.text((2253,1970), text=first_pos_print, anchor='rm', align='right', font=font, fill='black')
        draw.text((1138,2170), text=immun_start_print, anchor='rm', align='right', font=font, fill='black')
        draw.text((2253,2170), text=immun_end_print, anchor='rm', align='right', font=font, fill='black')
        
    font=ImageFont.truetype('static/fonts/Open_Sans/OpenSans-Light.ttf', size=60)
    draw.text((100,2600), text=cert_id, anchor='lm', align='right', font=font, fill='black')
    #write image end
    image_name=cert_id.replace(':','_')+'.png'
    im1.save('static/generated/'+image_name)
    return image_name





def main():
    print(generare(gname_print='Ionut-Andrei',fname_print='Popescu',birth=date(2002,10,12),disease_curr='COVID-19',country='UU',emitent='UU Ministry of Certificate Signing',
             cert_type='r',
             #vaccine_type_curr='mRNA',manufacturer_curr='Biontech',vaccine_prod_curr='Pfizer',doses_rec=4,doses_tot=7,dt_last_dose=date(2023,7,11))) #for vaccine
             #test_type_curr='Nucleic',result_test='Negative',nucleic_name='Utopia SARS-CoV-2 Test Kit Pro',rapid_id='1242',t_test_ctr='Utopia COVID-19 Test Centre 173', #for test
             #test=datetime(2024,9,15,16,2,19,tzinfo=pytz.timezone('Etc/GMT-2')), #for test
             r_test_ctr='Utopia COVID-19 Test Centre 149',dt_first_pos=date(2022,12,25)))
    
if __name__ == '__main__':
    main()
