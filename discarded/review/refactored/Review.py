from abc import abstractmethod


class Review:
    @abstractmethod
    def get_description(self, uid: str) -> str:
        pass
    
    #TODO this doesn't work
    def add_merchant_comment(self, comment: str):
        self = MerchantComment(self, comment)
    
    def add_commission_comment(self, comment: str):
        self = CommissionComment(self, comment)

class Rating(Review):
    def __init__(self, rating: int):
        self.rating = rating

    def get_description(self, uid: str) -> str:
        return str(self.rating)
    

class Comment(Review):
    def __init__(self, comment: str):
        self.comment = comment

    def get_description(self, uid: str) -> str:
        return self.comment

class MerchantComment(Comment):
    def __init__(self, review: Review, comment: str):
        super().__init__(comment)
        self.review = review

    def get_description(self, uid: str) -> str:
        return self.review.get_description(uid) + " " + self.comment

class CommissionComment(Comment):
    def __init__(self, review: Review, comment: str):
        super().__init__(comment)
        self.review = review

    def get_description(self, uid: str) -> str:
        if uid == "Commission":
            return self.review.get_description(uid) + " " + self.comment
        else:
            return self.review.get_description(uid)
