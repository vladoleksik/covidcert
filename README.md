# EUDCC network node
![image](https://img.shields.io/badge/License-MIT-green) ![image](https://img.shields.io/badge/Python-3.10-blue)
<!--Applets that enable verification of official european digital health certificates and emulates the issuing process and architecture for educational purposes.-->
This **unofficial** repository contains a Python applet that verifies an EU digital COVID certificate offline as an educational proof-of-concept for the public key cryptography involved in this decentralised, scalable, secure and reliable system.
For illustrating the full lifecycle of such a certificate, I have designed a possible backend that uses a self-generated key to issue dummy certificates.\
**These apps should not be used in official or production use-cases, as they were only designed for the purpose of explaining green passes with a lighschool-level math prerequisite.**

## How it works
The following part will assume some degree of familiarity with public key cryptography and algorithms such as RSA, ECDSA and SHA.

### Verification
Briefly, the verification app starts a local Flask server with a Bootstrap frontend that you can upload images of QR-codes to. The images are read using pyzlib, decoded from base 45. What resultys is a .zip file data, that can be extracted to another byte array, representing a COSE message.\
This message has four fields:
- *Protected header*, which stores the following data:
  - *Algortithm* &ndash; name of the algorithm used to digitally sign the certificate;
  - *KID* &ndash; the identifier of the key that was used to sign the data in the certificate;
- *Unprotected header*, which is left empty;
- *Payload*, which contains the relavant data &ndash; in this case, the holder health data;
- *Signature*, which holds the data needed to confirm that the relevant authority approves of the data and guarantees its integrity.
Using the KID to identify the authority who supposedly signed the data, the app looks through a .json list it fetched from [the address used by French app Sanipasse](https://raw.githubusercontent.com/lovasoa/sanipasse/master/src/assets/Digital_Green_Certificate_Signing_Keys.json) &ndash; thank you, by the way :).
There, it should find the data of the one who holds said key and fetch the public key (the number used to easily authentify everything signed by the holder). Using this key, it then cryptographically validates the certificate by matching two values: one obtained by encrypting the signature and another one by computing the hash of the payload. If they match, the certificate is valid. If *anything* fails, the certificate is invalid.
A valid certificate has its payload taken and decoded from its CBOR format, resulting in a JSON (*techincally, it all is a JSON Web Token*) string that holds all the data the certificates needs to store and... well, certify.

### Issuing
The counterpart of the first application takes a dummy cryptographic key and acquires from the user some personal data via the frontend interface created with the Flask server. It packs the data into a JSON string, with a randomly generated ID and computed date and time, signs the payload, packs it into a COSE message to then archive as .zip, encode in base 45, prepend "HC1:" to, and present as a QR-code, essentially doing all the work of the first app in reverse to show that such a network has no active parts that are loaded with an enormous volume of requests, even for a planet-scale application.

## How to install
**You should first and foremost note that, while no restrictions are being imposed regarding to the use of these apps, they are provided as-is, with little-to-no regard to compatibility and making it work on your device is up to you.**
Still, here's a short (quite simplified) list of steps needed to hopefully get the app up and running:
1. Make sure you have Python installed.
2. Make sure all the dependencies in ```requirements.txt``` are installed.
3. Clone this repository somewhere on your filesystem.
4. Replace the ```Generate\cert.key``` file with an **ECDSA (ECDH P-256) private key** you generate. When in doubt, you can use [this site](https://certificatetools.com).
5. Replace the ```Generate\cert.pem``` and ```Check\cert.pem``` files with the corresponding public key for the above private key, so that the verification app can recognise the certificates issued by its counterpart app.
6. Open a command line and run ```app_generate.py``` or ```app_scan.py```, depending on qhat you need. The localhost address you should access is communicated to you. Enjoy!
