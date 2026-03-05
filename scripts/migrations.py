from cloudinary.uploader import upload
from blog.models import Article


for a in Article.objects.all():
    # si l'image est encore en locale
    if str(a.image).startswith('media/'):
        result = upload(a.image.path)
        a.image = result['secure_url']
        a.save()
        print(f"Image de l'article '{a.titre}' migrée vers Cloudinary.")