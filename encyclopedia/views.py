import markdown2
import secrets
from markdown2 import Markdown
from django import forms
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util

class NewEntryForm(forms.Form):
  title = forms.CharField(label="Entry title", widget = forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
  content = forms.CharField(label="Enter content ex. #Java Java is a language", widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows' : 10})) 
  edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(),required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()

    })

#  call the get_entry function and show on entry page
def entry(request, title):
    #pass in the title in url and get title.md title
    page = util.get_entry(title) 
    if page is None:
        return render(request, "encyclopedia/notfound.html", {

            "message": f"The page '{title}' does not exist"
        })
    else:
        #convert markdown file to html file
        html = markdown2.markdown(page)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })
   

# create search function by getting the typed query <input name ='q'> in search bar by method = 'get'
def search(request):
    #passed in the typed query in search bar store in variable
    query = request.GET.get("q","") 
    #pass in the query in search bar and get query.md title
    search_result = util.get_entry(query) 

    # if the search query match with the entries list then redirect to that entry page
    if search_result is not None:
        return HttpResponseRedirect(reverse("entry", args=[query]))

        #if search query is a substring in entries list then lead to search page
    else:
        # passed in the typed query in search bar store in variable 'query'
        query = request.GET.get('q')
        # pass in the query in search bar and get query title
        search_result = util.get_entry(query)
        #make a set to store the subStringEntries 
        subStringEntries = []
        #create 'entry' variable to represent all files that can be found in entries list
        for entry in util.list_entries():
            #for case sensitive issue we put .upper() find if substring match any entries list
            if query.upper() in entry.upper():
            #add the entries that match the query substring into the subStringEntries set
                subStringEntries.append(entry)

        return render(request, "encyclopedia/search.html", {
            "entries": subStringEntries,
           "search": True,
           "value":query
        })   
   

def newpage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)  # contain data into new entry form#
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", args=[title]))
            else:
                return render(request, "encyclopedia/newpage.html", {
                "form": form,
                "message": f"The page '{title}' already exist",
                "existing": True,
                "entry": title
            })
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form,
                "existing": False
                })
    else:
        return render(request, "encyclopedia/newpage.html", {
        "form": NewEntryForm(),
        "existing" : False
    })


def edit(request,title):
    entryPage = util.get_entry(title)
    if entryPage is None:
        return render(request, "encyclopedia/notfound.html",{
            "entryTitle" : title,
            "message": f"The page '{title}' does not exist"
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = title
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newpage.html", {
            "form": form, 
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial,
            "content": form.fields["content"].initial
        })

def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[randomEntry]))

