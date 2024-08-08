from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField

class Author(Document):
    fullname = StringField(max_length=50)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    created_at = DateTimeField(required=True)

    def __str__(self):
        return self.fullname

class Tag(Document):
    name = StringField(max_length=60, unique=True)

    def __str__(self):
        return self.name

class Quote(Document):
    quote = StringField()
    tags = ListField(ReferenceField(Tag))
    author = ReferenceField(Author)
    created_at = DateTimeField(required=True)

    def __str__(self):
        return self.quote