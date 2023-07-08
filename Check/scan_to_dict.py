import cv2
from pyzbar.pyzbar import decode

import base64
from base45 import b45decode
import zlib

from typing import Dict, Tuple

from cose.messages import CoseMessage
from cose.headers import Algorithm, KID
from cose.keys import CoseKey, ec2, curves, keyops
from cose import algorithms
import cbor2

import json

from cryptojwt import jwk as cjwtk
from cryptojwt import utils as cjwt_utils
from pyasn1.codec.ber import decoder as asn1_decoder


from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cose.algorithms import Es256
from cose.keys.curves import P256
from cose.algorithms import Es256, EdDSA, Ps256
from cose.keys.keyparam import KpAlg, EC2KpX, EC2KpY, EC2KpCurve, RSAKpE, RSAKpN
from cose.keys.keyparam import KpKty
from cose.keys.keytype import KtyEC2, KtyRSA


#fisier_de_citit='coduri/Test_valid.png'
#fisier_de_citit='URN_UVCI_01_UU_XQTHFMET40428Q2C7A6QP6VYBAIIA3#O.png'

#Nu atinge
def public_ec_key_points(public_key: bytes) -> Tuple[str, str]:
    # This code adapted from: https://stackoverflow.com/a/59537764/1548275
    public_key_asn1, _remainder = asn1_decoder.decode(public_key)
    public_key_bytes = public_key_asn1[1].asOctets()

    off = 0
    if public_key_bytes[off] != 0x04:
        raise ValueError("EC public key is not an uncompressed point")
    off += 1

    size_bytes = (len(public_key_bytes) - 1) // 2

    x_bin = public_key_bytes[off:off + size_bytes]
    x = int.from_bytes(x_bin, 'big', signed=False)
    off += size_bytes

    y_bin = public_key_bytes[off:off + size_bytes]
    y = int.from_bytes(y_bin, 'big', signed=False)
    off += size_bytes

    bl = (x.bit_length() + 7) // 8
    bytes_val = x.to_bytes(bl, 'big')
    x_str = base64.b64encode(bytes_val, altchars='-_'.encode()).decode()

    bl = (y.bit_length() + 7) // 8
    bytes_val = y.to_bytes(bl, 'big')
    y_str = base64.b64encode(bytes_val, altchars='-_'.encode()).decode()

    return x_str, y_str
#Nu atinge

def chk_sgn(text):
    if text.startswith('HC'):
        text = text[3:]
        if text.startswith(':'):
            text = text[1:]
    try:
        text = b45decode(text)
    except:
        #print("Not an EU DCC!")
        return {'status':-1,
                'err':'Unable to decode Base 45.',
                'content':text}
    if __name__ == '__main__':
        print(bytearray(text).hex())

    try:
        text = zlib.decompress(text)
    except:
        #print("Not an EU DCC!")
        return {'status':-1,
                'err':'Unable to unzip content.',
                'content':text}
    if __name__ == '__main__':
        print(text)

    try:   
        msg = CoseMessage.decode(text)
    except:
        #print("Not an EU DCC!")
        return {'status':-1,
                'err':'Unable to get CBOR Web Token payload.',
                'content':text}
    
    try:   
        cbor = cbor2.loads(msg.payload)
    except:
        #print("Not an EU DCC!")
        return {'status':-1,
                'err':'Unable to get CBOR Web Token payload.',
                'content':msg}
    if __name__ == '__main__':
        print(cbor)

    if KID in msg.phdr:
        key_id = msg.phdr[KID]
    elif KID in msg.uhdr:
        key_id = msg.uhdr[KID]
    else:
        return {'status':0,
                'err':'Certificate is unsigned.',
                'payload':cbor}

    key_id=base64.b64encode(key_id)

    #print(key_id)

    #Avem key-id-ul
    #m6so0I2uIyw=   test
    #hA1+pwEOxCI=   buna



    #print(cbor)
    #Avem datele despre certificat, il parsam (in viitor)

    ok=0
    valid_EU=0
    #Verificam daca exista o semnatura a UE
    EU_file=1
    try:
        with open("list_EU.json", encoding="utf-8") as file:
            EU_keys = json.load(file)
    except:
        #print("No EU keys file!")
        EU_file=0
    
    if EU_file==1:
        for test_id,test_data in EU_keys.items():
            test_id_64=base64.b64encode(base64.b64decode(test_id))
            #print(key_id,test_id_64)
            if key_id==test_id_64:
                #print("Found an EU key!")
                EU_issuer=test_data['issuer']
                x,y = public_ec_key_points(base64.b64decode(test_data['publicKeyPem']))
                jwk_dict = {'crv': test_data['publicKeyAlgorithm']['namedCurve'],
                            'kid': key_id.hex(),
                            'kty': test_data['publicKeyAlgorithm']['name'][:2],
                            'x': x,
                            'y': y,
                            }
                if jwk_dict['kty']!='EC' or jwk_dict['crv']!='P-256':
                    #print("Key not supported")
                    continue
                cose_key = ec2.EC2(
                    crv=curves.P256,
                    x=cjwt_utils.b64d(jwk_dict["x"].encode()),
                    y=cjwt_utils.b64d(jwk_dict["y"].encode()),
                    )
                cose_key.key_ops = [keyops.VerifyOp]
                cose_key.kid = bytes(jwk_dict["kid"], "UTF-8")
                #print(cose_key)
                ok=1
                break

    if ok:
        msg.key = cose_key
        if not msg.verify_signature():
            #print("EU key {0} does not match.".format(cose_key.kid.decode()))
            ok=0
        else:
            ok=1
            valid_EU=1
    else:
        #print("No EU signature")
        pass
    #Am incercat sa verificam semnatura unei autoritati UE, altfel incercam semnatura Utopia

    if valid_EU:
        #print("EU Signature OK!")
        return {'status':2,
                'iss':EU_issuer,
                'kid':key_id.decode('ASCII'),
                'payload':cbor}



    #Incercam sa verificam cu certificatul nostru cert.pem
    Utopia_file=1
    try:
        with open('cert.pem', "rb") as file:
            pem = file.read()
        cert = x509.load_pem_x509_certificate(pem)
        pub = cert.public_key().public_numbers()
    except:
        Utopia_file=0

    if Utopia_file==0:
        #print("No Utopia signature.")
        return {'status':0,
                'iss':'Unknown issuer',
                'kid':key_id.decode('ASCII'),
                'payload':cbor}

    fingerprint = cert.fingerprint(hashes.SHA256())
    keyid = fingerprint[0:8]
    keyid_b64 = base64.b64encode(keyid)
    #print(keyid_b64,key_id)

    if keyid_b64==key_id:
        #print("Found matching Utopia certificate!")
        key_cert = CoseKey.from_dict(
            {
                KpKty: KtyEC2,
                EC2KpCurve: P256,
                KpAlg: Es256,
                EC2KpX: pub.x.to_bytes(32, byteorder="big"),
                EC2KpY: pub.y.to_bytes(32, byteorder="big")
            }
        )
        #print(key_cert)
        msg.key=key_cert
        if not msg.verify_signature():
            #print("Utopia key {0} does not match.".format(key_cert.kid.decode()))
            ok=0
        else:
            #print("Utopia Signature OK!")
            ok=1
    else:
        #print("No Utopia signature")
        pass

    if ok==0:
        #print("Unable to verify signature - certificate not trustworthy!")
        return {'status':0,
                'iss':'Unknown issuer',
                'kid':key_id.decode('ASCII'),
                'payload':cbor}
    else:
        return {'status':1,
                'iss':'C=UU, O=Mystery of Certificate Signing, 2.5.4.5=001, CN=Utopian Union Certificate Authority',
                'kid':key_id.decode('ASCII'),
                'payload':cbor}

def scan(fisier_de_citit):
    have_data=0
    try:
        img = cv2.imread(fisier_de_citit)
        cod = decode(img)
        text = cod[0].data.decode('ASCII')
        have_data=1
    except:
        result={'status':-1,
                'err':'No QR-Code in uploaded image.',
                'content': ''}
    if have_data:
        result=chk_sgn(text)
    return result


def main():
    print(json.dumps(scan('self-sgn-res.png'), indent=2))

if __name__ == '__main__':
    main()
