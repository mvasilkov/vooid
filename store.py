import time, base64

from openid.store.nonce import SKEW
from openid.store.interface import OpenIDStore
from openid.association import Association as OIDAssociation

from models import Nonce, Association

class DjangoOpenIDStore(OpenIDStore):
    def __init__(self):
        self.max_nonce_age = 6 * 60 * 60 # Six hours

    def storeAssociation(self, server_url, association):
        Association(
            server_url = server_url,
            handle = association.handle,
            secret = base64.encodestring(association.secret),
            issued = association.issued,
            lifetime = association.issued,
            assoc_type = association.assoc_type
        ).save()

    def getAssociation(self, server_url, handle=None):
        assocs = []

        if handle is not None:
            assocs = Association.objects.filter(
                server_url = server_url, handle = handle
            )
        else:
            assocs = Association.objects.filter(
                server_url = server_url
            )

        if not assocs:
            return None

        associations = []
        for assoc in assocs:
            association = OIDAssociation(
                assoc.handle, base64.decodestring(assoc.secret), assoc.issued,
                assoc.lifetime, assoc.assoc_type
            )
            if association.getExpiresIn() == 0:
                self.removeAssociation(server_url, assoc.handle)
            else:
                associations.append((association.issued, association))

        return len(associations) > 0 and associations[-1][1] or None

    def removeAssociation(self, server_url, handle):
        assocs = Association.objects.filter(
            server_url = server_url, handle = handle
        )
        assocs_exist = assocs.count() > 0
        assocs.delete()
        return assocs_exist


    def useNonce(self, server_url, timestamp, salt):
        if abs(timestamp - time.time()) > SKEW:
            return False

        nonce, created = Nonce.objects.get_or_create(
            server_url=server_url,
            timestam=timestamp,
            salt=salt)

        return created


