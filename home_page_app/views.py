from django.shortcuts import render

# Create your views here.

def home_view(request):
    return render(request, "home_page_app/index.html")


def about_view(request):
    return render(request, "home_page_app/about.html")


def contact_view(request):
    return render(request, "home_page_app/contact.html")


def membership_view(request):
    return render(request, "home_page_app/membership_plans.html")


def faqs_view(request):
    return render(request, "home_page_app/FAQs.html")


def event_list_view(request):
    return render(request, "home_page_app/event_list.html")

def event_detail_view(request, id):
    return render(request, "home_page_app/event_detail.html", {'id': id})

