import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import requests
import json
import plotly.express as px


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#dataframce creation from SQL DB

#SQL connection to fetch data from the SQL DB

mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="1024",
                        database="phonepe_data",
                        port="5432")
cursor=mydb.cursor()

#aggregated_insurance_df

cursor.execute("select * from aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()
Aggregated_insurance=pd.DataFrame(table1, columns=("States","Year","Quater","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated_transactions_df
cursor.execute("select * from aggregated_transactions")
mydb.commit()
table2 = cursor.fetchall()
Aggregated_transactions=pd.DataFrame(table2, columns=("States","Year","Quater","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated_user_df
cursor.execute("select * from aggregated_user")
mydb.commit()
table3 = cursor.fetchall()
Aggregated_user=pd.DataFrame(table3,columns=("States","Year","Quater","Brands","Percentage","Transaction_count"))

#map insurance
cursor.execute("select * from map_insurance")
mydb.commit()
table4 = cursor.fetchall()
map_Insurance=pd.DataFrame(table4,columns=("States","Year","Quater","Districts","Amount","Transaction_count"))

#map transactions
cursor.execute("select * from map_transaction")
mydb.commit()
table5 = cursor.fetchall()
map_Transaction=pd.DataFrame(table5,columns=("States","Year","Quater","Districts","Amount","Transaction_count"))

#map user
cursor.execute("select * from map_user")
mydb.commit()
table6 = cursor.fetchall()
map_user=pd.DataFrame(table6,columns=("States","Year","Quater","Districts","Registered Users","App Opens"))

#Top Insurance
cursor.execute("select * from top_insurance")
mydb.commit()
table7 = cursor.fetchall()
top_Insurance=pd.DataFrame(table7,columns=("States","Year","Quater","Pincodes","Amount","Transaction Count"))

#Top user
cursor.execute("select * from top_users")
mydb.commit()
table9 = cursor.fetchall()
top_User=pd.DataFrame(table9,columns=("States","Year","Quater","Pincodes","Registered Users"))

#Top transactions
cursor.execute("select * from top_transactions")
mydb.commit()
table10 = cursor.fetchall()
top_trans=pd.DataFrame(table10,columns=("States","Year","Quater","Pincodes","amount","transaction_count"))

#All Transactions
all_Trans=pd.concat([Aggregated_insurance,Aggregated_transactions])
map_all_trans=pd.concat([map_Insurance,map_Transaction])
top_all_trans=pd.concat([top_Insurance,top_trans])

#data for plotting geospatial data
url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response=requests.get(url)
datax=json.loads(response.content)
states_name=[]
for feature in datax["features"]:
    states_name.append(feature["properties"]["ST_NM"])
states_name.sort()    

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Streamlit section
st.set_page_config(layout="wide")
st.title(':violet[Phonepe Data Visualization]')

with st.sidebar:
    selected=option_menu("Menu",["Home","Analysis"])

# Home Tab
if selected == "Home":
    
    col1,col2=st.columns(2)
    with col1:
        st.markdown("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")        
        st.link_button("Official Website", "https://www.phonepe.com/pulse/")                
        st.link_button("Wikipedia page", "https://en.wikipedia.org/wiki/PhonePe")
        st.download_button("Download App", "https://www.phonepe.com/app-download/")
        st.empty()
        
    with col2:
        video_url='https://www.phonepe.com/pulse/videos/pulse-video.mp4?v=1'
        st.video(video_url)

    st.divider()
    st.write("The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a SQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
        


# ANALYSIS TAB
if selected == "Analysis":
    st.subheader(':violet[Analysis done on the basis of All India ,States and Top Charts between 2018 and 2023]')
     
    select = option_menu(None,
        options=["Nationwide", "State", "Top Charts" ],
        default_index=0,
        orientation="horizontal",
        styles={"container": {"width": "100%"},
                "nav-link": {"font-size": "16px", "text-align": "center", "margin": "-2px"},
                "nav-link-selected": {"background-color": "#6F36AD"}})
    ##Nationwide section##
    if select == "Nationwide":
        tab1, tab2 = st.tabs(["Transaction data","User data"])

        # TRANSACTION TAB
        with tab1:
            col1, col2, col3 = st.columns(3)
            # Select the year
            with col1:
                years = ["All"] + list(all_Trans['Year'].sort_values(ascending=True).unique())
                selected_year = st.select_slider("Select the year", years)

            # Select the quarter
            with col2:
                    quarter_options = ["All"] + list(all_Trans['Quater'].sort_values(ascending=True).unique())
                    quarter = st.select_slider("Select Quarter",quarter_options)

            # Select the transaction type
            with col3:
                transaction_types = ["All"] + list(all_Trans["Transaction_type"].unique())
                selected_transaction_type = st.selectbox("Select the transaction type", transaction_types)

            # Filtered dataframe
            filtered_df = all_Trans.copy()
            if selected_year != "All":
                filtered_df = filtered_df[filtered_df['Year'] == selected_year]
            if quarter != "All":
                filtered_df = filtered_df[filtered_df['Quater'] == quarter]
            if selected_transaction_type != "All":
                filtered_df = filtered_df[filtered_df['Transaction_type'] == selected_transaction_type]
            
            #info tab info
            totalamount=float(filtered_df['Transaction_amount'].sum())
            totalcount=(filtered_df['Transaction_count'].sum())
            Averageamount=float(filtered_df['Transaction_amount'].mean())
            
            col1,col2=st.columns(2)
            infotab1,infotab2,infotab3=st.columns(3,gap='small')
            with infotab1:
                st.info('Total Transaction Amount')
                st.metric(label='Rupees',value=f"{totalamount:,.0f}")
            with infotab2:
                st.info('Average Amount Transacted')
                st.metric(label='Rupees',value=f"{Averageamount:,.0f}")
            with infotab3:
                st.info('Total Transaction Count')
                st.metric(label='#',value=f"{totalcount:,.0f}")
            col1,col2=st.columns(2)
            with col1:
                compute = st.radio("view",["Transaction Amount", "Transaction Count"],
                captions = ["Total Amount Transacted", "Count of Transactions"],horizontal=True)

            if compute == "Transaction Amount":
         
                fig_india1=px.choropleth(filtered_df, geojson=datax, locations="States",featureidkey="properties.ST_NM", color="Transaction_amount", color_continuous_scale="thermal", 
                                    hover_name="States", title=f"Transaction Amount for the Year {selected_year} Year {quarter} Quarter and Transaction type {selected_transaction_type}",
                                    fitbounds="locations",height=1000)
                fig_india1.update_geos(visible=False)
                fig_india1.update_layout(dragmode=False)
                st.plotly_chart(fig_india1,use_container_width=True,height=1000)
                
                #heatmap
                hdata = filtered_df.groupby(['States'])['Transaction_amount'].sum().reset_index()                
                fig_tmap = px.treemap(hdata, path=['States'], values='Transaction_amount',
                        color='Transaction_amount', hover_data=['Transaction_amount'],
                        color_continuous_scale='thermal',height=700,title='Total Amount transacted by statewise')
                fig_tmap.update_traces(textinfo='label+value')
                st.plotly_chart(fig_tmap,use_container_width=True)
                    
            elif compute == "Transaction Count":            
                fig_india1=px.choropleth(filtered_df, geojson=datax, locations="States",featureidkey="properties.ST_NM", color="Transaction_count", color_continuous_scale="thermal", 
                                    hover_name="States", title=f"Transaction count for the Year {selected_year} Year {quarter} Quarter and Transaction type {selected_transaction_type}",
                                    fitbounds="locations",height=1000)
                fig_india1.update_geos(visible=False)
                fig_india1.update_layout(dragmode=False)                
                st.plotly_chart(fig_india1,use_container_width=True,height=1000)
                #heatmap
                hdata = filtered_df.groupby(['States'])['Transaction_count'].sum().reset_index()                
                fig_tmap = px.treemap(hdata, path=['States'], values='Transaction_count',
                        color='Transaction_count', hover_data=['Transaction_count'],
                        color_continuous_scale='thermal',height=700,title='Total count transacted by statewise')
                fig_tmap.update_traces(textinfo='label+value')
                st.plotly_chart(fig_tmap,use_container_width=True)

            #bar and line plots
            count_states=filtered_df.groupby(by='States').sum().reset_index()
            col1,col2=st.columns(2)
            with col1:
                fig_line=px.line(count_states,x='States',y='Transaction_count',title='Transaction count',width=900)
                st.plotly_chart(fig_line)
            with col2:
                fig_bar=px.bar(count_states,x='States',y='Transaction_amount',title='Transaction amount',width=900)
                st.plotly_chart(fig_bar)

        ## UsersTAB
        with tab2:
            col1, col2, col3 = st.columns(3)
            # Select the year
            with col1:
                years = ["All"] + list(Aggregated_user['Year'].sort_values(ascending=True).unique())
                selected_year = st.select_slider("Select the year", years, key='user_year_slider')

            # Select the quarter
            with col2:
                quarter_options = ["All"] + list(Aggregated_user['Quater'].sort_values(ascending=True).unique())
                quarter = st.select_slider("Select Quarter", quarter_options, key='user_quarter_slider')

            # Filter dataframe
            filtered_df = Aggregated_user.copy()
            if selected_year != "All":
                filtered_df = filtered_df[filtered_df['Year'] == selected_year]
            if quarter != "All":
                filtered_df = filtered_df[filtered_df['Quater'] == quarter]
                
            # Filtered map user dataframe as reg users and app opens are available in this dataframe
            filtered_m_df = map_user.copy()
            if selected_year != "All":
                filtered_m_df = filtered_m_df[filtered_m_df['Year'] == selected_year]
            if quarter != "All":
                filtered_m_df = filtered_m_df[filtered_m_df['Quater'] == quarter]

            #info tab info
            Transaction_count=float(filtered_df['Transaction_count'].sum())
            Registeredusers=(filtered_m_df['Registered Users'].sum())
            App_opens=(filtered_m_df['App Opens'].sum())

            infotab1,infotab2,infotab3=st.columns(3,gap='small')
            with infotab1:
                st.info('Transaction Count')
                st.metric(label='#',value=f"{Transaction_count:,.0f}")
            with infotab2:
                st.info('Registered Users')
                st.metric(label='#',value=f"{Registeredusers:,.0f}")
            with infotab3:
                st.info('App opens')
                st.metric(label='#',value=f"{App_opens:,.0f}")
            
            col1,col2=st.columns(2)
            with col1:
                compute = st.radio("view",["Transaction Count", "Registered Users",'App opens'],
                captions = ["Total transaction", "Count of registered users","App open count"],horizontal=True)

            if compute == "Transaction Count":            
                fig_india1=px.choropleth(filtered_df, geojson=datax, locations="States",featureidkey="properties.ST_NM", color="Transaction_count", color_continuous_scale="thermal", 
                                    hover_name="States", title=f"Transaction count for the Year {selected_year} Year {quarter} Quarter",
                                    fitbounds="locations",height=1000)
                fig_india1.update_geos(visible=False)
                fig_india1.update_layout(dragmode=False)
                st.plotly_chart(fig_india1,use_container_width=True,height=1000)

                #heatmap
                hdata = filtered_df.groupby(['States'])['Transaction_count'].sum().reset_index()                
                fig_tmap = px.treemap(hdata, path=['States'], values='Transaction_count',
                        color='Transaction_count', hover_data=['Transaction_count'],
                        color_continuous_scale='thermal',height=700,title='Total Amount transacted by statewise')
                fig_tmap.update_traces(textinfo='label+value')
                st.plotly_chart(fig_tmap,use_container_width=True)

                #Bar plot
                bdata=filtered_df.groupby(['Brands'])['Transaction_count'].sum().reset_index()
                fig_bar=px.bar(bdata.sort_values(by='Transaction_count',ascending=True),x='Transaction_count',y='Brands',orientation='h',width=1200,title='Transaction Count by device brands')
                st.plotly_chart(fig_bar)

            elif compute == "Registered Users":
                fig_india1=px.choropleth(filtered_m_df, geojson=datax, locations="States",featureidkey="properties.ST_NM", color="Registered Users", color_continuous_scale="thermal", 
                                    hover_name="States", title=f"Registered users for the Year {selected_year} Year {quarter} Quarter",
                                    fitbounds="locations",height=1000)
                fig_india1.update_geos(visible=False)
                fig_india1.update_layout(dragmode=False)
                st.plotly_chart(fig_india1,use_container_width=True,height=1000)

                #heatmap
                filtered_m_df['State_District'] = filtered_m_df['States'] + ' - ' + filtered_m_df['Districts']
                hdata = filtered_m_df.groupby(['States','Districts'])['Registered Users'].sum().reset_index()                
                fig_tmap = px.treemap(hdata, path=['States','Districts'], values='Registered Users',
                        color='Registered Users', hover_data=['Registered Users'],
                        color_continuous_scale='thermal',height=700,title='Registered Users')
                fig_tmap.update_traces(textinfo='label+value')
                st.plotly_chart(fig_tmap,use_container_width=True)

            elif compute == "App opens":
                fig_india1=px.choropleth(filtered_m_df, geojson=datax, locations="States",featureidkey="properties.ST_NM", color="App Opens", color_continuous_scale="thermal", 
                                    hover_name="States", title=f"App Opens for the Year {selected_year} Year {quarter} Quarter",
                                    fitbounds="locations",height=1000)
                fig_india1.update_geos(visible=False)
                fig_india1.update_layout(dragmode=False)
                st.plotly_chart(fig_india1,use_container_width=True,height=1000)

                #heatmap                
                hdata = filtered_m_df.groupby(['States','Districts'])['App Opens'].sum().reset_index()                
                fig_tmap = px.treemap(hdata, path=['States','Districts'], values='App Opens',
                        color='App Opens', hover_data=['App Opens'],
                        color_continuous_scale='thermal',height=700,title='App opens')
                fig_tmap.update_traces(textinfo='label+value')
                st.plotly_chart(fig_tmap,use_container_width=True)
    
    ## State wise section##
    
    elif select == "State":

        all_Trans=pd.concat([map_Insurance,map_Transaction])
        
        # TRANSACTION TAB
        col1, col2, col3 ,col4= st.columns(4)
        # Select the year
        with col1:
            years = ["All"] + list(all_Trans['Year'].sort_values(ascending=True).unique())
            selected_year = st.select_slider("Select the year", years)

        # Select the quarter
        with col2:
            quarter_options = ["All"] + list(all_Trans['Quater'].sort_values(ascending=True).unique())
            quarter = st.select_slider("Select Quarter",quarter_options)

        # Select State
        with col3:
            state_options=['All'] + list(all_Trans['States'].unique())
            selected_state=st.selectbox("Select The State",state_options)
        st.markdown('<hr>', unsafe_allow_html=True)

        # Filter dataframe
        filtered_df = all_Trans.copy()
        if selected_year != "All":
            filtered_df = filtered_df[filtered_df['Year'] == selected_year]
        if quarter != "All":
            filtered_df = filtered_df[filtered_df['Quater'] == quarter]

        if selected_state != "All":
            filtered_df = filtered_df[filtered_df['States'] == selected_state]

        # Filter dataframe
        filtered_ttype_df = pd.concat([Aggregated_insurance,Aggregated_transactions]).copy()
        if selected_year != "All":
            filtered_ttype_df = filtered_ttype_df[filtered_ttype_df['Year'] == selected_year]
        if quarter != "All":
            filtered_ttype_df = filtered_ttype_df[filtered_ttype_df['Quater'] == quarter]
        if selected_state != "All":
            filtered_ttype_df = filtered_ttype_df[filtered_ttype_df['States'] == selected_state]

        #info tab info
        totalamount=float(filtered_df['Amount'].sum())
        totalcount=(filtered_df['Transaction_count'].sum())
        Averageamount=float(filtered_df['Amount'].mean())
        col1,col2=st.columns(2)
        
        infotab1,infotab2,infotab3=st.columns(3,gap='small')
        with infotab1:
            st.info('Total Transaction Amount')
            st.metric(label='Rupees',value=f"{totalamount:,.0f}")            
        with infotab2:
            st.info('Average Amount Transacted')
            st.metric(label='Rupees',value=f"{Averageamount:,.0f}")
        with infotab3:
            st.info('Total Transaction Count')
            st.metric(label='#',value=f"{totalcount:,.0f}")

        st.markdown('<hr>', unsafe_allow_html=True)

        with col1:
            compute = st.radio("view",["Transaction Amount", "Transaction Count"],
            captions = ["Total Amount Transacted", "Count of Transactions"],horizontal=True)

        if compute == "Transaction Amount":
            fig_india1=px.choropleth(filtered_df, geojson=datax, locations="States",featureidkey="properties.ST_NM", color="Amount", color_continuous_scale="thermal", 
                                hover_name="States", title=f"Transaction Amount for the Year {selected_year} Year {quarter} Quarter",
                                fitbounds="locations",height=1000)
            fig_india1.update_geos(visible=False)
            fig_india1.update_layout(dragmode=False)
            st.plotly_chart(fig_india1,use_container_width=True,height=1000)

            #heatmap
            filtered_df['State_District'] = filtered_df['States'] + ' - ' + filtered_df['Districts']
            hdata = filtered_df.groupby(['States','Districts'])['Amount'].sum().reset_index()                
            fig_tmap = px.treemap(hdata, path=['States','Districts'], values='Amount',
                    color='Amount', hover_data=['Amount'],
                    color_continuous_scale='thermal',height=700)
            fig_tmap.update_traces(textinfo='label+value')
            st.plotly_chart(fig_tmap,use_container_width=True)

        if compute == "Transaction Count":
            fig_india1=px.choropleth(filtered_df, geojson=datax, locations="States",featureidkey="properties.ST_NM", color="Transaction_count", color_continuous_scale="thermal", 
                                hover_name="States", title=f"Transaction count for the Year {selected_year} Year {quarter} Quarter",
                                fitbounds="locations",height=1000)
            fig_india1.update_geos(visible=False)
            fig_india1.update_layout(dragmode=False)
            st.plotly_chart(fig_india1,use_container_width=True,height=1000)

            #heatmap
            filtered_df['State_District'] = filtered_df['States'] + ' - ' + filtered_df['Districts']
            hdata = filtered_df.groupby(['States','Districts'])['Transaction_count'].sum().reset_index()                
            fig_tmap = px.treemap(hdata, path=['States','Districts'], values='Transaction_count',
                    color='Transaction_count', hover_data=['Transaction_count'],
                    color_continuous_scale='thermal',height=700)
            fig_tmap.update_traces(textinfo='label+value')
            st.plotly_chart(fig_tmap,use_container_width=True)


        col1,col2=st.columns(2)

        with col1:     
                fig_pie=px.pie(filtered_ttype_df,values='Transaction_amount',names='Transaction_type',hole=0.5,height=500)
                fig_pie.update_layout(
                    annotations=[dict(text='Amount', x=0.5, y=0.5, font_size=20, showarrow=False)])
                st.plotly_chart(fig_pie,use_container_width=True)

        with col2:
                fig_pie=px.pie(filtered_ttype_df,values='Transaction_count',names='Transaction_type',hole=0.5,height=500)
                fig_pie.update_layout(
                    annotations=[dict(text='count', x=0.5, y=0.5, font_size=20, showarrow=False)])
                st.plotly_chart(fig_pie,use_container_width=True)
    
    ##Top Charts section##
    elif select == "Top Charts":
            col1, col2, col3 = st.columns(3)
            # Select the year
            with col1:
                years = ["All"] + list(all_Trans['Year'].sort_values(ascending=True).unique())
                selected_year = st.select_slider("Select the year", years)

            # Select the quarter
            with col2:
                    quarter_options = ["All"] + list(all_Trans['Quater'].sort_values(ascending=True).unique())
                    quarter = st.select_slider("Select Quarter",quarter_options)

            # Filter on all transactions dataframe
            filtered_df = all_Trans.copy()
            if selected_year != "All":
                filtered_df = filtered_df[filtered_df['Year'] == selected_year]
            if quarter != "All":
                filtered_df = filtered_df[filtered_df['Quater'] == quarter]

            #filter on district level data
            filtered_ddf=map_all_trans.copy()
            if selected_year != "All":
                filtered_ddf = filtered_ddf[filtered_ddf['Year'] == selected_year]
            if quarter != "All":
                filtered_ddf = filtered_ddf[filtered_ddf['Quater'] == quarter]

            #filter on pincode level data
            filtered_pdf=top_trans.copy()
            if selected_year != "All":
                filtered_pdf = filtered_pdf[filtered_pdf['Year'] == selected_year]
            if quarter != "All":
                filtered_pdf = filtered_pdf[filtered_pdf['Quater'] == quarter]            

           
            #info tab info
            totalamount=float(filtered_df['Transaction_amount'].sum())
            totalcount=(filtered_df['Transaction_count'].sum())
            Averageamount=float(filtered_df['Transaction_amount'].mean())
            
            col1,col2=st.columns(2)
            infotab1,infotab2,infotab3=st.columns(3,gap='small')
            with infotab1:
                st.info('Total Transaction Amount')
                st.metric(label='Rupees',value=f"{totalamount:,.0f}")
            with infotab2:
                st.info('Average Amount Transacted')
                st.metric(label='Rupees',value=f"{Averageamount:,.0f}")
            with infotab3:
                st.info('Total Transaction Count')
                st.metric(label='#',value=f"{totalcount:,.0f}")
                 
            col1,col2,col3=st.columns(3)

            with col3:
                st.markdown('Categories')
                top_ten_categories=filtered_df[['Transaction_type','Transaction_amount']].groupby(by='Transaction_type').sum()
                st.dataframe(top_ten_categories.sort_values(by='Transaction_amount',ascending=False))
                
                tab1,tab2,tab3=st.tabs(['States','Districts','Pincodes'])
                with tab1:
                    st.markdown('Top Ten States')
                    top_ten_states=filtered_df.groupby(by='States')['Transaction_amount'].sum().sort_values(ascending=False).head(10)
                    st.dataframe(top_ten_states,width=300)
                with tab2:
                    st.markdown('Top Ten Districts')
                    top_ten_districts=filtered_ddf.groupby(by='Districts')['Amount'].sum().sort_values(ascending=False).head(10)
                    st.dataframe(top_ten_districts,width=300)
                with tab3:
                    st.markdown('Top Ten Pincodes')
                    top_ten_pincodes=filtered_pdf.groupby(by='Pincodes')['amount'].sum().sort_values(ascending=False).head(10)
                    st.dataframe(top_ten_pincodes,width=300)

            with col1:
                                                              
                fig = px.line_polar(top_ten_categories.reset_index(), r='Transaction_amount', theta='Transaction_type',
                                 log_r=True, template='plotly_dark',line_close=True)
                fig.update_traces(fill='toself')

                st.plotly_chart(fig)

                fig4=px.pie(filtered_df.groupby(by='States')['Transaction_amount'].sum().reset_index().sort_values(by='Transaction_amount',ascending=False).head(10)
                            ,values='Transaction_amount',names='States',hole=0.6,title="Top Ten States")
                st.plotly_chart(fig4)

                fig5=px.bar(top_ten_districts.reset_index(),
                            y='Amount',x='Districts',title="Top Ten Districts")
                st.plotly_chart(fig5)

            #user data on top charts page

            st.header('User Data')
            col1, col2, col3 = st.columns(3)

            # Select the year
            with col1:
                years = ["All"] + list(Aggregated_user['Year'].sort_values(ascending=True).unique())
                selected_year = st.select_slider("Select the year", years, key='user_year_slider')

            # Select the quarter
            with col2:
                quarter_options = ["All"] + list(Aggregated_user['Quater'].sort_values(ascending=True).unique())
                quarter = st.select_slider("Select Quarter", quarter_options, key='user_quarter_slider')

            # Filter dataframe
            filtered_df = Aggregated_user.copy()
            if selected_year != "All":
                filtered_df = filtered_df[filtered_df['Year'] == selected_year]
            if quarter != "All":
                filtered_df = filtered_df[filtered_df['Quater'] == quarter]
                
            # Filtered map user dataframe as reg users and app opens are available in this dataframe
            filtered_m_df = map_user
            if selected_year != "All":
                filtered_m_df = filtered_m_df[filtered_m_df['Year'] == selected_year]
            if quarter != "All":
                filtered_m_df = filtered_m_df[filtered_m_df['Quater'] == quarter]
            
            # Filtered top user dataframe as reg users at a pincode level are available in this dataframe
            filtered_p_df = top_User.copy()
            if selected_year != "All":
                filtered_p_df = filtered_p_df[filtered_p_df['Year'] == selected_year]
            if quarter != "All":
                filtered_p_df = filtered_p_df[filtered_p_df['Quater'] == quarter]

            #info tab info
            Transaction_count=float(filtered_df['Transaction_count'].sum())
            Registeredusers=(filtered_m_df['Registered Users'].sum())
            App_opens=(filtered_m_df['App Opens'].sum())

            col1,col2=st.columns(2)
            infotab1,infotab2,infotab3=st.columns(3,gap='small')
            with infotab1:
                st.info('Transaction Count')
                st.metric(label='#',value=f"{Transaction_count:,.0f}")
            with infotab2:
                st.info('Registered Users')
                st.metric(label='#',value=f"{Registeredusers:,.0f}")
            with infotab3:
                st.info('App opens')
                st.metric(label='#',value=f"{App_opens:,.0f}")
            col1,col2,col3=st.columns(3)

            with col3:
                st.markdown('Top Ten mobile brands ')
                top_brands=filtered_df.groupby(by='Brands')['Transaction_count'].sum().sort_values(ascending=False).head(10)
                st.dataframe(top_brands,width=300)


                st.markdown('Registered users')
                tab1,tab2,tab3=st.tabs(['States','Districts','Pincodes'])
                with tab1:
                    st.markdown('Top Ten States')
                    top_ten_states=filtered_m_df.groupby(by='States')['Registered Users'].sum().sort_values(ascending=False).head(10)
                    st.dataframe(top_ten_states,width=300)
                with tab2:
                    st.markdown('Top Ten Districts')
                    top_ten_districts=filtered_m_df.groupby(by='Districts')['Registered Users'].sum().sort_values(ascending=False).head(10)
                    st.dataframe(top_ten_districts,width=300)
                with tab3:
                    st.markdown('Top Ten Pincodes')
                    top_ten_pincodes=filtered_p_df.groupby(by='Pincodes')['Registered Users'].sum().sort_values(ascending=False).head(10)
                    st.dataframe(top_ten_pincodes,width=300)

                st.markdown('App Opens')
                tab1,tab2=st.tabs(['States','Districts'])
                with tab1:
                    st.markdown('Top Ten States')
                    top_ten_states=filtered_m_df.groupby(by='States')['App Opens'].sum().sort_values(ascending=False).head(10)
                    st.dataframe(top_ten_states,width=300)
                with tab2:
                    st.markdown('Top Ten Districts')
                    top_ten_districts=filtered_m_df.groupby(by='Districts')['App Opens'].sum().sort_values(ascending=False).head(10)
                    st.dataframe(top_ten_districts,width=300)
                


            with col1:
                fig7=px.pie(top_brands.reset_index(),values='Transaction_count',names='Brands',hole=0.6,title="Top Ten Brands")
                st.plotly_chart(fig7)

                fig8=px.bar(filtered_m_df.groupby('States')['Registered Users'].sum().sort_values(ascending=False).reset_index().head(10),
                            x='States',y='Registered Users',color_continuous_scale='Thermal')
                st.plotly_chart(fig8)

                fig9=px.bar(filtered_m_df.groupby('Districts')['Registered Users'].sum().sort_values(ascending=False).reset_index().head(10),x='Districts',y='Registered Users')
                st.plotly_chart(fig9)

                fig10=px.line(filtered_m_df.groupby('States')['App Opens'].sum().sort_values(ascending=False).reset_index().head(10),x='States',y='App Opens')
                st.plotly_chart(fig10)

                fig11=px.line(filtered_m_df.groupby('Districts')['App Opens'].sum().sort_values(ascending=False).reset_index().head(10),x='Districts',y='App Opens')
                st.plotly_chart(fig11)