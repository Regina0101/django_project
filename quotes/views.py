# quotes/views.py
from bson import ObjectId
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from .utils import get_mongodb
from .forms import AuthorForm, QuoteForm, TagForm

db = get_mongodb()


def main(request, page=1):
    quotes = list(db.quotes.find())
    authors = list(db.authors.find())
    tags_pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "quote_count": {"$sum": 1}}},
        {"$sort": {"quote_count": -1}},
        {"$limit": 10},
        {"$project": {"id": "$_id", "quote_count": 1, "_id": 0}}
    ]
    top = list(db.quotes.aggregate(tags_pipeline))
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    for author in authors:
        author['id'] = str(author['_id'])
    for quote in quotes:
        quote['author'] = str(quote['author'])
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'authors': authors,'top': top})

def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            db.authors.insert_one(form.cleaned_data)
            return redirect(reverse('quotes:root'))
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


def add_quote(request):
    authors = list(db.authors.find())
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            author_name = request.POST.get('author')
            author = db.authors.find_one({"fullname": author_name})
            if not author:
                form.add_error('author', 'Selected author does not exist.')
            else:
                tags_input = request.POST.get('tags')
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                quote_data = form.cleaned_data
                quote_data['author'] = author['_id']
                quote_data['tags'] = tags
                db.quotes.insert_one(quote_data)
                return redirect(reverse('quotes:root'))
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form, 'authors': authors})



def author_info(request, _id):
    author_id = ObjectId(_id)
    author = db.authors.find_one({"_id": author_id})
    return render(request, 'quotes/author_info.html', {'author': author})


def quotes_by_tag(request, tag_name, page=1):
    quotes = list(db.quotes.find({"tags": tag_name}))
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

