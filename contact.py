class Contact:
    def __init__(self, first_name, last_name, email_1="", email_2="", email_3="", phone_1="", phone_2="",
                 phone_3="", phone_4="", phone_5="", address_1="", city_1="", state_1="", zip_1="",
                 country_1="", address_2="", city_2="", state_2="", zip_2="", country_2="", website="",
                 birthday="", last_interaction="", relationship="", middle_name=""):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.email_1 = email_1
        self.email_2 = email_2
        self.email_3 = email_3
        self.phone_1 = phone_1
        self.phone_2 = phone_2
        self.phone_3 = phone_3
        self.phone_4 = phone_4
        self.phone_5 = phone_5
        self.address_1 = address_1
        self.city_1 = city_1
        self.state_1 = state_1
        self.zip_1 = zip_1
        self.country_1 = country_1
        self.address_2 = address_2
        self.city_2 = city_2
        self.state_2 = state_2
        self.zip_2 = zip_2
        self.country_2 = country_2
        self.website = website
        self.birthday = birthday
        self.last_interaction = last_interaction
        self.relationship = relationship
        # Also set relationship_general for compatibility with SQLAlchemy model
        self.relationship_general = relationship

    def to_dict(self):
        return {key: getattr(self, key) for key in vars(self)}