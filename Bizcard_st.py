import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
st.title("""
         Bizcard EasyOCR Application
         
         Business Cards Data Extraction and Display
         """)
uploaded_file = st.file_uploader("Upload your file here...", type="png")
if uploaded_file is not None:
    def main():
        import streamlit as st
        import pandas as pd
        import mysql.connector
        from PIL import Image
        import re
        import easyocr
        import imageio.v3 as iio
        from streamlit_extras.colored_header import colored_header
        #img=Image.open(r"E:/DataScience/images_bizcard/img_1.png")
        
        reader = easyocr.Reader(['en'],gpu=False)
        st.markdown("<h2 style='font-family: Calibri; font-size: 36px;'>Business Card Data Extract</h2>",unsafe_allow_html=True)
        img = iio.imread(uploaded_file)
        # consume img
        #item = cv2.cvtcolor(img, cv2.COLOR_RGB2BGR)
        st.image(img)
        result = reader.readtext(img,detail=0)
        full_lst=[]
        df=pd.DataFrame(columns=['Name',
                        'Designation',
                        'Address_Line1',
                        'Address_Line2',
                        'State',
                        'Country',
                        'Postal_Code',
                        'Company_Name',
                        'e_mail',
                        'website',
                         'Phone1',
                         'Phone2',
                         'Phone3',
                         'Phone4',
                        'image'
                        ])
        states_lst=['andaman & nicobar islands', 'andhra pradesh', 'andhrapradesh', 'arunachal pradesh','arunachalpradesh','assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra & nagar haveli & daman & diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachalpradesh','himachal pradesh' ,'jammu & kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya pradesh', 'madhyapradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamilnadu','tamil nadu', 'telangana', 'tripura', 'uttar pradesh','uttarpradesh', 'uttarakhand','westbengal', 'west bengal']
        full_lst=[]
        for val in result:
            cleaned_lst = val.replace(';','')
            cleaned_lst=cleaned_lst.replace('-','')
            cleaned_lst=cleaned_lst.replace('+','')
            full_lst.append(cleaned_lst)
        print(full_lst)
        names=[]
        numbers=[]
        alnum=[]
        email=[]
        web=[]
        code=[]
        Designation=[]
        Address_Line1=[]
        Address_Line2=[]
        phone=[]
        for val in full_lst:
            if val.isalpha():
                names.append(val)
            if val.isdigit() and len(val)>6:
                numbers.append(val)
            # if val.isdigit() and len(val)==6:
            #     code.append(val)
            if ((val.isalnum()) or (' ' in val)) and (val.isdigit() is False):
                alnum.append(val)
            if (('www' in val.casefold()) and val not in web):#or ('WWW' in val):
                web.append(val)
            if ('@' in val) :
                email.append(val)
        numbers_in_alnum=[]
        alphabets_in_alnum=[]

        
        for i in names[:]:
            if i in alnum:
                alnum.remove(i)
        #print(alnum)
        for val in alnum:
            if  (re.findall(r'[0-9]+', val) is not None) and (re.findall(r'[a-zA-Z]+', val) is not None):
                numbers_in_alnum= re.findall(r'[0-9]+', val)
                alphabets_in_alnum = re.findall(r'[a-zA-Z]+', val)
                #print(numbers_in_alnum)
                #print(alphabets_in_alnum)
                for val in numbers_in_alnum:
                    if ((len(val)==6) and (val not in code)):
                        code.append(val)
                    elif ((len(val)!=6) and (val not in code)):
                        code.append(000000)
            str_alnum=(" ".join(alnum)).replace(',',' ')
            str_alnum_lst=str_alnum.split()
            compare_alnum=[x.casefold() for x in str_alnum_lst]
            state=[]
            for val1 in compare_alnum:
                if val1 in states_lst:
                    state.append(val1)
        state=[x.upper() for x in state]
        code.pop(000000)
        for val in alnum:
            if 'www' not in val.casefold() and len(alnum)>2:
                Designation.append(alnum[0])
                Address_Line1.append(alnum[1])
                Address_Line2.append(alnum[2])
        print(numbers)

        for i in range(0,len(numbers)):
            if len(numbers[i])>6:
                phone.append(numbers[i])
        print(phone)
        if len(phone)==1:
            phone1=[phone[0]]
            phone2=['0']
            phone3=['0']
            phone4=['0']
        elif len(phone)==2:
            phone1=[phone[0]]
            phone2=[phone[1]]
            phone3=['0']
            phone4=['0']
        elif len(phone)==3:
            phone1=[phone[0]]
            phone2=[phone[1]]
            phone3=[phone[2]]
            phone4=['0']
        elif len(phone)==4:
            phone1=[phone[0]]
            phone2=[phone[1]]
            phone3=[phone[2]]
            phone4=[phone[3]]
        else:
            phone1=['0']
            phone2=['0']
            phone3=['0']
            phone4=['0']
        df['Postal_Code']=code
        df['Name']=names[0]
        names.pop(0)
        df['Company_Name']=" ".join(names[1:])
        df['e_mail']=email[0]
        df['website']=web[0]
        df['Country']='India'
        df['State']=state[0]
        df['image']=["E:/DataScience/images_bizcard/img_3.png"]
        df['Designation']=Designation[0]
        df['Address_Line1']=Address_Line1[0] 
        df['Address_Line2']=Address_Line2[0]
        df['Phone1']=phone1
        df['Phone2']=phone2
        df['Phone3']=phone3
        df['Phone4']=phone4
        df
        #st.dataframe(df)
        with st.sidebar:
            selected = option_menu("Main Menu", ["Insert","Update","Select","Delete"], 
                icons=[], menu_icon="cast", default_index=1)
        if selected=='Insert':
            connection=mysql.connector.connect(host="localhost", user="root", password="12345",database="project_3")
            mycursor=connection.cursor()
            if connection:
                query="""CREATE TABLE if not exists `bizcard` (
            `Name` varchar(400) DEFAULT NULL,
            `Designation` varchar(400) DEFAULT NULL,
            `Address_Line1` varchar(200) DEFAULT NULL,
            `Address_Line2` varchar(200) DEFAULT NULL,
            `State` varchar(400) DEFAULT NULL,
            `Country` varchar(200) DEFAULT NULL,
            `Postal_Code` varchar(10) DEFAULT NULL,
            `Phone1` varchar(55) DEFAULT '0',
            `Phone2` varchar(55) DEFAULT '0',
            `Phone3` varchar(55) DEFAULT '0',
            `Phone4` varchar(55) DEFAULT '0',
            `Company_Name` varchar(400) DEFAULT NULL,
            `e_mail` varchar(200) DEFAULT NULL,
            `website` varchar(200) DEFAULT NULL,
            `image` LONGBLOB NOT NULL
            ) """
                mycursor.execute(query)
                atrows=[]
                for index in df.index:
                    row=tuple(df.loc[index].values)
                    row=tuple(str(d) for d in row)
                    atrows.append(row)
                insert_query="""insert into bizcard values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                mycursor.executemany(insert_query,atrows)
                connection.commit()
        st.write("""List of Columns for Reference:
                                                'Name' ,
                                                'Designation' ,
                                                'Address_Line1',
                                                'Address_Line2',
                                                'State' ,
                                                'Country',
                                                'Postal_Code' ,
                                                'Phone',
                                                'Company_Name' ,
                                                'e_mail',
                                                'website',
                                                'image'""") 
        if selected=='Select':
            user_input1=st.text_input("Enter the row to select in the format- Name_as_in_db<space>Phone1_as_in_db :")
            if user_input1:
                ip_list=user_input1.split()
                name=ip_list[0]
                phone1=ip_list[1]
                if column_name is not None and value is not None and name is not None and phone1 is not None:  
                    connection=mysql.connector.connect(host="localhost", user="root", password="12345",database="project_3")
                    mycursor=connection.cursor()
                    if connection:
                        select_query="""select * from bizcard where Name='{name}' and Phone1='{phone1}'"""
                        mycursor.execute(select_query)
                        result=mycursor.fetchall()
                    for data in result:
                        st.write(data)
        if selected=='Update':
            user_input2=st.text_input("Enter the column to update in the format- update_column_name<space>value<space>Name_as_in_db<space>Phone1_as_in_db :")
            if user_input2:
                ip_list=user_input2.split()
                column_name=ip_list[0]
                value=ip_list[1]
                name=ip_list[2]
                phone1=ip_list[3]
                if column_name is not None and value is not None and name is not None and phone1 is not None: 
                    connection=mysql.connector.connect(host="localhost", user="root", password="12345",database="project_3")
                    mycursor=connection.cursor()
                    if connection:
                        update_query="""UPDATE bizcard SET {column_name}='{value}'where Name='{name}' and Phone1='{phone1}'"""
                        mycursor.execute(update_query)
                        connection.commit()
        
        if selected=='Delete': 
            user_input3=st.text_input("Enter the row to delete in the format- Name_as_in_db<space>Phone1_as_in_db :")
            if user_input3:
                ip_list=user_input3.split()
                name=ip_list[0]
                phone1=ip_list[1]
            if name is not None and phone1 is not None: 
                connection=mysql.connector.connect(host="localhost", user="root", password="12345",database="project_3")
                mycursor=connection.cursor()
                if connection:
                    delete_query="""Delete from bizcard where Name='{name}' and Phone1='{phone1}'"""
                    mycursor.execute(delete_query)
                    connection.commit()
        else:
            st.write("Image File Not Uploaded")
    main()


