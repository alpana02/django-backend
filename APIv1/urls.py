from django.urls import path
from . import views
from.views import uploadUrl,getAllSentences,updateSelectedSentence,summary,uploadPdf

urlpatterns = [
    # path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', views.RegisterView.as_view(), name='auth_register'),
    # path('', views.getRoutes)
    path('uploadUrl/',uploadUrl,name = 'uploadUrl'),
    path('uploadPdf/',uploadPdf,name = 'uploadPdf'),
    path('getAllSentences/<int:websiteId>',getAllSentences,name = 'getAllSentences'),
    path('updateSelectedSentence/<int:sentenceId>',updateSelectedSentence,name = 'updateSelectedSentence'),
    path('summary/<int:websiteId>',summary,name = 'summary')
]
