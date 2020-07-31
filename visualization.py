from io import BytesIO
from flask import Flask,render_template,send_file              #For render template
import numpy as np                                             #For Array Operation
import pandas as pd                                            #For data extraction
import matplotlib.pyplot as plt                                #For Data Visualization
import jinja2

app=Flask(__name__)

#PI PLOT

def pieDigram(clgData):

    fig, ax = plt.subplots(figsize=(10,5))
    Amravati=0
    Aurangabad=0
    Mumbai=0
    Nagpur=0
    Nashik=0
    Pune=0

    for i in clgData["ID"]:
        if i>1000 and i<2000:
            Amravati=Amravati+1
        elif i>2000 and i<3000:
            Aurangabad=Aurangabad+1
        elif i>3000 and i<4000:
            Mumbai=Mumbai+1
        elif i>4000 and i<5000:
            Nagpur=Nagpur+1
        elif i>5000 and i<6000:
            Nashik=Nashik+1
        elif i>6000 and i<7000:
            Pune=Pune+1

    univerity="Amravati","Aurangabad","Mumbai","Nagpur","Nashik","Pune"
    clgcount=[Amravati,Aurangabad,Mumbai,Nagpur,Nashik,Pune]
    piecolor=["gold","yellowgreen","lightcoral","lightskyblue","red","green"]
    explode=(0.1,0.1,0.1,0.1,0.1,0.1)
    plt.pie(clgcount,explode=explode,labels=univerity,colors=piecolor,autopct='%1.1f%%',shadow=True,startangle=140)
    plt.axis('equal')
    plt.title("Pie Diagram Of Percent Of College Count From University")
    plt.savefig("static/Pie Diagram of Percent of college count from university.png")
    barGraph(clgData,Amravati,Aurangabad,Mumbai,Nagpur,Nashik,Pune)       #Call barGraph function

#University Bar Graph

def barGraph(clgData,Amravati,Aurangabad,Mumbai,Nagpur,Nashik,Pune):

    fig, ax = plt.subplots(figsize=(10,5))
    barclgcount=[Amravati,Aurangabad,Mumbai,Nagpur,Nashik,Pune]
    universitybar=('Amravati','Aurangabad','Mumbai','Nagpur','Nashik','Pune')
    y_pos = np.arange(len(universitybar))

    plt.bar(y_pos, barclgcount, color=["gold","yellowgreen","lightcoral","lightskyblue","red","green"],edgecolor="black")

    plt.xlabel('Number of Colleges')
    plt.ylabel('Name of Universities')
    plt.xticks(y_pos, universitybar,rotation=20)
    plt.title("Bar Graph of University Wise College Count")
    plt.savefig("static/Bar Graph of University wise college count.png")

#Discriate Graph

def discretGraph(clgData):

    #University Distrubution
    amravatiUniversity=pd.DataFrame(data=clgData[clgData.Region=="Amravati"])
    aurangabadUniversity=pd.DataFrame(data=clgData[clgData.Region=="Aurangabad"])
    mumbaiUniversity=pd.DataFrame(data=clgData[clgData.Region=="Mumbai"])
    nagpurUniversity=pd.DataFrame(data=clgData[clgData.Region=="Nagpur"])
    nashikUniversity=pd.DataFrame(data=clgData[clgData.Region=="Nashik"])
    puneUniversity=pd.DataFrame(data=clgData[clgData.Region=="Pune"])    

    
    amrAu=len(amravatiUniversity[amravatiUniversity.Autonomus_Status=="Autonomous"])
    amrNa=len(amravatiUniversity[amravatiUniversity.Autonomus_Status=="Non-Autonomous"])
    aurAu=len(aurangabadUniversity[aurangabadUniversity.Autonomus_Status=="Autonomous"])
    aurna=len(aurangabadUniversity[aurangabadUniversity.Autonomus_Status=="Non-Autonomous"])
    mumAu=len(mumbaiUniversity[mumbaiUniversity.Autonomus_Status=="Autonomous"])
    mumNa=len(mumbaiUniversity[mumbaiUniversity.Autonomus_Status=="Non-Autonomous"])
    nasAu=len(nashikUniversity[nashikUniversity.Autonomus_Status=="Autonomous"])
    nasNa=len(nashikUniversity[nashikUniversity.Autonomus_Status=="Non-Autonomous"])
    nagAu=len(nagpurUniversity[nagpurUniversity.Autonomus_Status=="Autonomous"])
    nagNa=len(nagpurUniversity[nagpurUniversity.Autonomus_Status=="Non-Autonomous"])
    puAu =len(puneUniversity[puneUniversity.Autonomus_Status=="Autonomous"])
    puNa =len(puneUniversity[puneUniversity.Autonomus_Status=="Non-Autonomous"])


    category_names = ['Non-Autonomous','Autonomous']
    results = {
        'AMRAVATI': [amrNa,amrAu],
        'AURANGABAD': [aurna,aurAu],
        'MUMBAI': [mumNa,mumAu],
        'NAGPUR': [nagNa,nagAu],
        'NASHIK': [nasNa,nasAu],
        'PUNE': [puNa,puAu]
    }


    def survey(results, category_names):
        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(
            np.linspace(0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)
            xcenters = starts + widths / 2

            r, g, b, _ = color
            text_color = 'black' if r * g * b < 1 else 'darkgrey'
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                ax.text(x, y, str(int(c)), ha='center', va='center',
                        color=text_color)
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                loc='lower left', fontsize='large')

        return fig, ax

    survey(results, category_names)
    plt.savefig("static/Discrete Distribution of University wise Autonomous and Non-Autonomous.png")
    scaterdPlot(amravatiUniversity,aurangabadUniversity,mumbaiUniversity,nagpurUniversity,nashikUniversity,puneUniversity)
    amravatiDoubleGraph(amravatiUniversity)
    aurangabadDoubleGraph(aurangabadUniversity)
    mumbaiDoubleGraph(mumbaiUniversity)
    nagpurDoubleGraph(nagpurUniversity)
    nashikDoubleGraph(nashikUniversity)
    puneDoubleGraph(puneUniversity)

#Categorical Plot

def categoricalPlot(clgData):
        
    fig, ax = plt.subplots(figsize=(20,10))
    x=clgData["District"].value_counts()
    names = list(x.keys())
    values = [ x[i] for i in range (len(x))]

    plt.scatter(names, values)
    plt.plot(names, values)
    plt.xticks(rotation=80)
    plt.xlabel('Districts')
    plt.ylabel("College Count")
    plt.title("Categorical Representation of District Wise College Count")
    plt.savefig("static/Categorical Representation of District Wise College Count.png")

#Scattered Plot

def scaterdPlot(amravatiUniversity,aurangabadUniversity,mumbaiUniversity,nagpurUniversity,nashikUniversity,puneUniversity):
        
    fig, ax = plt.subplots(figsize=(20,10))
    category_name=["Amravati",'Aurangabad',"Mumbai",'Nagpur','Nashik','Pune']
    plt.ylim(['Girls Count Zero(yes)','Girls Count Not Zero(NO)'])
    plt.xlim([1000,7000])
    plt.axis([1000,7000,-0.5,1.5])
    plt.scatter(amravatiUniversity['ID'],amravatiUniversity['Girls_Total']>0,color='gold')
    plt.scatter(aurangabadUniversity['ID'],aurangabadUniversity['Girls_Total']>0,color='yellowgreen')
    plt.scatter(mumbaiUniversity['ID'],mumbaiUniversity['Girls_Total']>0,color='lightcoral')
    plt.scatter(nagpurUniversity['ID'],nagpurUniversity['Girls_Total']>0,color='lightskyBlue')
    plt.scatter(nashikUniversity['ID'],nashikUniversity['Girls_Total']>0,color='red')
    plt.scatter(puneUniversity['ID'],puneUniversity['Girls_Total']>0,color='green')
    plt.xlabel("College ID")
    plt.ylabel("College Status")
    plt.title("Check College Girls Count Zero or Not")
    plt.savefig("static/Check College Girls Count Zero or Not.png")

#Double Bar Graph Amravati

def amravatiDoubleGraph(amravatiUniversity):
        
    # data to plot
    n_groups = len(amravatiUniversity['ID'])
    men_means = amravatiUniversity['Boys_Total']
    women_means = amravatiUniversity['Girls_Total']

    # create plot
    fig, ax = plt.subplots(figsize=(20,10))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, men_means, bar_width,edgecolor='black',
    alpha=opacity,
    color='g',
    label='Boys')

    rects2 = plt.bar(index + bar_width, women_means, bar_width,edgecolor="black",
    alpha=opacity,
    color='r',
    label='Girls')

    plt.xlabel('College ID')
    plt.ylabel('Count OF Students')
    plt.title('Gender Count in Colleges In Amravati University')
    plt.xticks(index + bar_width,rotation=45,labels=amravatiUniversity['ID'])
    plt.legend()
    plt.savefig("static/Gender Count in Colleges In Amravati University.png")

#Double Bar Graph Aurangabad

def aurangabadDoubleGraph(aurangabadUniversity):
        
    # data to plot
    n_groups = len(aurangabadUniversity['ID'])
    men_means = aurangabadUniversity['Boys_Total']
    women_means = aurangabadUniversity['Girls_Total']

    # create plot
    fig, ax = plt.subplots(figsize=(20,10))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, men_means, bar_width,edgecolor='black',
    alpha=opacity,
    color='g',
    label='Boys')

    rects2 = plt.bar(index + bar_width, women_means, bar_width,edgecolor="black",
    alpha=opacity,
    color='r',
    label='Girls')

    plt.xlabel('College ID')
    plt.ylabel('Count OF Students')
    plt.title('Gender Count in Colleges In Aurangabad University')
    plt.xticks(index + bar_width,rotation=45,labels=aurangabadUniversity['ID'])
    plt.legend()
    plt.savefig("static/Gender Count in Colleges In Aurangabad University.png")

#Double Bar Graph Mumbai

def mumbaiDoubleGraph(mumbaiUniversity):
        
    # data to plot
    n_groups = len(mumbaiUniversity['ID'])
    men_means = mumbaiUniversity['Boys_Total']
    women_means = mumbaiUniversity['Girls_Total']

    # create plot
    fig, ax = plt.subplots(figsize=(20,10))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, men_means, bar_width,edgecolor='black',
    alpha=opacity,
    color='g',
    label='Boys')

    rects2 = plt.bar(index + bar_width, women_means, bar_width,edgecolor="black",
    alpha=opacity,
    color='r',
    label='Girls')

    plt.xlabel('College ID')
    plt.ylabel('Count OF Students')
    plt.title('Gender Count in Colleges Of Mumbai University')
    plt.xticks(index + bar_width,rotation=45,labels=mumbaiUniversity['ID'])
    plt.legend()
    plt.savefig("static/Gender Count in Colleges In Mumbai University.png")

#Double Bar Graph Nagpur

def nagpurDoubleGraph(nagpurUniversity):
        
    # data to plot
    n_groups = len(nagpurUniversity['ID'])
    men_means = nagpurUniversity['Boys_Total']
    women_means = nagpurUniversity['Girls_Total']

    # create plot
    fig, ax = plt.subplots(figsize=(20,10))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, men_means, bar_width,edgecolor='black',
    alpha=opacity,
    color='g',
    label='Boys')

    rects2 = plt.bar(index + bar_width, women_means, bar_width,edgecolor="black",
    alpha=opacity,
    color='r',
    label='Girls')

    plt.xlabel('College ID')
    plt.ylabel('Count OF Students')
    plt.title('Gender Count in Colleges Of Nagpur University')
    plt.xticks(index + bar_width,rotation=45,labels=nagpurUniversity['ID'])
    plt.legend()
    plt.savefig("static/Gender Count in Colleges In Nagpur University.png")

#Double Bar Graph Nashik

def nashikDoubleGraph(nashikUniversity):
        
    # data to plot
    n_groups = len(nashikUniversity['ID'])
    men_means = nashikUniversity['Boys_Total']
    women_means = nashikUniversity['Girls_Total']

    # create plot
    fig, ax = plt.subplots(figsize=(20,10))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, men_means, bar_width,edgecolor='black',
    alpha=opacity,
    color='g',
    label='Boys')

    rects2 = plt.bar(index + bar_width, women_means, bar_width,edgecolor="black",
    alpha=opacity,
    color='r',
    label='Girls')

    plt.xlabel('College ID')
    plt.ylabel('Count OF Students')
    plt.title('Gender Count in Colleges Of Nashik University')
    plt.xticks(index + bar_width,rotation=45,labels=nashikUniversity['ID'])
    plt.legend()
    plt.savefig("static/Gender Count in Colleges In Nashik University.png")

#Double Bar Graph Pune

def puneDoubleGraph(puneUniversity):
        
    # data to plot
    n_groups = len(puneUniversity['ID'])
    men_means = puneUniversity['Boys_Total']
    women_means = puneUniversity['Girls_Total']

    # create plot
    fig, ax = plt.subplots(figsize=(20,10))
    index = np.arange(n_groups)
    bar_width = 0.40
    opacity = 0.8

    rects1 = plt.bar(index, men_means, bar_width,edgecolor='black',
    alpha=opacity,
    color='g',
    label='Boys')

    rects2 = plt.bar(index + bar_width, women_means, bar_width,edgecolor="black",
    alpha=opacity,
    color='r',
    label='Girls')

    plt.xlabel('College ID')
    plt.ylabel('Count OF Students')

    plt.title('Gender Count in Colleges Of Pune University')
    plt.xticks(index + bar_width,rotation=80,labels=puneUniversity['ID'])
    plt.legend()
    plt.savefig("static/Gender Count in Colleges In Pune University.png")


#Genrate Plot Function

def genratePlots():

    #Reading CSV
    clgData=pd.read_csv('DTE Colleges.csv')
    pieDigram(clgData)
    discretGraph(clgData)
    categoricalPlot(clgData)




@app.route('/')
def index():
    genratePlots()                           #Call for genratePlot Function to genrete plots
    return render_template('index.html')     #Render The Template for visualization of data

if __name__=="__main__":
    app.run(debug=True)                   
    
    
    

