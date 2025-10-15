class Message:

    def __init__(self,from_user,to_user,title,text,status):
        self.from_user = from_user
        self.to_user = to_user
        self.title = title
        self.text = text
        self.status = status

    def to_dict(self):
   
        return {
            "from": self.from_user,
            "to": self.to_user,
            "title": self.title,
            "message": self.text,
            "status": self.status
        }

    def __str__(self):
       
        return f"De: {self.from_user} | Para: {self.to_user} | Título: {self.title} | Status: {self.status}"