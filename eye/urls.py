from django.urls import path
from django.contrib import admin

from . import views

app_name = 'eye'
urlpatterns = [
  path('', views.home, name='url_index'),
  path('home', views.home, name='url_home'),
  path('qrprint1/', views.qrprint1, name='url_qrprint1'),
  path('qrprintn/<int:number>/', views.qrprintn, name='url_qrprintn'),
  path('explore/', views.explore, name='url_explore'),
  path('create/', views.create, name='url_create'),
  path('create/<int:item_id>/', views.create, name='url_createn'),
  path('item/<int:item_id>/', views.item, name='url_itemn'),
  path('login/', views.login, name='url_login'),
  path('logout/', views.logout, name='url_logout'),
  path('ajax/get-orgbranches/', views.ajax_get_orgbranches, name='url_ajax_get_orgbranches'),
  path('ajax/get-models/', views.ajax_get_models, name='url_ajax_get_models'),
  path('ajax/get-locations/', views.ajax_get_locations, name='url_ajax_get_locations'),
  path('ajax/get-orgs/', views.ajax_get_orgs, name='url_ajax_get_orgs'),
  path('ajax/get-itemtypes/', views.ajax_get_itemtypes, name='url_ajax_get_itemtypes'),
  path('ajax/get-events/', views.ajax_get_events, name='url_ajax_get_events'),
  path('ajax/delete_event/<int:eventid>', views.ajax_delete_event, name='url_ajax_delete_event'),
  path('commit/<int:pkid>/', views.commit, name='url_commitn'),
  path('commit_printerinfo/<int:pkid>/', views.commit_printerinfo, name='url_commit_printerinfon'),
  path('commit_upsinfo/<int:pkid>/', views.commit_upsinfo, name='url_commit_upsinfon'),
  path('commit_pcinfo/<int:pkid>/', views.commit_pcinfo, name='url_commit_pcinfon'),
  path('commit/', views.commit, name='url_commit'),
  path('modal/add_itemtype/',views.modal_addtype, name='url_modal_add_itemtype'),
  path('modal/add_organization/',views.modal_addorganization, name='url_modal_add_organization'),
  path('modal/add_orgbranch/',views.modal_addorgbranch, name='url_modal_add_orgbranch'),
  path('modal/add_model/',views.modal_addmodel, name='url_modal_add_model'),
  path('modal/add_location/',views.modal_addlocation, name='url_modal_add_location'),
  path('modal/add_qrcodes/',views.modal_addqrcodes, name='url_modal_add_qrcodes'),
  path('modal/add_event/<int:item_id>/',views.modal_addevent, name='url_modal_add_eventn'),
  path('event_dismiss/<int:eventid>/',views.event_dismiss, name='url_event_dismissn'),
]
