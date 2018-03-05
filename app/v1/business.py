from flask import Flask

BUSINESS = {}


class businesses():
    def __init__(self, businessId, businessName, category, location, email):
        self.businessId = businessId
        self.businessName = businessName
        self.category = category
        self.location = location
        self.created_by = email