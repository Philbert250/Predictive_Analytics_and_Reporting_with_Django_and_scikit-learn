from io import BytesIO
import csv
import io
import numpy as np
import pandas as pd
import pandas_datareader as web
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.template.loader import get_template
from django.db.models import Sum

from .models import*
from django.db.models import Max
from django.db.models import Min
from xhtml2pdf import pisa

import os
from django.conf import settings
from django.templatetags.static import static
import matplotlib
matplotlib.use('Agg')  # Set the backend to a non-GUI backend

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from sklearn.linear_model import LinearRegression
from django.db.models import Sum
from .models import Uploadcsv

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime

# Create your views here.

# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('signing')
    else:
        return render(request, 'signin.html')

def logout_user(request):
    auth.logout(request)
    return redirect('signing')


def welcome(request):

    ########################### operation of scatter graph ##########################
    data = Uploadcsv.objects.all()

    # Create a DataFrame from the model data
    df = pd.DataFrame(list(data.values()))

    # Convert the numeric columns to integers
    df['year'] = pd.to_numeric(df['year'])
    df['death_cases'] = pd.to_numeric(df['death_cases'])

    # Perform linear regression
    X = df['year'].values.reshape(-1, 1)
    y = df['death_cases'].values.reshape(-1, 1)
    reg = LinearRegression().fit(X, y)

    # Generate scatter plot
    fig, ax = plt.subplots()
    ax.scatter(X, y)
    ax.plot(X, reg.predict(X), color='red')
    ax.set_xlabel('Year')
    ax.set_ylabel('Death Cases')
    ax.set_title('Scatter Plot: Years vs Death Cases')

    # Render the plot to a FigureCanvas
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)

    # Set the buffer's file position to the beginning
    buffer.seek(0)

    # Save the plot to a temporary file
    plot_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'plot.png')
    with open(plot_path, 'wb') as f:
        f.write(buffer.read())

    plot_url = static('img/plot.png')
    

    selectcase = Uploadcsv.objects.all()
    casesum = Uploadcsv.objects.aggregate(Sum('cases'))
    deathsum = Uploadcsv.objects.aggregate(Sum('death_cases'))
    contextdata = {
        'cases': selectcase,
        'sumcase': casesum,
        'sumdeath': deathsum,
        'plot_path': plot_url
    }
    return render(request, 'index.html', context=contextdata)

def predictpage(request):
    data = Uploadcsv.objects.all()

    # Create a DataFrame from the model data
    df = pd.DataFrame(list(data.values()))

    # Convert the numeric columns to integers
    df['year'] = pd.to_numeric(df['year'])
    df['death_cases'] = pd.to_numeric(df['death_cases'])

    # Perform linear regression
    X = df['year'].values.reshape(-1, 1)
    y = df['death_cases'].values.reshape(-1, 1)
    reg = LinearRegression().fit(X, y)

    # Generate scatter plot
    fig, ax = plt.subplots()
    ax.scatter(X, y)
    ax.plot(X, reg.predict(X), color='red')
    ax.set_xlabel('Year')
    ax.set_ylabel('Death Cases')
    ax.set_title('Scatter Plot: Years vs Death Cases')

    # Render the plot to a FigureCanvas
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)

    # Set the buffer's file position to the beginning
    buffer.seek(0)

    # Save the plot to a temporary file
    plot_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'plot.png')
    with open(plot_path, 'wb') as f:
        f.write(buffer.read())

    plot_url = static('img/plot.png')

    selectcase = Uploadcsv.objects.all()
    casesum = Uploadcsv.objects.aggregate(Sum('cases'))
    deathsum = Uploadcsv.objects.aggregate(Sum('death_cases'))
    if request.method =='POST':
        province = request.POST['province']
        year = request.POST['year']
        datalist = Uploadcsv.objects.all().filter(province_name=province)
        maxCasedata = Uploadcsv.objects.all().filter(province_name=province).order_by('cases').first()
        minCasedata = Uploadcsv.objects.all().filter(province_name=province).order_by('cases').last()
        mindata = int('0' + minCasedata.cases)
        maxdata = int('0' + maxCasedata.cases)
        casedeff= mindata - maxdata
        if minCasedata.year == 2021:
            predictyear = ((mindata + casedeff) * 100) / mindata
        else:
            predictyear = ((mindata - casedeff) * 100) / mindata
        maxDeathCasedata = Uploadcsv.objects.all().filter(province_name=province).order_by('death_cases').first()
        minDeathCasedata = Uploadcsv.objects.all().filter(province_name=province).order_by('death_cases').last()
        mindeathdata = int('0' + minDeathCasedata.death_cases)
        maxdeathdata = int('0' + maxDeathCasedata.death_cases)
        casedeathdeff= mindeathdata - maxdeathdata
        if minDeathCasedata.year == 2021:
            predictyeardeath = ((mindeathdata + casedeathdeff) * 100) / mindata
        else:
            predictyeardeath = ((mindeathdata - casedeathdeff) * 100) / mindata
    contextdata = {
        'cases': selectcase,
        'sumcase': casesum,
        'sumdeath': deathsum,
        'resultCase': predictyear,
        'resultDeath': predictyeardeath,
        'plot_path': plot_url
    }
    return render(request,'index.html', context=contextdata)

def generaldata(request):
    qs = Uploadcsv.objects.all().values()
    generaldata = qs.to_timeseries(index='province_name',
                          pivot_columns='year',
                          values='cases',
                          storage='long')
    deathdata = qs.to_timeseries(index='province_name',
                          pivot_columns='year',
                          values='death_cases',
                          storage='long')
    contextdata = {
        'general' : generaldata.to_html(classes='table table-bordered', table_id="dataTable"),
        'deatdata' : deathdata.to_html(classes='table table-bordered', table_id="dataTable")
    }
    return render(request,'general.html', context=contextdata)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def reportpdf(request):
    template = get_template('reportpdf.html')
    Northernselectcase =  Uploadcsv.objects.all().filter(province_name='Northern')
    Southernselectcase =  Uploadcsv.objects.all().filter(province_name='Southern')
    Westernselectcase =  Uploadcsv.objects.all().filter(province_name='Western')
    Easternselectcase =  Uploadcsv.objects.all().filter(province_name='Eastern')
    Kigaliselectcase =  Uploadcsv.objects.all().filter(province_name='Kigali')
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    contextdata = {
        'Northernselect': Northernselectcase,
        'Southernselect': Southernselectcase,
        'Westernselect': Westernselectcase,
        'Easternselect': Easternselectcase,
        'Kigaliselect': Kigaliselectcase,
        'timesp': ts
    }
    html = template.render(contextdata)
    pdf = render_to_pdf('reportpdf.html',contextdata)
    return HttpResponse(pdf, content_type='application/pdf')

def uploadcv(request):
    if request.method == 'POST' and request.FILES['csv']:
        csv_file = request.FILES['csv']
        fetchData=Uploadcsv.objects.all()
        if not csv_file.name.endswith('.csv'):
            return render(request, 'uplaodcsv.html', {'messagefailed': 'This is not a csv File, upload a csv file!!'})
        data_set=csv_file.read().decode('UTF-8')
        io_string=io.StringIO(data_set)

        for col in csv.DictReader(io_string):
            Uploadcsv.objects.update_or_create(year=col['year'],province_name=col['province_name'],cases=col['cases'],death_cases=col['death_cases'])

        return render(request, 'uplaodcsv.html', {'message': 'Data has been inserted successful'})
    return render(request,'uplaodcsv.html')

def pdf_img(request):                                  

    # Create the HttpResponse object with the appropriate PDF headers. 
    response = HttpResponse(content_type='application/pdf') 

    # Create the PDF object, using the response object as its "file." 
    p = canvas.Canvas(response)     
    p.drawString(100, 100, "Hello  (Dynamic PDF) - ") 
    my_image = ImageReader('https://www.google.com/images/srpr/logo11w.png')

    p.drawImage(my_image, 10, 500, mask='auto')

    # Close the PDF object. 
    p.showPage() 
    p.save() 

    # Show the result to the user    
    return response