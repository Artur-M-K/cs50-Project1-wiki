import markdown2
import random
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from markdown2 import Markdown

from . import util

markdowner = Markdown()

class NewForm(forms.Form):
    page = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class newEntryForm(forms.Form):
    title = forms.CharField(label="title")
    description = forms.CharField(widget=forms.Textarea(),label="")

class editEntryForm(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(),label="")

def index(request):
    entries = util.list_entries()
    search_results = []

    if request.method == "POST":
        form = NewForm(request.POST)
        
        if form.is_valid():
                page = form.cleaned_data['page']
                             
                for entry in entries: 
                    if entry.lower() == page.lower():
                        pageResult = util.get_entry(page)
                        pageResult_markdown = markdown2.markdown(pageResult)
                        return render(request, "encyclopedia/wiki.html", {
                        "wiki": pageResult_markdown,
                        "name": page,
                        "form": NewForm()
                        })
                    
                        
                    if page.lower() in entry.lower():
                        search_results.append(entry)
                        return render(request, "encyclopedia/search.html", {
                        "results": search_results,
                        "name": page,
                        "form": NewForm()
                        })
                else:
                        error = 'Page is not Exsist'
                        return render(request, "encyclopedia/error.html", {
                            "name": page,
                            'error': error,
                            "form": NewForm()
                        })
        
    else: 
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewForm()
        })

def wiki(request, name):
    entry = util.get_entry(name)
    entry_markdown = markdown2.markdown(entry)
    error = 'Page is not Exsist'
    if entry is None:

        return render(request, "encyclopedia/error.html", {
            "name": name,
            'error': error,
            "form": NewForm()
        })
    else:
        return render(request, "encyclopedia/wiki.html", {
            "wiki": entry_markdown,
            "name": name,
            "form": NewForm()
        })

def newEntry(request):
    entries = util.list_entries()
    if request.method == 'POST':
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            if title in entries:
                    error = "This title is already exist in encyclopedia, please choose a different name"

                    return render(request, "encyclopedia/error.html", {
                        "name": title,
                        'error': error,
                        "form": NewForm()
                    })
            else:
                    titleForSave = '#' + title
                    descriptionForSave = '\n' + description
                    contentForSave = titleForSave + descriptionForSave
                    util.save_entry(title,contentForSave)
                    name = util.get_entry(title)
                    markdown = markdowner.convert(name)

                    return render(request, "encyclopedia/wiki.html", {
                        "wiki": markdown,
                        "name": title,
                        "form": NewForm()
                    })    
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "newEntryForm": newEntryForm(),
            "form": NewForm()
        })

def randomEntry(request):
    entries = util.list_entries()
    random_entry_result = random.choice(entries)
    entry = util.get_entry(random_entry_result)
    entry_markdown = markdown2.markdown(entry)

    return render(request, "encyclopedia/randomEntry.html", {
        "form": NewForm(),
        'entry': entry_markdown,
        'name': random_entry_result,
        "form": NewForm()
    })

def editEntry(request, name):
    if request.method == 'GET':
        entry = util.get_entry(name)

        return render(request, "encyclopedia/editEntry.html", {
        'name': name,
        'editForm': editEntryForm(initial={'textarea': entry}),
        "form": NewForm()
        })
    else:
        form = editEntryForm(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data['textarea']
            util.save_entry(name,textarea)
            entry = util.get_entry(name)
            entry_markdown = markdown2.markdown(entry)

            return render(request, "encyclopedia/wiki.html", {
            "wiki": entry_markdown,
            "name": name,
            "form": NewForm()
            })