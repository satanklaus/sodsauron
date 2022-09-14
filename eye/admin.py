from django.contrib import admin

from .models import Event
from .models import Organization
from .models import Orgbranch
from .models import ItemType
from .models import Item
from .models import EventType
from .models import Hobbit
from .models import Location
from .models import ItemModel
from .models import InfoPrinter


# Register your models here.
admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(Orgbranch)
admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(EventType)
admin.site.register(Hobbit)
admin.site.register(Location)
admin.site.register(ItemModel)
admin.site.register(InfoPrinter)

