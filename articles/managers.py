# Path: articles/managers.py

from django.db import models
from django.db.models import Count, Q

class ArticleManager(models.Manager):
    def with_reactions(self, user=None):
        queryset = self.annotate(
            likes=Count('reactions', filter=Q(reactions__reaction='like')),
            dislikes=Count('reactions', filter=Q(reactions__reaction='dislike')),
            score=Count('reactions', filter=Q(reactions__reaction='like')) - 
                  Count('reactions', filter=Q(reactions__reaction='dislike'))
        )
        
        if user and user.is_authenticated:
            from .models import Reaction 
            user_reaction = Reaction.objects.filter(
                user=user, article_id=models.OuterRef('pk')
            ).values('reaction')[:1]
            queryset = queryset.annotate(annotated_reaction=models.Subquery(user_reaction))
            
        return queryset