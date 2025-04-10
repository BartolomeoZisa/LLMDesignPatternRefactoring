from abc import ABC, abstractmethod

class Review(ABC):
    def get_description(self, uid: str) -> str:
        description = [] 
        if self._merchant_comments:
            description.append(" ".join(self._merchant_comments))  
        
        if uid == "Commission" and self._commission_comments:
            description.append(" ".join(self._commission_comments))  # Add commission comments only for commission members
        
        return " ".join(description)
    
    def __init__(self):        
        self._merchant_comments = []  # Use underscore to make them "private"
        self._commission_comments = []

    def add_merchant_comment(self, comment: str):
        self._merchant_comments.append(comment)
    
    def add_commission_comment(self, comment: str):
        self._commission_comments.append(comment)

    

class Rating(Review):
    def __init__(self, rating: int):
        super().__init__()
        self.rating = rating 

    def get_description(self, uid):
        return (str(self.rating) + " " +  super().get_description(uid)) if super().get_description(uid) else str(self.rating)  
    

