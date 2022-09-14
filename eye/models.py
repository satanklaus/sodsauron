from django.db import models

class Organization(models.Model):
  name = models.CharField(max_length=200)
  def __str__(self):
    return self.name

class Orgbranch(models.Model):
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  address = models.CharField(max_length=1000, blank=True)
  def __str__(self):
    return str(self.name)

class ItemType(models.Model):
  name = models.CharField(max_length=100)
  def __str__(self):
    return self.name

class Location(models.Model):
  orgbranch = models.ForeignKey(Orgbranch, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  def __str__(self):
    return str(self.name)

class ItemModel(models.Model):
  name = models.CharField(max_length=200)
  type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
  def __str__(self):
    #return str(self.type.name) + ' => ' + str(self.name)
    return str(self.name)


class Item(models.Model):
  location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
  description = models.CharField(max_length=1000, blank=True)
  model = models.ForeignKey(ItemModel, on_delete=models.CASCADE, null=True)
  served = models.BooleanField(default=False)
  Reserved = models.BooleanField(default=False)
  def __str__(self):
    if not self.location:
      _location = "_loc"
    else:
      _location = str(self.location)
    if not self.model:
      _model = "_mod"
    else:
      _model = str(self.model)
    return _location + ','  + _model

class EventType(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=1000, blank=True)
  def __str__(self):
    return self.name

class Hobbit(models.Model):
  name = models.CharField(max_length=100)
  def __str__(self):
    return self.name

class Event(models.Model):
  eventtype = models.ForeignKey(EventType, on_delete=models.CASCADE)
  date = models.DateTimeField(blank=True)
  description = models.CharField(max_length=1000, blank=True)
#  hobbit = models.ForeignKey(Hobbit, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  def __str__(self):
    return str(self.eventtype)+' в ' + str(self.item) + ' @' + str(self.date)

class InfoPrinter(models.Model):
  itemid = models.ForeignKey(Item, on_delete=models.CASCADE)
  qprints = models.PositiveIntegerField(blank=True)

class InfoUPS(models.Model):
  itemid = models.ForeignKey(Item, on_delete=models.CASCADE)
  replace_date = models.DateTimeField(blank=True, null=True)
  test_date = models.DateTimeField(blank=True, null=True)
  test_result = models.CharField(max_length=1000, blank=True)

class InfoPC(models.Model):
  itemid = models.ForeignKey(Item, on_delete=models.CASCADE)
  service_date = models.DateTimeField(blank=True, null=True)
