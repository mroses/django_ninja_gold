from django.shortcuts import render, redirect
import random

# Create your views here.
def index(req):
    if 'gold_count' not in req.session:
        req.session['gold_count'] = 0

    if 'activities' not in req.session:
        req.session['activities'] = []

    return render(req, 'main/index.html')

def process(req):
    if req.method != "POST" or 'location' not in req.POST:
        return redirect('/') #makes sure we hit process route through form rather than somebody just typing in /process in url

    #each time we hit the process route, it will generate a new randint from the location map below. this is how we get new gold amounts each time we click the form process route.
    location_map = {
        'cave': random.randint(5,10),
        'house': random.randint(2,5),
        'farm': random.randint(10, 20),
        'casino': random.randint(-50, 50)
    }
    print "*" * 80
    print req.POST['location'] #this is the value of the location clicked on. If click cave, this will print the string 'cave'
    print location_map['cave'] #generates random int for cave
    print location_map[req.POST['location']] 
    #since req.POST['location'] is string 'cave' in this example, we can replace location_map['cave'] with location_map[req.POST['location']]
    current_gold = location_map[req.POST['location']]
    req.session['gold_count'] += current_gold #accesses current gold count stored in session and adds random int to it

    if current_gold > 0:
        activity = {
            'content': "Earned {} Gold at the {}.".format(current_gold, req.POST['location']),
            'css_class': 'green'
        }
    else:
        activity = {
            'content': "Lost {} Gold at the {}.".format(current_gold * -1, req.POST['location']),
            'css_class': 'red'
        }
    req.session['activities'].append(activity) #adds activity to empty activity list we created at beginning
    req.session.modified = True # session doesn't know we have appended something to a list because it's just pointing to a specific location. It doesn't know whats in the location has changed. So we use req.session.modified = True to tell it. Tells Django to copy everything over and makes it to the new request.
    return redirect('/')

def reset(req):
    req.session.clear()
    return redirect('/')

def color(req, color):
    print "*" * 80
    print color
    return redirect('/')