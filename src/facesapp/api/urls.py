from django.urls import path
from ..api.views import *
from ..comparison_manager.do_comparisons import do_comparisons
from ..comparison_manager.push_results import push_results

urlpatterns = [
    path('images/', images),
    path('new_image/', new_image),

    # remove these url once the APSchedular is up and running
    path('test-comparisons/', do_comparisons),
    path('push-results/', push_results)
]