from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
	return render(request, 'home.html')

def view_list(request):
	return render(request, 'list.html', {'items': Item.objects.all()})

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/5/')