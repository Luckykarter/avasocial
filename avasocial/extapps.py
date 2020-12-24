from pyhunter import PyHunter
import clearbit


class ClearBit:
    def __init__(self, api_key):
        self.clearbit = clearbit
        self.clearbit.key = api_key

    class PersonData:
        def __init__(self, email):
            try:
                data = clearbit.Enrichment.find(email=email, stream=True)
                response = dict(data)
            except Exception as e:
                response = {}

            response = response.get('person', {})
            name_data = response.get('name', {})
            geo_data = response.get('geo', {})

            self.name = self._get_value(name_data, 'givenName')
            self.surname = self._get_value(name_data, 'familyName')
            self.country = self._get_value(geo_data, 'country')
            self.city = self._get_value(geo_data, 'city')
            self.site = self._get_value(response, 'site')
            self.avatar_link = self._get_value(response, 'avatar')
            self.employment = self._get_value(response.get('employment', {}), 'name')

        def _get_value(self, data, token):
            res = data.get(token)
            return res if res else ''


class Hunter(PyHunter):
    def __init__(self, api_key):
        super().__init__(api_key)

    def ismailvalid(self, email):
        """
        Verifies e-mail using service Hunter.
        If there is an issue in response - e-mail considered invalid

        :param email: e-mail address to validate
        :return: True if e-mail is valid, False - otherwise
        """

        validation = self.email_verifier(email)
        return not (validation.get('status', 'invalid') == 'invalid')
