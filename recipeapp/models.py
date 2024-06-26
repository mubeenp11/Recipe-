from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/')
    date = models.DateField()
    view=models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True) 
  
    def __str__(self):
        return self.title
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True) 
    class Meta:
        unique_together =['user', 'recipe']
    def __str__(self):
        return f'feedback by {self.user.username} on {self.recipe.title}'
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Notification for {self.user.username}: {self.message}"


  

