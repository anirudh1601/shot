from django.urls import path
from . import views


urlpatterns = [
	path('',views.audio,name="audio"),
	path('screen_png',views.serve_pil_image ,name="pil"),
	path('js/<path:path>',views.send_js,name='js')
]