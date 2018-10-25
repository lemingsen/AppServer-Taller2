"""Util for connecting and decode firebase tokens"""
import firebase_admin
# pylint: disable=R0903


class Firebase:
    """Firebase_admin wrapper for decoding firebase token"""
    def __init__(self, certificate):
        try:
            self.app = firebase_admin.get_app()
        except ValueError:
            cred = firebase_admin.credentials.Certificate(certificate)
            self.app = firebase_admin.initialize_app(cred)

    def decode_token(self, id_token):
        """Decodes firebase token"""
        decoded_token = firebase_admin.auth.verify_id_token\
            (id_token['idToken'], self.app, check_revoked=True)
        return decoded_token['uid']
