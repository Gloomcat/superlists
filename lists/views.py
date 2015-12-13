from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
	if request.method == 'POST':
		item = Item.objects.create(text=request.POST['item_text'])
		return redirect('/lists/5/')

	return render(request, 'home.html')

def view_list(request):
	return render(request, 'list.html', {'items': Item.objects.all()})