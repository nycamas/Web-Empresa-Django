from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        ordering = ['created']

class ThreadManager(models.Manager):
    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2) # self = thread.Objects.all()
        if len(queryset)>0:
            return queryset[0]
        return None
    
    def find_or_create(self, user1, user2):
        thread= self.find(user1, user2)
        if thread is None:
            thread= Thread.objects.create()
            thread.users.add(user1, user2)
        return thread        
        
class Thread(models.Model):
    users = models.ManyToManyField(User,related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")
    
    objects = ThreadManager()
    #Tread.objects
    class Meta:
        ordering = ['-updated']
        
    
    
def messages_changed(sender, **kwargs):
        instance=kwargs.pop("instance", None) # la instancia del hilo
        action=kwargs.pop("action", None)
        pk_set=kwargs.pop("pk_set", None)
        print(instance, action,pk_set)
        false_pk_set=set()
        if action is "pre_add":
            for msg_pk in pk_set:
                msg= Message.objects.get(pk=msg_pk)
                if msg.user not in instance.users.all():
                    print(f'El user: {msg.user} no pertenece al hilo')
                    false_pk_set.add(msg_pk)
        #ya tenemos los que no estan  asi que los quitamos del set original
        pk_set.difference_update(false_pk_set)
        # forzamos la actualizacion del campo
        instance.save()
                    
                
m2m_changed.connect(messages_changed,sender=Thread.messages.through)