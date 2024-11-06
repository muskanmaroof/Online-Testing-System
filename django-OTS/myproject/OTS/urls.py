from django.urls import path
from OTS.views import *
app_name='OTS'

urlpatterns = [
    path('', welcome, name='welcome-page'),
    path('registration/', candidateRegistrationForm, name='register-form'),
    path('store-candidate/', candidateRegistration, name='storeCandidate'),
    path('login/', loginView , name="login"),
    path('home/', candidateHome , name="home"),
    path('test-paper/', testPaper , name="testpaper"),
    path('calculate-result/', calculateTestResult , name="calculateTest"),
    path('test-history/', testResultHistory , name="testHistory"),
    path('result/', showTestResult , name="result"),
    path('logout/', logoutView , name="logout"),
]