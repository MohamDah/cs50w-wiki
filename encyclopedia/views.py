from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, TITLE):
    if util.get_entry(TITLE) != None:
        entry = markdown2.markdown(util.get_entry(TITLE))
    elif util.get_entry(TITLE.capitalize()) != None:
        entry = markdown2.markdown(util.get_entry(TITLE.capitalize()))
    else:
        return render(request, "encyclopedia/apology.html", { "apology": "entry does not exist"})

    return render(request, "encyclopedia/title.html", {
        "entry": entry,
        "title": TITLE
    })

def search(request):
    query = request.GET.get("q")
    if util.get_entry(query) != None or util.get_entry(query.capitalize()) != None:
        return redirect(f"wiki/{query}")
    else:
        results = []
        for entry in util.list_entries():
            if query in entry:
                results.append(entry)
    return render(request, "encyclopedia/results.html", {
        "results": results
    })

def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if not title or not content:
            return render(request, "encyclopedia/apology.html", { "apology": "Don't leave any field empty"})
        if title in util.list_entries():
            return render(request, "encyclopedia/apology.html", { "apology": "Title already exists"})
        util.save_entry(title, content)
        return redirect(f"wiki/{title}")

    else:
        return render(request, "encyclopedia/new.html")

def edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if not content:
            return render(request, "encyclopedia/apology.html", { "apology": "Don't leave any field empty"})
        util.save_entry(title, content)
        return redirect(f"wiki/{title}")
    else:
        title = request.GET.get("title")
        text = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "text": text,
            "title": title
        })

def random(request):
    titles = util.list_entries()
    title = choice(titles)
    return redirect(f"wiki/{title}")