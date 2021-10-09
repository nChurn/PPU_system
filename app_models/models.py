from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomAccManager
# Create your models here.
class Acc(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=31, null=True, blank=True)
    last_name = models.CharField(max_length=31, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_moder = models.BooleanField(default=False)
    is_secretar = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)
    is_vned = models.BooleanField(default=False)
    is_analit = models.BooleanField(default=False)

    objects = CustomAccManager()

    moder = models.ForeignKey('self', related_name='acc_moderat', on_delete=models.DO_NOTHING, null=True, blank=True)
    
#    acc_id = models.IntegerField(primary_key=True, default=1)
#    id = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'username']

    class Meta:
        db_table = 'acc'

    def save(self, *args, **kwargs):
        print(self.is_moder)
#        if self.is_moder:
#            print('aaaa')
#            raise ValueError("moder has not moder")


        print(self.id)
        return super(Acc, self).save(*args, **kwargs)

    def get_moder_ppus(self):
        return PPU.objects.filter(moder=self.id)
        
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.last_name + " " + self.first_name

    def get_all_owners(self):
        return Acc.objects.filter(moder=self.username)


class Category(models.Model):
    title = models.CharField(max_length=63)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.title

class Effect(models.Model):
    title = models.CharField(max_length=63)

    class Meta:
        db_table = 'effect'

    def __str__(self):
        return self.title


class PPU(models.Model):
    STATUS_CHOICES = [
        ('1', 'first_checking'),
        # проверка первым модером
        ('2', 'second_checking'),
        # проверка вторым модером
        ('3', 'expert_checking'),
        # проверка группой экспертов
        ('4', "need_update"),
        # отправлено на доработку
        ('5', 'execution'),
        # выполняется
        ('6', 'finalized'),  
        # выполнено
        ('7', 'denied'),     
        # отказано
    ]

    title = models.CharField(max_length=63, unique=True)
    problem = models.TextField()
    solution = models.TextField()

    file = models.FileField(upload_to='pppus/files/', blank=True, null=True)


    author = models.ForeignKey(Acc, related_name = 'author', on_delete=models.CASCADE)
    co_author = models.ForeignKey(Acc, related_name='co_author', on_delete=models.CASCADE, blank=True, null=True)
    co_author_procent = models.CharField(max_length=2, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)

    status = models.CharField(max_length=63, choices=STATUS_CHOICES, default=1)

    moder = models.ForeignKey(Acc, related_name='ppu_moder', on_delete=models.DO_NOTHING, blank=True, null=True)

    deadlines = models.DateTimeField(null=True, blank=True)
    vned = models.ForeignKey(Acc, on_delete=models.DO_NOTHING, related_name='vned', blank=True, null=True)

    class Meta:
        db_table = 'ppu'


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if self.co_author and not self.co_author_procent:
            raise ValueError('set co_author_procent before save object')

        if self.status == 1:
            self.moder = self.author.moder
        

    #    moder = self.author.

        return super(PPU, self).save(*args, **kwargs)

    def owners(self):
        if self.co_author:
            return [self.author.username, self.co_author.username]
        else:
            return [self.author.username]

"""
class VnedPPU(models.Model):
    title = models.CharField(max_length=63, unique=True)
    problem = models.TextField()
    solution = models.TextField()

    file = models.FileField(upload_to='pppus/files/', blank=True, null=True)


    author = models.ForeignKey(Acc, related_name = 'vned_author', on_delete=models.CASCADE)
    co_author = models.ForeignKey(Acc, related_name='vned_co_author', on_delete=models.CASCADE, blank=True, null=True)
    co_author_procent = models.CharField(max_length=2, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)


    moder = models.ForeignKey(Acc, related_name='vned_moder', on_delete=models.DO_NOTHING, blank=True, null=True)


    deadline = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
#    id = 
#    vned_id = models.IntegerField(primary_key=True)
#    ppu = models.ForeignKey(PPU, on_delete=models.PROTECT, related_name='ppu_proto', null=True, blank=True)
    #vned_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return "vned: " + self.title 

    def save(self, *args, **kwargs):
        #self.id += 1
        return super(VnedPPU, self).save(*args, **kwargs)
"""