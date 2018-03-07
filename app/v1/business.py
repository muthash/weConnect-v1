from flask import Flask

class Business():
    def __init__(self, businessId, businessName, category, location, created_by):
        self.businessId = businessId
        self.businessName = businessName
        self.category = category
        self.location = location
        self.created_by = created_by
        self.reviews = []

    def __str__(self):
        business = {'businessId': self.businessId,
                    'businessName': self.businessName,
                    'category': self.category,
                    'location': self.location,
                    'created_by': self.created_by 
        }
        return business