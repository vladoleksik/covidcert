# EUDCC network node
This **unofficial** repository contains a Python applet that verifies an EU digital COVID certificate offline as an educational proof-of-concept for the public key cryptography involved in this decentralised, scalable, secure and reliable system.
For illustrating the full lifecycle of such a certificate, I have designed a possible backend that uses a self-generated key to issue dummy certificates.
**These apps should not be used in official or production use-cases, as they were only designed for the purpose of explaining green passes with a lighschool-level math prerequisite.**

## How it works
Briefly, the verification app starts a local Flask server with a Bootstrap frontend that you can upload images of QR-codes to. The images are read using pyzlib, decoded from base 45, then 
<!--Applets that enable verification of official european digital health certificates and emulates the issuing process and architecture for educational purposes.-->
