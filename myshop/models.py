from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from multiselectfield import MultiSelectField

STATE_CHOICES = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh ", "Arunachal Pradesh "),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chandigarh", "Chandigarh"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Delhi", "Delhi"),
    ("Daman and Diu", "Daman and Diu"),
    ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu and Kashmir ", "Jammu and Kashmir "),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Lakshadweep", "Lakshadweep"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Puducherry", "Puducherry"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
)

SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
)

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

LABEL_CHOICES = (
    ('New', 'new'),
    ('Bestseller', 'bestseller'),
)

LABEL_COLOR_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

PAYMENT_OPTION_CHOICES = (
    ('Stripe', 'Stripe'),
    ('Paypal', 'Paypal'),
    ('Cash on delivery', 'Cash on delivery'),
)


class Carousel(models.Model):
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.IntegerField(null=True)
    address1 = models.CharField(max_length=200, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(
        max_length=70, choices=STATE_CHOICES, null=True)
    zip_code = models.PositiveIntegerField(null=True)
    profile_image = models.ImageField(
        upload_to='images', default='images/user1.jpg', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_image.path)

        if img.width > 150 or img.height > 150:
            new_img = (150, 150)
            img.thumbnail(new_img)
            img.save(self.profile_image.path)


class Category(models.Model):
    category = models.CharField(max_length=15)

    def __str__(self):
        return self.category


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discounted_price = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    tag = models.CharField(choices=LABEL_CHOICES,
                           max_length=15, blank=True, null=True)
    label = models.CharField(choices=LABEL_COLOR_CHOICES,
                             max_length=1, blank=True, null=True)
    brand = models.CharField(max_length=50)
    size = MultiSelectField(choices=SIZE_CHOICES, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 300 or img.height > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)


class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.product.title)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    prod_size = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=3, blank=True, null=True)
    payment_option = models.CharField(
        max_length=50, choices=PAYMENT_OPTION_CHOICES, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.id)

    @property
    def total_cost_of_product(self):
        if self.product.discounted_price:
            item_cost = self.product.discounted_price
        else:
            item_cost = self.product.price
        return self.quantity * item_cost


class Review(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
