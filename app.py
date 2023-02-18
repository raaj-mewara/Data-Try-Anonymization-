import streamlit as st
from PIL import Image
import pandas as pd
import re
import hashlib
def make_hashes(password):   
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,Email,password,Cpassword) VALUES (?,?,?,?,?,?)',(FirstName,LastName,Mobile,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_rule():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data
  
st.title("Welcome To Data Stream Anonymization")
menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)
if choice=="Home":
    original_title="<p style='text-align: center;'>Annonymization provide  privacy by grouping the data. So the privacy of the class is limited. Here we provide privacy as well as protection by propose idea of encryption. As there is many terms in data that are confidential so here our idea is to protect that data by applying Fully homomorphic Encryption.</p>"
    image = Image.open('flow.png')
    st.image(image)
    st.markdown(original_title, unsafe_allow_html=True)
if choice=="SignUp":
    FirstName = st.text_input("Firstname")
    LastName = st.text_input("Lastname")
    Mobile = st.text_input("Mobile")
    Email = st.text_input("Email")
    new_password = st.text_input("Password",type='password')
    Cpassword = st.text_input("Confirm Password",type='password')
    
    if st.button("Signup"):
        #Validation
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (pattern.match(Mobile)):
            if re.fullmatch(regex, Email):
                create_usertable()
                add_userdata(FirstName,LastName,Mobile,Email,make_hashes(new_password),make_hashes(Cpassword))
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
            else:
                st.warning("Not Valid Email")               
        else:
            st.warning("Not Valid Mobile Number")
        
        
if choice=="Login":
    st.subheader("Login Section")
    Email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):
        #Validation
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(Email,check_hashes(password,hashed_pswd))
            if result:
                st.success("Login Sucess")
                st.subheader("Upload .CSV File Only")
                uploaded_file = st.file_uploader("Choose a file")
                if uploaded_file is not None:
                    dataframe = pd.read_csv(uploaded_file)
                    dataframe.to_csv("adult.csv")
                    cl=len(dataframe.columns)
                    rl=len(dataframe)
                    st.success("The data Contain Columns="+str(cl))
                    st.success("The data Contain Rows="+str(rl))
                    st.dataframe(dataframe, 800, 300)
                    types=dataframe.dtypes
                    num=[]
                    cate=[]
                    k=0
                    for i in types:
                        if i=='int64':
                            num.append(dataframe.columns[k])
                            k=k+1
                        else:
                            cate.append(dataframe.columns[k])
                            k=k+1
                    gencol=st.multiselect('Select Generlization Columns',cate)
                    kencol=st.multiselect('Select K-Annonymity Numerical Columns',num)
                    kenccol=st.multiselect('Select K-Annonymity Categerical Columns',cate)
                    sencol=st.multiselect('Select Sensetive Columns',dataframe.columns.to_list())
                    from DataAno import generalization
                    if st.button("Apply"):
                        from DataAno import generalization
                        dataframe[gencol]=dataframe[gencol].apply(generalization)
                        from DataAno import kannonimity
                        dataframe[kencol]=dataframe[kencol].apply(kannonimity)
                        from sklearn.preprocessing import LabelEncoder
                        le=LabelEncoder()
                        dataframe[kenccol]=dataframe[kenccol].apply(le.fit_transform)
                        from DataAno import sensetive
                        dataframe[sencol]=dataframe[sencol].apply(sensetive)
                        
                        st.dataframe(dataframe, 800, 300)
                        dataframe.to_csv("Annonymize.csv")
                        def convert_df(df):
                            return df.to_csv().encode('utf-8')
                        csv=convert_df(dataframe)
                        import os
                        sizeO=os.path.getsize("adult.csv")
                        sizeA=os.path.getsize("Annonymize.csv")
                        st.warning("Original data is " + str(round((sizeO/1024),2))+"KB And Anonymized data is "+str(round((sizeA/1024),2))+"KB")
                        st.download_button(label="Download data as CSV",data=csv,file_name='Annonymize.csv',mime='text/csv')
            else:
                st.warning("Incorrect Email/Password")
        else:
                st.warning("Not Valid Email")               
        
        
        
  
    

    
