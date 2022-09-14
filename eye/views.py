import io, sys, inspect, os
from django.http import FileResponse, JsonResponse, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab_qrcode import QRCodeImage
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import django.core.exceptions
from .forms import ItemForm, SearchItemForm, LoginForm, ItemTypeForm, OrganizationForm, OrgbranchForm, ItemModelForm, LocationForm, EventForm, QRForm, InfoPrinterForm, InfoUPSForm, InfoPCForm
from eye.models import Item, Event, Orgbranch, Organization, ItemType, ItemModel, Location, InfoPrinter, InfoUPS, InfoPC

def dprint(module, function, message):
    print("DEBUG["+module+":"+function+"]: "+message)

def home(request):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if not request.user.is_authenticated:
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'not authenticated')
    return redirect('/%s?sendmeto=%s' % (settings.LOGIN_URL, request.path))
  else:
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'authenticated')
    return render(request, 'eye/home.html', {'user':request.user})

def qrprint(request):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if not request.user.is_authenticated:
    return redirect('/%s?sendmeto=%s' % (settings.LOGIN_URL, request.path))
  hgap = 38 * mm
  canvaswidth, canvasheight  = A4
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'SIZE: '+canvasheight+' : '+canvaswidth)
  buffer = io.BytesIO()
  doc = Canvas(buffer, pagesize=A4)
  leftoffset = 3 * mm
  topoffset = 0.5 * mm
  ymargin = 2.5 * mm
  qrheight = 32 * mm
  vgap = 5 * mm
  qrwidth = 32 * mm
  # number of horizontal qr-codes 
  horqrnum = 3
  pdfmetrics.registerFont(TTFont('DVS', 'DejaVuSerif.ttf'))
  centered = ParagraphStyle(name='comment',fontSize=12,fontName='DVS',alignment=1)
  code = ParagraphStyle(name='code',fontSize=6,fontName='DVS',alignment=1)
  for x in range(24):
    item = Item()
    item.save()
    xpos = leftoffset + x%horqrnum * (qrwidth+hgap)
    ypos = canvasheight - topoffset -(int(x/horqrnum)+1) * (qrheight+vgap)
    doc.line(0, ypos, canvaswidth, ypos)
    f = Frame(qrwidth+xpos, ypos+ymargin, qrwidth, qrheight, leftPadding=2, bottomPadding=2, rightPadding=2, topPadding=2, id=None, showBoundary=1)
    f.addFromList([Paragraph("Содействие",centered), Paragraph("sd.sodrk.ru",centered),Paragraph("тел. 400-440",centered),Image("/home/sodadmin/sauron/sauron/sod-icon.png", 10*mm, 10*mm),Paragraph('id: '+str(item.id),centered)],doc)
    QRCodeImage("https://eye.sodrk.ru/item/"+str(item.id), border=1, size=qrwidth ).drawOn(doc, xpos, ypos+ymargin) 
  doc.showPage()
  doc.save()
  buffer.seek(0)
  return FileResponse(buffer, as_attachment=True, filename='qrs.pdf')

def qrprintn(request,number):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],os.getcwd())
  number_of_pages =  number//24 + 1
  hgap = 38 * mm
  canvaswidth, canvasheight  = A4
  buffer = io.BytesIO()
  doc = Canvas(buffer, pagesize=A4)
  #left page margin
  leftoffset = 3 * mm
  #dirty hack
  topoffset = 0.5 * mm
  ymargin = 2.5 * mm
  qrheight = 32 * mm
  vgap = 5 * mm
  qrwidth = 32 * mm
  # number of horizontal qr-codes 
  horqrnum = 3
  pdfmetrics.registerFont(TTFont('DVS', 'DejaVuSerif.ttf'))
  centered = ParagraphStyle(name='comment',fontSize=12,fontName='DVS',alignment=1)
  code = ParagraphStyle(name='code',fontSize=6,fontName='DVS',alignment=1)
  for page in range(number_of_pages):
    for x in range(24):
      item = Item()
      item.save()
      xpos = leftoffset + x%horqrnum * (qrwidth+hgap)
      ypos = canvasheight - topoffset -(int(x/horqrnum)+1) * (qrheight+vgap)
      doc.line(0, ypos, canvaswidth, ypos)
      f = Frame(qrwidth+xpos, ypos+ymargin, qrwidth, qrheight, leftPadding=2, bottomPadding=2, rightPadding=2, topPadding=2, id=None, showBoundary=1)
      f.addFromList([Paragraph("Содействие",centered), Paragraph("sd.sodrk.ru",centered),Paragraph("тел. 400-440",centered),Image("eye/files/sod-icon.png", 10*mm, 10*mm),Paragraph('id: '+str(item.id),centered)],doc)
      QRCodeImage("https://eye.sodrk.ru/item/"+str(item.id), border=1, size=qrwidth ).drawOn(doc, xpos, ypos+ymargin) 
  doc.showPage()
  doc.save()
  buffer.seek(0)
  return FileResponse(buffer, as_attachment=True, filename='qrs.pdf')

def qrprint1(request):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if not request.user.is_authenticated:
    return redirect('/%s?sendmeto=%s' % (settings.LOGIN_URL, request.path))
  item_id = request.GET.get("item_id",None)
  hgap = 38 * mm
  canvaswidth, canvasheight  = A4
  buffer = io.BytesIO()
  doc = Canvas(buffer, pagesize=A4)
  #left page margin
  leftoffset = 3 * mm
  #dirty hack
  topoffset = 0.5 * mm
  ymargin = 2.5 * mm
  qrheight = 32 * mm
  vgap = 5 * mm
  qrwidth = 32 * mm
  horqrnum = 3
  pdfmetrics.registerFont(TTFont('DVS', 'DejaVuSerif.ttf'))
  centered = ParagraphStyle(name='comment',fontSize=12,fontName='DVS',alignment=1)
  code = ParagraphStyle(name='code',fontSize=6,fontName='DVS',alignment=1)
  for x in range(1):
    xpos = leftoffset + x%horqrnum * (qrwidth+hgap)
    ypos = canvasheight - topoffset -(int(x/horqrnum)+1) * (qrheight+vgap)
    #doc.line(0, ypos, canvaswidth, ypos)
    f = Frame(qrwidth+xpos, ypos+ymargin, qrwidth, qrheight, leftPadding=2, bottomPadding=2, rightPadding=2, topPadding=2, id=None, showBoundary=1)
    f.addFromList([Paragraph("Содействие",centered), Paragraph("sd.sodrk.ru",centered),Paragraph("тел. 400-440",centered),Image("files/sod-icon.png", 10*mm, 10*mm),Paragraph('id: '+str(item_id),centered)],doc)
    QRCodeImage("https://eye.sodrk.ru/item/"+str(item_id), border=1, size=qrwidth ).drawOn(doc, xpos, ypos+ymargin) 
  doc.showPage()
  doc.save()
  buffer.seek(0)
  return FileResponse(buffer, as_attachment=True, filename='qrs.pdf')

def item(request, item_id):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if not request.user.is_authenticated:
    #RO
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'RO')
    try:
      reqitem = Item.objects.get(pk=item_id)
    except NameError:
      return JsonResponse({"status":"error","data":"exception: nameerror"}, status = 200)
    except Item.DoesNotExist:
      if request.method == 'GET':
        return JsonResponse({"status":"error","data":"exception: does not exist"}, status = 200)
    initials = {}
    try: 
      initials['orgbranch'] = reqitem.location.orgbranch.id
    except Exception as e: pass
    try: 
      initials['itemtype'] = reqitem.model.type
    except Exception as e: pass
    try: 
      initials['organization'] = reqitem.location.orgbranch.organization.id
    except Exception as e: pass
    if not hasattr(reqitem, 'orgbranch'):
      ro_stats = { "organization":"-", "orgbranch": "-", "location": "-", "model": "-", "type": "-", "description":"-", "served":"-", "id": "-"}
    else: 
      ro_stats = { "organization":reqitem.location.orgbranch.organization.name, "orgbranch":reqitem.location.orgbranch.name, "location":reqitem.location.name, "model":reqitem.model.name, "type":reqitem.model.type.name, "description":reqitem.description, "served":reqitem.served, "id":reqitem.pk }
    if hasattr(reqitem.model, 'type'):
      if reqitem.model.type.name == 'Принтер' or reqitem.model.type.name == 'МФУ' :
        if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'printer')
        try:
          iteminfo = InfoPrinter.objects.get(itemid=item_id)
        except InfoPrinter.DoesNotExist:
          iteminfo = InfoPrinter(itemid_id=item_id, qprints=0)
          iteminfo.save()
        except Exception as e: 
          additional_form = InfoPrinterForm(instance=iteminfo)
          additional_form.action = "commit_printerinfo"
      if reqitem.model.type.name == 'ИБП':
        try:
              iteminfo = InfoUPS.objects.get(itemid=item_id)
        except InfoUPS.DoesNotExist:
          iteminfo = InfoUPS(itemid_id=item_id)
          iteminfo.save()
          additional_form = InfoUPSForm(instance=iteminfo)
          additional_form.action = "commit_upsinfo"
      if reqitem.model.type.name == 'Системный блок':
        try:
          iteminfo = InfoPC.objects.get(itemid=item_id)
        except InfoPC.DoesNotExist:
          iteminfo = InfoPC(itemid_id=item_id)
          iteminfo.save()
          additional_form = InfoPCForm(instance=iteminfo)
          additional_form.action = "commit_pcinfo"

    if 'additional_form' in locals() or 'additional_form' in globals():
      return render(request, 'eye/view_ro.html', {'ro_stats': ro_stats, 'user':request.user,'pkid':reqitem.id, 'additional_form':additional_form})
    else:
      return render(request, 'eye/view_ro.html', {'ro_stats': ro_stats, 'user':request.user,'pkid':reqitem.id, })
  #RW 
  else:  
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'RW')
    try:
        reqitem = Item.objects.get(pk=item_id)
    except NameError:
        return JsonResponse({"status":"error","data":"exception: nameerror"}, status = 200)
    except Item.DoesNotExist:
        if request.method == 'GET':
            form = ItemForm()
            form.order_fields( ['organization','orgbranch','location','itemtype','model','description'])
            return render(request, 'eye/create.html', {'form': form, 'user':request.user, 'pkid': item_id})
    if hasattr(reqitem.model, 'type'):
      if reqitem.model.type.name == 'Принтер' or reqitem.model.type.name == 'МФУ' :
        try:
            iteminfo = InfoPrinter.objects.get(itemid=item_id)
        except InfoPrinter.DoesNotExist:
            iteminfo = InfoPrinter(itemid_id=item_id, qprints=0)
            iteminfo.save()
        except Exception as e: 
          if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'err get additional info '+type(e).__name__)
        additional_form = InfoPrinterForm(instance=iteminfo)
        additional_form.action = "commit_printerinfo"
      if reqitem.model.type.name == 'ИБП':
        try:
            iteminfo = InfoUPS.objects.get(itemid=item_id)
        except InfoUPS.DoesNotExist:
            iteminfo = InfoUPS(itemid_id=item_id)
            iteminfo.save()

        additional_form = InfoUPSForm(instance=iteminfo)
        additional_form.action = "commit_upsinfo"
      if reqitem.model.type.name == 'Системный блок':
        try:
            iteminfo = InfoPC.objects.get(itemid=item_id)
        except InfoPC.DoesNotExist:
            iteminfo = InfoPC(itemid_id=item_id)
            iteminfo.save()

        additional_form = InfoPCForm(instance=iteminfo)
        additional_form.action = "commit_pcinfo"

    #EVENTS 
    try:
        events = Event.objects.all().filter(item=item_id)
    except NameError:
        return JsonResponse({"status":"error","data":"exception: nameerror"}, status = 200)
    except Item.DoesNotExist:
        return JsonResponse({"status":"error","data":"exception: not exist"}, status = 200)
    #>Item Exist
    initials = {}
    try: initials['orgbranch'] = reqitem.location.orgbranch.id
    except Exception as e: pass
    try: initials['itemtype'] = reqitem.model.type
    except Exception as e: pass
    try: initials['organization'] = reqitem.location.orgbranch.organization.id
    except Exception as e: pass

    form = ItemForm(instance=reqitem, initial=initials)
    form.order_fields( ['organization','orgbranch','location','itemtype','model','description'])
    if 'additional_form' in locals() or 'additional_form' in globals():
        return render(request, 'eye/view_rw.html', {'form': form, 'user':request.user,'pkid':reqitem.id, 'events':events, 'additional_form':additional_form})
    else:
        return render(request, 'eye/view_rw.html', {'form': form, 'user':request.user,'pkid':reqitem.id, 'events':events})


def explore(request):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if not request.user.is_authenticated:
    return redirect('/'+settings.LOGIN_URL)
  if request.method == 'GET':
    form = SearchItemForm()
    form.order_fields( ['item_id', 'organization','orgbranch','location','itemtype','model'])
    return render(request, 'eye/explore.html', {'form': form, 'user':request.user})

  if request.method == 'POST':
    formdata = request.POST.copy()
    search_result = Item.objects.all()
    if ('location' in request.POST and request.POST['location'] != ''): 
        search_result = search_result.filter(location=request.POST['location'])
    else:
      if ('orgbranch' in request.POST and request.POST['orgbranch'] != ''):
        search_result = search_result.filter(location__orgbranch__pk=int(request.POST['orgbranch']))
      else: 
        if ('organization' in request.POST and request.POST['organization'] != ''):
          search_result = search_result.filter(location__orgbranch__organization__pk= int(request.POST['organization']) )
        if ('showempty' in request.POST and request.POST['showempty'] == 'on'): 
          True;
        else:
          search_result = search_result.filter(location__isnull=False)
        if ('item_id' in request.POST and request.POST['item_id'] != ''): 
            search_result = search_result.filter(pk=request.POST['item_id'])


        if ('served' in request.POST and request.POST['served'] == 'on'): 
            search_result = search_result.filter(served=True)
        else:
            search_result = search_result.filter(served=False)

        #FILTER BY MODELS-TYPES
        if ('model' in request.POST and request.POST['model'] != ''): 
            search_result = search_result.filter(model=request.POST['model'])
        else:
            if ('itemtype' in request.POST and request.POST['itemtype'] != ''):
                search_result = search_result.filter(model__type=request.POST['itemtype'])
        records = [] 
        for record in search_result:


            records.append({ 'id': 'EMPTY', 'description': 'EMPTY', 'model': 'EMPTY', 'itemtype':'EMPTY', 'location':'EMPTY', 'organization':'EMPTY', 'orgbranch':'EMPTY', 'served':'EMPTY'})
            try: records[len(records)-1]['id'] = record.pk 
            except Exception as e: pass
            try: records[len(records)-1]['description'] = record.description 
            except Exception as e: pass
            try: records[len(records)-1]['model'] = record.model.name 
            except Exception as e: pass
            try: records[len(records)-1]['itemtype'] = record.model.type.name 
            except Exception as e: pass
            try: records[len(records)-1]['location'] = record.location.name
            except Exception as e: pass
            try: records[len(records)-1]['organization'] = record.location.orgbranch.organization.name
            except Exception as e: pass
            try: records[len(records)-1]['orgbranch'] = record.location.orgbranch.name
            except Exception as e: pass
            try: records[len(records)-1]['served'] = record.served
            except Exception as e: pass

        form = SearchItemForm(formdata)
        form.order_fields( ['organization','orgbranch','location','itemtype','model'])
        return render(request, 'eye/explore.html', {'form': form, 'user':request.user, 'records':records})


def create(request, pkid=None):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        return redirect('/%s?sendmeto=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'GET':
        #form = ItemExForm()
        form = ItemForm()
        form.order_fields( ['organization','orgbranch','location','itemtype','model','description'])
        return render(request, 'eye/create.html', {'form': form, 'uperuser':request.user})

def ajax_get_orgbranches(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('/'+settings.LOGIN_URL)
    if request.is_ajax and request.method == 'GET':
        orgname_pk = request.GET.get("orgname_pk",None)
        orgbranches = list(Orgbranch.objects.filter(organization = orgname_pk).values('pk','name'))
        return JsonResponse({"status":"success","data":{"orgbranches":orgbranches}}, status = 200)

def ajax_get_events(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('/'+settings.LOGIN_URL)
    if request.is_ajax and request.method == 'GET':
        result = []
        item_id = request.GET.get("item_id",None)
        events = Event.objects.all().filter(item=item_id)
        for event in events:
            result.append({"eventtype": str(event.eventtype), "date": str(event.date), "description": str(event.description), "eventid":event.pk})
        return JsonResponse({"status":"success","data":{"events":result}}, status = 200)

def ajax_delete_event(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('/'+settings.LOGIN_URL)
    if request.is_ajax and request.method == 'GET':





        return JsonResponse({"status":"success"}, status = 200)

def ajax_get_models(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('/'+settings.LOGIN_URL)
    if request.is_ajax and request.method == 'GET':
        itemtype_pk = request.GET.get("itemtype_pk",None)
        models = list(ItemModel.objects.filter(type = itemtype_pk).values('pk','name'))
        return JsonResponse({"status":"success","data":{"models":models}}, status = 200)

def ajax_get_locations(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('/'+settings.LOGIN_URL)
    if request.is_ajax and request.method == 'GET':
        orgbranch_pk = request.GET.get("orgbranch_pk",None)

        locations = list(Location.objects.filter(orgbranch = orgbranch_pk).values('pk','name'))



        return JsonResponse({"status":"success","data":{"locations":locations}}, status = 200)

def ajax_get_orgs(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('/'+settings.LOGIN_URL)
    if request.is_ajax and request.method == 'GET':
            organizations = list(Organization.objects.all().values('pk', 'name'))
            return JsonResponse({"status":"success","data":{"organizations":organizations}}, status = 200)

def ajax_get_itemtypes(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('/'+settings.LOGIN_URL)
    if request.is_ajax and request.method == 'GET':
            itemtypes = list(ItemType.objects.all().values('pk', 'name'))
            return JsonResponse({"status":"success","data":{"itemtypes":itemtypes}}, status = 200)


def logout(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('/'+settings.LOGIN_URL)
    django_logout(request)
    return redirect('/')

def login(request):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if request.method == 'GET':
    form = LoginForm()
    try: 
      sendmeto = request.GET['sendmeto']
    except Exception as e: 
        sendmeto = None
    return render(request, 'eye/login.html', {'form': form, 'error_msg':'dfdfdfd', 'user':request.user, 'sendmeto':sendmeto})
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      user = authenticate(username=cd['username'], password=cd['password'])
      if user is not None:
        if user.is_active:
          django_login(request, user)
          if 'sendmeto' in request.POST:
            return redirect(request.POST['sendmeto'])
          else:
            return redirect('/')
        else:
          return HttpResponse('Disabled account')
      else:
        return redirect('/')
  return render(request, 'eye/login.html', {'form': form, 'user':request.user})

def modal_addevent(request, item_id):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'GET':
      if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'get')
      initials = {}
      initials['item'] = item_id
      form = EventForm(initial=initials)
      return render(request, 'eye/add_event_modal.html', {'itemid': item_id,'form': form})
    if request.method == 'POST':
      if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'post')
      form = EventForm(request.POST)
      if form.is_valid():
          try:
             form.save()
          except BaseException as e:
              return JsonResponse({"status":"error", "data":{"py":["base py exception"]}})
              raise
          return JsonResponse({"status":"success", "data":""})
      else:
          return JsonResponse({"status":"error", "data":form.errors})

def modal_addtype(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'GET':
      form = ItemTypeForm()
      return render(request, 'eye/add_type_modal.html', {'form': form})
    if request.method == 'POST':
        form = ItemTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status":"success", "data":""})
        else:
            return JsonResponse({"status":"error", "data":form.errors})

def modal_addqrcodes(request):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if request.method == 'GET':
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'get')
    form = QRForm()
    return render(request, 'eye/add_qrcode_modal.html', {'form': form})
  if request.method == 'POST':
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'post')
    form = QRForm(request.POST)
    if form.is_valid():
      if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'form is valid')
      url = reverse('eye:url_qrprintn', args=[request.POST['number']])
      return JsonResponse({"status":"success", "data":{'redirect':url}})
    else:
      return JsonResponse({"status":"error", "data":form.errors})

def modal_addorganization(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'GET':
      form = OrganizationForm()
      return render(request, 'eye/add_organization_modal.html', {'form': form})
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status":"success", "data":""})
        else:
            return JsonResponse({"status":"error", "data":form.errors})

def modal_addorgbranch(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'GET':
      form = OrgbranchForm()
      return render(request, 'eye/add_orgbranch_modal.html', {'form': form})
    if request.method == 'POST':
        form = OrgbranchForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status":"success", "data":""})
        else:
            return JsonResponse({"status":"error", "data":form.errors})

def modal_addmodel(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'GET':
      form = ItemModelForm()
      return render(request, 'eye/add_model_modal.html', {'form': form})
    if request.method == 'POST':
        form = ItemModelForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status":"success", "data":""})
        else:
            return JsonResponse({"status":"error", "data":form.errors})

def modal_addlocation(request):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'GET':
      form = LocationForm()
      return render(request, 'eye/add_location_modal.html', {'form': form})
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status":"success", "data":""})
        else:
            return JsonResponse({"status":"error", "data":form.errors})

def commit_printerinfo(request, pkid=None):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'POST':
         if (pkid): 
             try:
                 printerinfo = InfoPrinter.objects.get(itemid=pkid)
             except Exception as e: pass
             form = InfoPrinterForm(request.POST, instance=printerinfo)
         if form.is_valid():
            form.save()
            return render(request, 'eye/created.html', {'info_url': reverse('eye:url_itemn', args=[pkid]), 'info_number': pkid, 'user': request.user})
         else:
            return JsonResponse(form.errors, status = 200) 

def commit_upsinfo(request, pkid=None):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'POST':
         if (pkid): 
             try:
                 upsinfo = InfoUPS.objects.get(itemid=pkid)
             except Exception as e: pass
             form = InfoUPSForm(request.POST, instance=upsinfo)
         if form.is_valid():
            form.save()
            return render(request, 'eye/created.html', {'info_url': reverse('eye:url_itemn', args=[pkid]), 'info_number': pkid, 'user': request.user})
         else:
            return JsonResponse(form.errors, status = 200) 

def commit_pcinfo(request, pkid=None):
    if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
    if request.method == 'POST':
         if (pkid): 
             try:
                 pcinfo = InfoPC.objects.get(itemid=pkid)
             except Exception as e: pass
             form = InfoPCForm(request.POST, instance=pcinfo)
         if form.is_valid():
            form.save()
            return render(request, 'eye/created.html', {'info_url': reverse('eye:url_itemn', args=[pkid]), 'info_number': pkid, 'user': request.user})
         else:
            return JsonResponse(form.errors, status = 200) 

def commit(request, pkid=None):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
  if request.method == 'POST':
    if (pkid): 
    #called with id parameter
      if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'with pkid')
      try:
        item = Item.objects.get(pk=pkid)
      except Item.DoesNotExist:
        item = Item()
        item.id = pkid
      form = ItemForm(request.POST, instance=item)
    else:      
      if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'w/o pkid')
      form = ItemForm(request.POST)
    if form.is_valid():
      newitem = form.save()
      return render(request, 'eye/created.html', {'info_url': reverse('eye:url_itemn', args=[newitem.pk]), 'info_number': newitem.pk, 'user': request.user})
    else:
      return JsonResponse(form.errors, status = 200) 

def event_dismiss(request, eventid):
  if settings.DEBUG: dprint(__name__, inspect.stack()[0][3],'start')
