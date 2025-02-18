from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, URLField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import NumberInput

class ProfileForm(FlaskForm):
    address = StringField("Address", validators=[DataRequired()])
    contact = StringField("Contact Number", validators=[DataRequired()])
    submit = SubmitField("Update Profile")

class WishlistForm(FlaskForm):
    gift_name = StringField("Gift Name", validators=[DataRequired()])
    brand = StringField("Brand", validators=[Optional()])
    model_version = StringField("Model/Version", validators=[Optional()])
    price = DecimalField("Price (in USD)", validators=[Optional()], widget=NumberInput())
    amazon_link = URLField("Amazon Link", validators=[Optional()])
    submit = SubmitField("Add to Wishlist")
