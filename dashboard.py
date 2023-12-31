import pandas as pd
import panel as pn
import plotly.graph_objs as go
import holoviews as hv
from holoviews import opts
import param

# Load the dataset
df = pd.read_csv('StudentsPerformance.csv')
df ["average score"] = (df ['math score'] + df['reading score'] + df['writing score']) /3 

class student_EDA (param.Parameterized): 


    gender_list= (list)(df["gender"].unique())
    gender_list.append('ALL')
    gender_widget  =param.ObjectSelector(default='ALL',objects=gender_list,label="Gender")

    race_ethnicity_list= (list)(df["race/ethnicity"].unique())
    race_ethnicity_list.append('ALL')
    race_ethnicity_widget  = param.ObjectSelector(default='ALL',objects=race_ethnicity_list,label="Race/Ethnicity")

    parental_level_of_education_list = (list)(df["parental level of education"].unique())
    parental_level_of_education_list.append('ALL')
    parental_level_of_education_widget  = param.ObjectSelector(default='ALL',objects=parental_level_of_education_list,label="Parental level of education")
    
    lunch_list= (list)(df["lunch"].unique())
    lunch_list.append('ALL')
    lunch_widget = param.ObjectSelector(default='ALL',objects=lunch_list,label="Lunch")

    test_prep_list= (list)(df["test preparation course"].unique())
    test_prep_list.append('ALL')
    test_preparation_course_widget  = param.ObjectSelector(default='ALL',objects=test_prep_list,label="Test preparation course")
    
    math_widget = param.Number(0, bounds=(0, 100))
    reading_widget  = param.Number(0, bounds=(0, 100))
    writing_widget  = param.Number(0, bounds=(0, 100))
    average_widget  = param.Number(0, bounds=(0, 100))




    @param.depends('gender_widget','race_ethnicity_widget','parental_level_of_education_widget','lunch_widget','test_preparation_course_widget','math_widget','reading_widget','writing_widget','average_widget',watch=True, on_init=False)
    def table (self):
         # Define the filters dictionary and filter_table widget
        filters = {
        'gender': {'type': 'input', 'func': 'like', 'placeholder': 'Enter gender'},
        'race/ethnicity': {'type': 'input','placeholder': 'Enter race'},
        'parental level of education': {'type': 'input', 'func': 'like', 'placeholder': 'Enter parental level of education'},
        'lunch': {'type': 'input', 'func': 'like', 'placeholder': 'Enter director'},
        'test preparation course': {'type': 'input', 'func': 'like', 'placeholder': 'Enter writer'},
        'reading score': {'type': 'number', 'func': '>=', 'placeholder': 'Enter minimum reading score'},
        'math score': {'type': 'number', 'func': '>=', 'placeholder': 'Enter minimum math score'},
        'writing score': {'type': 'number', 'func': '>=', 'placeholder': 'Enter minimum rating'}
         }
        df1=df
        if (self.gender_widget!='ALL'):
            df1 = df1[df1['gender']==self.gender_widget]

        if (self.race_ethnicity_widget!='ALL'):
            df1 = df1[df1['race/ethnicity']==self.race_ethnicity_widget]

        if (self.parental_level_of_education_widget!='ALL'):
            df1 = df1[df1["parental level of education"]==self.parental_level_of_education_widget]

        if (self.lunch_widget!='ALL'):
            df1 = df1[df1['lunch']==self.lunch_widget]

        if (self.test_preparation_course_widget!='ALL'):
            df1 = df1[df1['test preparation course']==self.test_preparation_course_widget]
        df1 = df1[df1['math score']>=self.math_widget]
        df1 = df1[df1['reading score']>=self.reading_widget]
        df1 = df1[df1['writing score']>=self.writing_widget]
        df1 = df1[df1['average score']>=self.average_widget]
        
        total_student = len(df1)
        success_df = df1[df1["average score"]>=60]
        total_success = len(success_df)
        filter_table =pn.widgets.Tabulator(df1, pagination='remote', layout='fit_columns', page_size=10, sizing_mode='stretch_width')
        
        # Create a plotly figure object
        fig = go.Figure()

        # Add a text annotation to the figure
        fig.add_annotation(
            x=0.5,
            y=0.5,
            xref='paper',
            yref='paper',
            text=str(total_student),
            font=dict(size=36, color='#C91B26'),
            #bgcolor='blue',
            showarrow=False
        )

        # Update the plot layout
        fig.update_layout(
            title="Number of Students",
            title_font=dict(size=14),

            width=150,
            height=150,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        # Create a plotly figure object
        fig1 = go.Figure()

        # Add a text annotation to the figure
        fig1.add_annotation(
            x=0.5,
            y=0.5,
            xref='paper',
            yref='paper',
            text=str(total_success),
            font=dict(size=36, color='#C91B26'),
            #bgcolor='blue',
            showarrow=False
        )

        # Update the plot layout
        fig1.update_layout(
            title="Number of graduates",
            title_font=dict(size=14),
            width=150,
            height=150,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )

        return  pn.Row(
            pn.Column(
            pn.Row(fig),
            pn.Row(fig1)
            ),
            pn.Spacer(width=10),  # Add some spacing between the sidebar and the filter_table
            pn.Column(filter_table, height=500, sizing_mode='stretch_both', width_policy='max'),
            sizing_mode='stretch_both'
        )  
   

    @param.depends('gender_widget','race_ethnicity_widget','parental_level_of_education_widget','lunch_widget','test_preparation_course_widget','math_widget','reading_widget','writing_widget',watch=True, on_init=False)
    def plots1(self):
        df1=df
        if (self.gender_widget!='ALL'):
            df1 = df1[df1['gender']==self.gender_widget]

        if (self.race_ethnicity_widget!='ALL'):
            df1 = df1[df1['race/ethnicity']==self.race_ethnicity_widget]

        if (self.parental_level_of_education_widget!='ALL'):
            df1 = df1[df1["parental level of education"]==self.parental_level_of_education_widget]

        if (self.lunch_widget!='ALL'):
            df1 = df1[df1['lunch']==self.lunch_widget]

        if (self.test_preparation_course_widget!='ALL'):
            df1 = df1[df1['test preparation course']==self.test_preparation_course_widget]
            
        df1 = df1[df1['math score']>=self.math_widget]
        df1 = df1[df1['reading score']>=self.reading_widget]
        df1 = df1[df1['writing score']>=self.writing_widget]
        df1 = df1[df1['average score']>=self.average_widget] 
        fig1 = go.Figure()

        for gender in df1['gender'].unique():
            data = df1[df1['gender']==gender]['average score']
            fig1.add_trace(go.Histogram(x=data, name=gender, opacity=0.75, 
                                        marker=dict(color='#160A47' if gender=='male' else ' #C91B26')))
            
        fig1.update_layout(barmode='group', width=890, height=450, xaxis_title='Average Score', yaxis_title='Frequency', 
                        title='Average Scores by Gender')
        grid3 = pn.Row(
        fig1, sizing_mode='stretch_both', width_policy='max'
    ) 

        # fig1.show()
        return grid3
    @param.depends('gender_widget','race_ethnicity_widget','parental_level_of_education_widget','lunch_widget','test_preparation_course_widget','math_widget','reading_widget','writing_widget',watch=True, on_init=False)
    def plots2(self):
        df1=df
        if (self.gender_widget!='ALL'):
            df1 = df1[df1['gender']==self.gender_widget]

        if (self.race_ethnicity_widget!='ALL'):
            df1 = df1[df1['race/ethnicity']==self.race_ethnicity_widget]

        if (self.parental_level_of_education_widget!='ALL'):
            df1 = df1[df1["parental level of education"]==self.parental_level_of_education_widget]

        if (self.lunch_widget!='ALL'):
            df1 = df1[df1['lunch']==self.lunch_widget]

        if (self.test_preparation_course_widget!='ALL'):
            df1 = df1[df1['test preparation course']==self.test_preparation_course_widget]
            
        df1 = df1[df1['math score']>=self.math_widget]
        df1 = df1[df1['reading score']>=self.reading_widget]
        df1 = df1[df1['writing score']>=self.writing_widget]
        df1 = df1[df1['average score']>=self.average_widget]
        data = [go.Box(x =df1['reading score'],
                    showlegend=False,
                    name = 'Reading Score',
                     marker=dict(color='#160A47')),
                go.Box(x=df1['writing score'],
                    showlegend=False,
                    name = 'Writing Score', marker=dict(color='#9C0F5F')),
                go.Box(x=df1['math score'],
                    showlegend=False,
                    name = 'Math Score', marker=dict(color='#C91B26')),
                go.Box(x=df1['average score'],
                showlegend=False,
                name = 'Average Score', marker=dict(color='#F2671F'))]
                

        layout = go.Layout(title={'text': "Scores",
                                'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                        width = 890,
                        height=450,
                        )

        fig = go.Figure(data = data, layout = layout)
        grid3 = pn.Row(
        fig, sizing_mode='stretch_both', width_policy='max'
            ) 

        # fig1.show()
        return grid3
    
    @param.depends('gender_widget','race_ethnicity_widget','parental_level_of_education_widget','lunch_widget','test_preparation_course_widget','math_widget','reading_widget','writing_widget',watch=True, on_init=False)
    def plots3(self):
        df1=df
        if (self.gender_widget!='ALL'):
            df1 = df1[df1['gender']==self.gender_widget]

        if (self.race_ethnicity_widget!='ALL'):
            df1 = df1[df1['race/ethnicity']==self.race_ethnicity_widget]

        if (self.parental_level_of_education_widget!='ALL'):
            df1 = df1[df1["parental level of education"]==self.parental_level_of_education_widget]

        if (self.lunch_widget!='ALL'):
            df1 = df1[df1['lunch']==self.lunch_widget]

        if (self.test_preparation_course_widget!='ALL'):
            df1 = df1[df1['test preparation course']==self.test_preparation_course_widget]
            
        df1 = df1[df1['math score']>=self.math_widget]
        df1 = df1[df1['reading score']>=self.reading_widget]
        df1 = df1[df1['writing score']>=self.writing_widget]
        df1 = df1[df1['average score']>=self.average_widget]

        scatter_plot = go.Figure(data=go.Scatter(x=df1['writing score'], y=df1['reading score'], mode='markers', marker=dict(color=df1['average score'], colorscale='sunsetdark')))
        scatter_plot.update_layout(width=440, height=455, xaxis_title='Writing Score', yaxis_title='Reading Score', title='Scatter Plot of Writing Score vs Reading Score')
        scatter_plot1 = go.Figure()

        scatter_plot1.add_trace(go.Scatter(x=df1['math score'], y=df1['average score'], 
                                mode='markers', marker=dict(color='#C91B26')))

        scatter_plot1.update_layout(title='Scatter Plot of Math Score vs Average Score',
                        xaxis_title='Math Score', yaxis_title='Average Score',width=440, height=455)


        grid = pn.Row(
        pn.Column(scatter_plot, sizing_mode='stretch_both', width_policy='max'),
        pn.Spacer(width=10),
        pn.Column(scatter_plot1, sizing_mode='stretch_both', width_policy='max'),

    ) 

        # fig1.show()
        return grid
    
    @param.depends('gender_widget','race_ethnicity_widget','parental_level_of_education_widget','lunch_widget','test_preparation_course_widget','math_widget','reading_widget','writing_widget',watch=True, on_init=False)
    def plots4(self):
        df1=df
        if (self.gender_widget!='ALL'):
            df1 = df1[df1['gender']==self.gender_widget]

        if (self.race_ethnicity_widget!='ALL'):
            df1 = df1[df1['race/ethnicity']==self.race_ethnicity_widget]

        if (self.parental_level_of_education_widget!='ALL'):
            df1 = df1[df1["parental level of education"]==self.parental_level_of_education_widget]

        if (self.lunch_widget!='ALL'):
            df1 = df1[df1['lunch']==self.lunch_widget]

        if (self.test_preparation_course_widget!='ALL'):
            df1 = df1[df1['test preparation course']==self.test_preparation_course_widget]
            
        df1 = df1[df1['math score']>=self.math_widget]
        df1 = df1[df1['reading score']>=self.reading_widget]
        df1 = df1[df1['writing score']>=self.writing_widget]
        df1 = df1[df1['average score']>=self.average_widget]

        heatmap = go.Figure(go.Heatmap(x=df['race/ethnicity'],
                            y= df['lunch'],
                            z = df['average score'].values.tolist(),colorscale='sunset'))
        heatmap.update_layout(
            title={
        'text': 'Heatmap of Race/Ethnicity and Lunch<br>by Average score',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }      ,
                xaxis_title='Race/Ethnicity',
            yaxis_title='Lunch',
            width=440,
            height=455
        )

        heatmap1 = go.Figure(go.Heatmap(x=df['parental level of education'],
                            y= df['test preparation course'],
                            z = df['average score'].values.tolist(),colorscale='sunset'))
        heatmap1.update_layout(
                    title={
        'text': 'Heatmap of Parental education and Test preparation <br> by Average score',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }      ,       
                               
                               xaxis_title='Parental level of education', yaxis_title='Test preparation course',width=440, height=455)

        grid = pn.Row(
        pn.Column(heatmap, sizing_mode='stretch_both', width_policy='max'),
        pn.Spacer(width=10),
        pn.Column(heatmap1, sizing_mode='stretch_both', width_policy='max'),

    ) 

        # fig1.show()
        return grid
    
dashboard = student_EDA()
# Define a custom panel template with the grid layout
template = pn.template.FastListTemplate(
    title='Student dashboard',
    main=[dashboard.table,dashboard.plots1,dashboard.plots2,dashboard.plots3,dashboard.plots4],
    sidebar_width=305,
    header_background = "#A01346 ",
     header=[pn.pane.HTML("""
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        header {
            background-color: #A01346;
            color: white;
            width: 56rem;
        }
        
        .logo-container {
            display: flex;
            align-items: end;
            justify-content: end;
            
        }
        
        .logo-container a {
            display: flex;
            flex-direction: row;
            align-items: center;
            text-decoration: none;
            color: white;
            margin-right: 12px;
            
        }
        
        .logo {
            font-size: 1.4em;
            margin-bottom: 5px;
        }
        
        .logo-title {
            font-size: 1em;
            text-align: center;
            margin-left:5px;
            margin-bottom:10px;
        }
    </style>
</head>
<body>
    <header>
    
        <div class="logo-container">
             <a href="D:/Dauphine/M2/Projets s2/Projet_data_viz/data_viz/Main.html">
                <i class="fas fa-home logo"></i>
                <div class="logo-title">Home</div>
            </a>
            <a href="http://localhost:5006/ML">
            <i class="fas fa-laptop logo"></i>
                <div class="logo-title">Machine Learning</div>
            </a>
           
    
        </div>
    
    </header>
    <!-- rest of the page content goes here -->
</body>
</html>""")],
    theme_toggle = False,
    logo  = "ico.ico",

     sidebar=[pn.Param(dashboard.param,widgets={'math_widget':pn.widgets.FloatSlider,'reading_widget':pn.widgets.FloatSlider,'writing_widget':pn.widgets.FloatSlider, 'race_ethnicity_widget': pn.widgets.Select,'gender_widget': pn.widgets.Select, 'parental_level_of_education_widget': pn.widgets.Select, 'lunch_widget': pn.widgets.Select, 'test_preparation_course_widget': pn.widgets.Select})]
)

# Show the template in a browser tab
template.servable()