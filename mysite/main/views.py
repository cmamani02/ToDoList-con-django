from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
# Create your views here.

def index(response, id):
    #return HttpResponse("<h1>WebDev 101!</h1>")
    my_dict = {}
    ls = ToDoList.objects.get(id=id)
    #item = ls.item_set.get(id=1) #por ahora solo tenemos uno!
    #return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" %(ls.name, str(item.text))) #muestra el id parametro
    #return render(response, "main/base.html", {"name":ls.name})
    if response.method == "POST":
        #save and add items
        print(response.POST)
        if response.POST.get("save"):
            #reviso si los items fueron clickeados
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    #actualizo el item
                    item.complete = True
                else:
                    #si fue desclickeado o no hubo cambios
                    item.complete = False
                item.save() #guarda cambios en la base de datos
            
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")

            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid") 
    return render(response, "main/list.html", {"ls":ls})

def home(response):
    return render(response, "main/home.html", {})     

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
        
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})  