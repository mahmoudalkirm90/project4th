from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, IntegerField

from users.permissions import IsDoctor, IsPatient

from .serializers import (ArticaleCraeteSerializer,
                          ArticleRetrieveSerializer,
                          ArticlesMostReactionScoreSerializer, 
                          ReactionSerializer,
                          DeleteArticleSerializer,
                          ArticleSerializer,

                          )
from .models import Article, Reaction
from .recommender import recommend_articles
from .pagination import ArticlePagination

from users.models import User

class ArticleCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    serializer_class = ArticaleCraeteSerializer

    def get_queryset(self,request):
        return Article.objects.filter(author=request.user.doctor)
    
    def create(self, serializer): 
        serializer = self.get_serializer(data = self.request.data) 
        serializer.is_valid(raise_exception=True) 
        serializer.save()

        return Response({
            "message": "Article added, please wait until review it"
        })

class ArticleRetrieveAPIView(generics.RetrieveAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleRetrieveSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Article.objects.annotate(
                likes = Count('reactions', filter=Q(reactions__reaction='like')),
                dislikes = Count('reactions', filter=Q(reactions__reaction='dislike')),
                score = Count('reactions', filter=Q(reactions__reaction='like')) - 
                        Count('reactions', filter=Q(reactions__reaction='dislike'))
                ).filter(status="Approved").order_by('-likes','-score',)
class ArticleListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleRetrieveSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def get_queryset(self):
        username = self.request.query_params.get('author_username', None)
        user = self.request.user
        
        objs = Article.objects.annotate(
            likes = Count('reactions', filter=Q(reactions__reaction='like')),
            dislikes = Count('reactions', filter=Q(reactions__reaction='dislike')),
            score = Count('reactions', filter=Q(reactions__reaction='like')) - 
                    Count('reactions', filter=Q(reactions__reaction='dislike'))
            )
        
        # اذا كان موجود البارامتر بالرابط منرجع فقط المقالات المقبولة
        if username:
            user = get_object_or_404(User, username=username)
            return objs.filter(author=user.doctor, status="Approved").order_by('-likes','-score',)
        
        # منرجع كل المقالات لصاحبها
        return objs.filter(author=user.doctor).order_by('-likes','-score',)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), IsDoctor()]
        return super().get_permissions()
            
class RecommendedArticlesAPIView(generics.ListAPIView):
    pagination_class   = ArticlePagination
    serializer_class   = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        patient     = self.request.user.patient
        recommended = recommend_articles(patient=patient)

        recommended_ids = list(recommended.keys())

        # حافظ على ترتيب الـ recommended بـ CASE WHEN
        order = Case(
            *[
                When(id=article_id, then=pos)
                for pos, article_id in enumerate(recommended_ids)
            ],
            output_field=IntegerField()
        )

        return (
            Article.objects
            .filter(id__in=recommended_ids, status='Approved')
            .annotate(
                likes    = Count('reactions', filter=Q(reactions__reaction='like')),
                dislikes = Count('reactions', filter=Q(reactions__reaction='dislike')),
                score    = (
                    Count('reactions', filter=Q(reactions__reaction='like')) -
                    Count('reactions', filter=Q(reactions__reaction='dislike'))
                ),
                relevance_order = order,
            )
            .order_by('relevance_order', '-score')  # ترتيب الـ recommendation أولاً، score كـ tiebreaker
        )

class ArticlesMostReactionScoreListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticlesMostReactionScoreSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    def get_queryset(self):
        return Article.objects.annotate(
                likes = Count('reactions', filter=Q(reactions__reaction='like')),
                dislikes = Count('reactions', filter=Q(reactions__reaction='dislike')),
                score = Count('reactions', filter=Q(reactions__reaction='like')) - 
                        Count('reactions', filter=Q(reactions__reaction='dislike'))
                ).filter(status="Approved").order_by('-likes','-score',)

class ReactionGenericAPIView(generics.GenericAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated] 
    
    def post(self, request, article_id):
        user = request.user
        reaction_type = request.data.get('reaction')
        article = get_object_or_404(Article, id = article_id)
        if not article.status == "Approved": 
            return Response({"article not "})
        exist = Reaction.objects.filter(
            user=user,
            article=article,
        ).first()
        if exist: 
            if exist.reaction == reaction_type: 
                # (toggle reaction) 
                exist.delete()
                return Response({"message": f"{reaction_type} removed"})
            
            else: 
                exist.reaction = reaction_type
                exist.save()
                return Response({"message": f"{reaction_type} added"})
        Reaction.objects.create(
            user=user,
            article=article,
            reaction=reaction_type
        )
        return Response({"message": f"{reaction_type} added"})
        
class DeleteArticleGenericAPIView(generics.GenericAPIView): 
    serializer_class = DeleteArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user.doctor
        )
    def delete(self, request, article_id): 
        author = request.user.doctor
        article = get_object_or_404(Article, id=article_id)

        if not article.author == author: 
            return Response({
                "message": "article not related to author"
            }, status=400)
        
        article.delete()
        return Response({
            "message": "Article deleted"
        })
