from flask import Flask,jsonify
from flask_cors import CORS  # Import Flask-CORS
import mysql.connector
from flask import request,send_file,jsonify
from datetime import datetime
from flask_jwt_extended import create_access_token
import base64
import hashlib

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


from flask import Flask,jsonify,make_response,request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
CORS(app)  

class admin_model():
   
    def admin_signup(self, username, password, email, first_name, last_name, phone_number, other_admin_info):
        try:
            # Check if the user already exists
            check_query = 'SELECT * FROM admins WHERE email = %s OR phone_number = %s'
            cur.execute(check_query, (email, phone_number))
            result = cur.fetchone()
           
            if result:
                return jsonify(msg="USER ALREADY EXISTS IN DATABASE")
           
            # Insert the new admin
            insert_query = '''
                INSERT INTO admins (username, password, email, first_name, last_name, phone_number, other_admin_info)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cur.execute(insert_query, (username, password, email, first_name, last_name, phone_number, other_admin_info))
           
            # Commit the transaction
            con.commit()
           
            return jsonify(msg="Admin signed up successfully")
       
        except Exception as e:
            return jsonify(msg="Error occurred on the server side", error=str(e))


    def admin_login(self,email,password):
        try:
            print("this is insid the admin login modle ")
            query = f'SELECT * FROM hotelbooking.admins WHERE email="{email}" AND password="{password}" '
            print(email,password)

            cur.execute(query)
            user_details = cur.fetchone()
            if user_details:
                access_token = create_access_token(identity=user_details)
                return jsonify(access_token=access_token,login=True)
            else:
                return jsonify({"msg": "user not found,Please enter a valid credential"})
        except Exception as e:
            return jsonify(msg=f"{e}",err="error")
       

class room_model():

    def room_details_insert(self, hotel_id, room_type, description, price_per_night, maximum_guests, other_room_info, adults, kids, numberOfRooms, image1, image2, image3, image4, image5):
        try:
            # Prepare the SQL query with placeholders for values
            insert_query = ('''
                INSERT INTO rooms (hotel_id, room_type, description, price_per_night, maximum_guests, other_room_info, adults, kids, numberOfRooms, image1, image2, image3, image4, image5)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            ''')
            print(hotel_id,description)

            # Execute the SQL query with the provided parameters
            cur.execute(insert_query, (hotel_id, room_type, description, price_per_night, maximum_guests, other_room_info, adults, kids, numberOfRooms, image1, image2, image3, image4, image5))

            # Commit the transaction
            con.commit()

            return jsonify(msg="Room added successfully")
        except Exception as e:
            print(e)
            return jsonify(msg="Error occurred on the server side", error=str(e))

       
    def search_room(self, id):
        def image_base64(image):
            image_data = base64.b64encode(image).decode('utf-8')
            return image_data

        try:
            cur.execute(f'SELECT * FROM rooms WHERE hotel_id = {id}')
            result = cur.fetchall()

            for row in result:
                row['image1'] = image_base64(row['image1'])
                row['image2'] = image_base64(row['image2'])
                row['image3'] = image_base64(row['image3'])
                row['image4'] = image_base64(row['image4'])
                row['image5'] = image_base64(row['image5'])

            return jsonify(result)
        except Exception as e:
            return jsonify(error=str(e))
       

class profile_model():
    def init(self) :
        pass
    def get_user_data(self,data):
        query = "SELECT * FROM users WHERE email = %s"
        cur.execute(query, (data,))
        result = cur.fetchone()
        return jsonify(user_id=result['id'],name=result['name'],phone=result['phone'],email=result['email'])


class stateCity_model():
    def nameOfState (self):
        try:
            cur.execute ("SELECT id,state FROM state_city")
            result = cur.fetchall()
            return jsonify(result)
        except Exception  as e:
            return jsonify(msg="error", error =str(e))

    def nameOfDistrict (Self,state):
        try:
            cur.execute (f"SELECT city FROM state_city WHERE state = '{state}'")
            result= cur.fetchall()
            return jsonify(result)
        except Exception  as e:
            return jsonify (error=str(e))


class hotel_model():
   
    def dashboard(self):
        try:
            cur.execute("SELECT * FROM hotels")
            result=cur.fetchall()
            for row in result:
                image_path = row['image']  # Assuming 'image' is the field name for the image path
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()
                    row['image'] = base64.b64encode(image_data).decode('utf-8')
            return jsonify(result)
        except Exception as e:
            return jsonify(error=str(e))
   
    def insert_hotel_details (self,name,state,city,description,price_per_night,available_rooms,amenities,imagePath):
        try:
            query = """
                    INSERT INTO hotels
                    (name, state, city, description, image, price_per_night, available_rooms, amenities)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
           
            cur.execute(query, (name, state, city, description, imagePath, price_per_night, available_rooms, amenities))
            cur.execute('SELECT id FROM hotels ORDER BY created_at DESC LIMIT 1')
            result=cur.fetchone()
            print(result)
            return jsonify (msg="data insert successfully",hotel_id=result['id'])
        except Exception as e:
            return jsonify(error=str(e))

    def search_hotels(self,state,city):
        try:
            cur.execute (f'SELECT * FROM hotels WHERE state = "{state}" and city = "{city}" ')
            result = cur.fetchall()
           
            return result
        except Exception as e:
            return jsonify(error=str(e))
   

class user_model():

    def register(self,name,email,phone,password):
        try:
            # Check if email or phone already exists in the database

            check_query = f"SELECT id FROM users WHERE email = '{email}' OR phone = '{phone}'"
            cur.execute(check_query)
            existing_record = cur.fetchone()
           
           
            if existing_record:
                return jsonify("user is already exists.")
           
           
           

            # If not found, insert the new record
            insert_query = f"INSERT INTO users (name, email, phone, password) VALUES ('{name}', '{email}', '{phone}', '{password}')"
            print(insert_query)
            cur.execute(insert_query)
            return jsonify("Signup successful")
        except Exception as e:
            return jsonify(error=str(e))
       
       
        # login or access_token creating if user present in the database
    def login(self, email, password):
        query = F"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
       

        cur.execute(query)
     
        user_details = cur.fetchone()
     

        if user_details:
            access_token = create_access_token(identity=user_details)
            return jsonify(access_token=access_token,login=True,user_id=user_details['id'],name=user_details['name'],phone=user_details['phone'],email=user_details['email'])
        else:
            return jsonify({"msg": "user not found,Please enter a valid credential"})
           
    def edit_user_details (self,id,data):
        qry="UPDATE users SET "
        for key in data:
            qry += f"{key}='{data[key]}',"
        qry = qry[:-1]+f"WHERE id ={id}"

        cur.execute(qry)
        if cur.rowcount>0:
            return make_response({"msg":"user update Successfully "},201)
        else:
            return make_response({"msg":"Nothing update try again "},202)











#jwt
app.config ['JWT_SECRET_KEY']= 'S@31905#1101shu00pp109ss108'
jwt=JWTManager(app)


try:
    con = mysql.connector.connect(host="localhost", user="root", password="Swastika@123", database="hotelbooking")
    print("connection successful shubham sharma connected")
    con.autocommit=True
    cur = con.cursor(dictionary=True)
       
    # creating a users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTO_INCREMENT, name TEXT NULL , email VARCHAR(45) NULL , phone VARCHAR(45) NULL, password VARCHAR(100))''')

    # create an auth table
    cur.execute('''CREATE TABLE IF NOT EXISTS auth (id INTEGER PRIMARY KEY AUTO_INCREMENT ,user_id VARCHAR(45), jwt_token TEXT )''')

    # create a Hotels table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            state VARCHAR(50) NOT NULL,
            city VARCHAR(50) NOT NULL,
            description TEXT,
            image VARCHAR(100),
            price_per_night DECIMAL(10, 2) NOT NULL,
            available_rooms INT NOT NULL,
            amenities TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    con.commit()
    # create a booking table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            hotel_id INT NOT NULL,
            check_in_date DATE NOT NULL,
            check_out_date DATE NOT NULL,
            num_guests INT NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (hotel_id) REFERENCES hotels(id)
        )
    ''')
    con.commit()

    # create a reviews table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            hotel_id INT NOT NULL,
            rating INT NOT NULL,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (hotel_id) REFERENCES hotels(id)
        )
    ''')
    con.commit()


        # Payment Information Table Entity:

    cur.execute('''
        CREATE TABLE IF NOT EXISTS payment_information (
            payment_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            cardholder_name VARCHAR(255) NOT NULL,
            card_number VARCHAR(255) NOT NULL,
            expiration_date DATE NOT NULL,
            billing_address TEXT,
            other_payment_info TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    con.commit()

    #Admins Table Entity:
    cur.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            phone_number VARCHAR(20),
            other_admin_info TEXT,
            UNIQUE (username),
            UNIQUE (email)
    )

    ''')
    con.commit()

    #Promotions Table Entity:
    cur.execute('''
        CREATE TABLE IF NOT EXISTS promotions (
            promo_id INT PRIMARY KEY AUTO_INCREMENT,
            promo_code VARCHAR(50) NOT NULL,
            discount_amount DECIMAL(10, 2) NOT NULL,
            validity_period DATE NOT NULL,
            hotel_id INT NOT NULL,
            other_promotion_info TEXT,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id)
    )

    ''')
    con.commit()


    # Location table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            location_id INT PRIMARY KEY AUTO_INCREMENT,
            hotel_id INT NOT NULL,
            latitude DECIMAL(10, 6) NOT NULL,
            longitude DECIMAL(10, 6) NOT NULL,
            city VARCHAR(100) NOT NULL,
            state VARCHAR(100),
            country VARCHAR(100) NOT NULL,
            zip_code VARCHAR(20),
            other_location_info TEXT,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id)
    )

    ''')
    con.commit()


    #Rooms Table Entity:

    cur.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    hotel_id INT NOT NULL,
    room_type VARCHAR(100) NOT NULL,
    description TEXT,
    image1 MEDIUMBLOB,
    image2 MEDIUMBLOB,
    image3 MEDIUMBLOB,
    image4 MEDIUMBLOB,
    image5 MEDIUMBLOB,
    price_per_night DECIMAL(10, 2) NOT NULL,
    adults INT,
    kids INT,
    maximum_guests INT NOT NULL,
    other_room_info TEXT,
    FOREIGN KEY (hotel_id) REFERENCES hotels(id),
    numberOfRooms INT NOT NULL
    )
    ''')
    con.commit()



    # #Booking History Table Entity:

    # cur.execute ('''
    #     CREATE TABLE IF NOT EXISTS booking_history (
    #         history_id INT PRIMARY KEY AUTO_INCREMENT,
    #         user_id INT NOT NULL,
    #         hotel_id INT NOT NULL,
    #         room_id INT NOT NULL,
    #         check_in_date DATE NOT NULL,
    #         check_out_date DATE NOT NULL,
    #         total_price DECIMAL(10, 2) NOT NULL,
    #         status ENUM('completed', 'canceled') NOT NULL,
    #         booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #         other_booking_history_info TEXT,
    #         FOREIGN KEY (user_id) REFERENCES users(id),
    #         FOREIGN KEY (hotel_id) REFERENCES hotels(id),
    #         FOREIGN KEY (room_id) REFERENCES rooms(id)
    #     )

    # ''')
    # con.commit()


    cur.execute('''CREATE TABLE IF NOT EXISTS state_city (id INT AUTO_INCREMENT PRIMARY KEY,state VARCHAR(100) NOT NULL,city TEXT NOT NULL,numberOfCity INT NOT NULL,other_info TEXT)''')

    con.commit()

    # cur.execute('''
    #     INSERT INTO state_city (state, city, numberOfCity, other_info)
    #     VALUES
    #     ('Andhra Pradesh', 'Anantapur,Chittoor,East Godavari,Guntur,Krishna,Kurnool,Nellore,Prakasam,Srikakulam,Visakhapatnam,Vizianagaram,West Godavari,YSR Kadapa', 13, NULL),
    #     ('Arunachal Pradesh', 'Tawang,West Kameng,East Kameng,Papum Pare,Kurung Kumey,Kra Daadi,Lower Subansiri,Upper Subansiri,West Siang,East Siang,Siang,Upper Siang,Lower Siang,Lower Dibang Valley,Dibang Valley,Anjaw,Lohit,Namsai,Changlang,Tirap,Longding', 21, NULL),
    #     ('Assam', 'Baksa,Barpeta,Biswanath,Bongaigaon,Cachar,Charaideo,Chirang,Darrang,Dhemaji,Dhubri,Dibrugarh,Goalpara,Golaghat,Hailakandi,Hojai,Jorhat,Kamrup Metropolitan,Kamrup,Karbi Anglong,Karimganj,Kokrajhar,Lakhimpur,Majuli,Morigaon,Nagaon,Nalbari,Dima Hasao,Sivasagar,Sonitpur,South Salmara-Mankachar,Tinsukia,Udalguri,West Karbi Anglong', 33, NULL),
    #     ('Bihar', 'Araria,Arwal,Aurangabad,Banka,Begusarai,Bhagalpur,Bhojpur,Buxar,Darbhanga,East Champaran (Motihari),Gaya,Gopalganj,Jamui,Jehanabad,Kaimur (Bhabua),Katihar,Khagaria,Kishanganj,Lakhisarai,Madhepura,Madhubani,Munger (Monghyr),Muzaffarpur,Nalanda,Nawada,Patna,Purnia (Purnea),Rohtas,Saharsa,Samastipur,Saran,Sheikhpura,Sheohar,Sitamarhi,Siwan,Supaul,Vaishali,West Champaran', 38, NULL),
    #     ('Chandigarh (UT)', 'Chandigarh', 1, NULL),
    #     ('Chhattisgarh', 'Balod,Baloda Bazar,Balrampur,Bastar,Bemetara,Bijapur,Bilaspur,Dantewada (South Bastar),Dhamtari,Durg,Gariyaband,Janjgir-Champa,Jashpur,Kabirdham (Kawardha),Kanker (North Bastar),Kondagaon,Korba,Korea (Koriya),Mahasamund,Mungeli,Narayanpur,Raigarh,Raipur,Rajnandgaon,Sukma,Surajpur,Surguja', 27, NULL),
    #     ('Dadra and Nagar Haveli (UT)', 'Dadra & Nagar Haveli', 1, NULL),
    #     ('Daman and Diu (UT)', 'Daman,Diu', 2, NULL),
    #     ('Delhi (NCT)', 'Central Delhi,East Delhi,New Delhi,North Delhi,North East Delhi,North West Delhi,Shahdara,South Delhi,South East Delhi,South West Delhi,West Delhi', 11, NULL),
    #     ('Goa', 'North Goa,South Goa', 2, NULL),

    #     ('Gujarat', 'Ahmedabad,Amreli,Anand,Aravalli,Banaskantha (Palanpur),Bharuch,Bhavnagar,Botad,Chhota Udepur,Dahod,Dangs (Ahwa),Devbhoomi Dwarka,Gandhinagar,Gir Somnath,Jamnagar,Junagadh,Kachchh,Kheda (Nadiad),Mahisagar,Mehsana,Morbi,Narmada (Rajpipla),Navsari,Panchmahal (Godhra),Patan,Porbandar,Rajkot,Sabarkantha (Himmatnagar),Surat,Surendranagar,Tapi (Vyara),Vadodara,Valsad', 33, NULL),
    #     ('Haryana', 'Ambala,Bhiwani,Charkhi Dadri,Faridabad,Fatehabad,Gurgaon,Hisar,Jhajjar,Jind,Kaithal,Karnal,Kurukshetra,Mahendragarh,Mewat,Palwal,Panchkula,Panipat,Rewari,Rohtak,Sirsa,Sonipat,Yamunanagar', 22, NULL),
    #     ('Himachal Pradesh', 'Bilaspur,Chamba,Hamirpur,Kangra,Kinnaur,Kullu,Lahaul & Spiti,Mandi,Shimla,Sirmaur (Sirmour),Solan,Una', 12, NULL),
    #     ('Jammu and Kashmir', 'Anantnag,Bandipore,Baramulla,Budgam,Doda,Ganderbal,Jammu,Kargil,Kathua,Kishtwar,Kulgam,Kupwara,Leh,Poonch,Pulwama,Rajouri,Ramban,Reasi,Samba,Shopian,Srinagar,Udhampur', 22, NULL),
    #     ('Jharkhand', 'Bokaro,Chatra,Deoghar,Dhanbad,Dumka,East Singhbhum,Garhwa,Giridih,Godda,Gumla,Hazaribag,Jamtara,Khunti,Koderma,Latehar,Lohardaga,Pakur,Palamu,Ramgarh,Ranchi,Sahibganj,Seraikela-Kharsawan,Simdega,West Singhbhum', 24, NULL),
    #     ('Karnataka', 'Bagalkot,Ballari (Bellary),Belagavi (Belgaum),Bengaluru (Bangalore) Rural,Bengaluru (Bangalore) Urban,Bidar,Chamarajanagar,Chikballapur,Chikkamagaluru (Chikmagalur),Chitradurga,Dakshina Kannada,Davangere,Dharwad,Gadag,Hassan,Haveri,Kalaburagi (Gulbarga),Kodagu,Kolar,Koppal,Mandya,Mysuru (Mysore),Raichur,Ramanagara,Shivamogga (Shimoga),Tumakuru (Tumkur),Udupi,Uttara Kannada (Karwar),Vijayapura (Bijapur),Yadgir', 31, NULL),
    #     ('Kerala', 'Alappuzha,Ernakulam,Idukki,Kannur,Kasaragod,Kollam,Kottayam,Kozhikode,Malappuram,Palakkad,Pathanamthitta,Thiruvananthapuram,Thrissur,Wayanad', 14, NULL),
    #     ('Lakshadweep (UT)', 'Agatti,Amini,Androth,Bithra,Chethlath,Kavaratti,Kadmath,Kalpeni,Kilthan,Minicoy', 10, NULL),
    #     ('Madhya Pradesh', 'Agar Malwa,Alirajpur,Anuppur,Ashoknagar,Balaghat,Barwani,Betul,Bhind,Bhopal,Burhanpur,Chhatarpur,Chhindwara,Damoh,Datia,Dewas,Dhar,Dindori,Guna,Gwalior,Harda,Hoshangabad,Indore,Jabalpur,Jhabua,Katni,Khandwa,Khargone,Mandla,Mandsaur,Morena,Narsinghpur,Neemuch,Panna,Raisen,Rajgarh,Ratlam,Rewa,Sagar,Satna,Sehore,Seoni,Shahdol,Shajapur,Sheopur,Shivpuri,Sidhi,Singrauli,Tikamgarh,Ujjain,Umaria,Vidisha', 52, NULL),
    #     ('Maharashtra', 'Ahmednagar,Akola,Amravati,Aurangabad,Beed,Bhandara,Buldhana,Chandrapur,Dhule,Gadchiroli,Gondia,Hingoli,Jalgaon,Jalna,Kolhapur,Latur,Mumbai City,Mumbai Suburban,Nagpur,Nanded,Nandurbar,Nashik,Osmanabad,Palghar,Parbhani,Pune,Raigad,Ratnagiri,Sangli,Satara,Sindhudurg,Solapur,Thane,Wardha,Washim,Yavatmal', 36, NULL),



    #     ('Manipur', 'Bishnupur,Chandel,Churachandpur,Imphal East,Imphal West,Jiribam,Kakching,Kamjong,Kangpokpi,Noney,Pherzawl,Senapati,Tamenglong,Tengnoupal,Thoubal,Ukhrul', 16, NULL),
    #     ('Meghalaya', 'East Garo Hills,East Jaintia Hills,East Khasi Hills,North Garo Hills,Ri Bhoi,South Garo Hills,South West Garo Hills, South West Khasi Hills,West Garo Hills,West Jaintia Hills,West Khasi Hills', 11, NULL),
    #     ('Mizoram', 'Aizawl,Champhai,Kolasib,Lawngtlai,Lunglei,Mamit,Saiha,Serchhip', 8, NULL),
    #     ('Nagaland', 'Dimapur,Kiphire,Kohima,Longleng,Mokokchung,Mon,Peren,Phek,Tuensang,Wokha,Zunheboto', 11, NULL),
    #     ('Odisha', 'Angul,Balangir,Balasore,Bargarh,Bhadrak,Boudh,Cuttack,Deogarh,Dhenkanal,Gajapati,Ganjam,Jagatsinghapur,Jajpur,Jharsuguda,Kalahandi,Kandhamal,Kendrapara,Kendujhar (Keonjhar),Khordha,Koraput,Malkangiri,Mayurbhanj,Nabarangpur,Nayagarh,Nuapada,Puri,Rayagada,Sambalpur,Sonepur,Sundargarh', 30, NULL),
    #     ('Puducherry (UT)', 'Karaikal,Mahe,Puducherry,Yanam', 4, NULL),
    #     ('Punjab', 'Amritsar,Barnala,Bathinda,Faridkot,Fatehgarh Sahib,Fazilka,Ferozepur,Gurdaspur,Hoshiarpur,Jalandhar,Kapurthala,Ludhiana,Mansa,Moga,Muktsar,Nawanshahr (Shahid Bhagat Singh Nagar),Pathankot,Patiala,Rupnagar (Ropar),Sahibzada Ajit Singh Nagar (Mohali),Sangrur,Tarn Taran', 22, NULL),
    #     ('Rajasthan', 'Ajmer,Alwar,Banswara,Baran,Barmer,Bharatpur,Bhilwara,Bikaner,Bundi,Chittorgarh,Churu,Dausa,Dholpur,Dungarpur,Hanumangarh,Jaipur,Jaisalmer,Jalore,Jhalawar,Jhunjhunu,Jodhpur,Karauli,Kota,Nagaur,Pali,Pratapgarh,Rajsamand,Sawai Madhopur,Sikar,Sirohi,Sri Ganganagar,Tonk,Udaipur', 33, NULL),
    #     ('Sikkim', 'East Sikkim,North Sikkim,South Sikkim,West Sikkim', 4, NULL),
    #     ('Tamil Nadu', 'Ariyalur,Chengalpattu,Chennai,Coimbatore,Cuddalore,Dharmapuri,Dindigul,Erode,Kallakurichi,Kancheepuram,Kanyakumari,Karur,Krishnagiri,Madurai,Mayiladuthurai,Nagapattinam,Namakkal,Nilgiris,Perambalur,Pudukkottai,Ramanathapuram,Ranipet,Salem,Sivaganga,Tenkasi,Thanjavur,Theni,Thoothukudi,Tiruchirappalli,Tirunelveli,Tirupathur,Tiruppur,Tiruvallur,Tiruvannamalai,Vellore,Viluppuram,Virudhunagar', 38, NULL),
    #     ('Telangana', 'Adilabad,Bhadradri Kothagudem,Hanamkonda,Hyderabad,Jagtial,Jangaon, Jayashankar Bhupalapally,Jogulamba Gadwal,Kamareddy,Karimnagar,Khammam,Komaram Bheem Asifabad,Mahabubabad,Mahabubnagar,Mancherial,Medak,Nagarkurnool,Nalgonda,Nirmal,Nizamabad,Peddapalli,Rajanna Sircilla,Rangareddy,Sangareddy,Siddipet,Suryapet,Wanaparthy,Warangal (Rural),Warangal (Urban),Yadadri Bhuvanagiri', 33, NULL),
    #     ('Tripura', 'Dhalai,Gomati,Khowai,North Tripura,Sepahijala,South Tripura,Unakoti,West Tripura', 8, NULL),
    #     ('Uttar Pradesh', 'Agra,Aligarh,Ambedkar Nagar,Amethi (Chatrapati Sahuji Mahraj Nagar),Amroha (J.P. Nagar),Auraiya,Ayodhya (Faizabad),Azamgarh,Baghpat,Bahraich,Balarampur,Ballia,Banda,Barabanki,Bareilly,Basti,Bhadohi,Bijnor,Budaun,Bulandshahr,Chandauli,Chitrakoot,Deoria,Etah,Etawah,Farrukhabad,Fatehpur,Firozabad,Gautam Buddha Nagar,Ghaziabad,Ghazipur,Gonda,Gorakhpur,Hapur,Hardoi,Hathras,Jalaun,Jaunpur,Jhansi,Kannauj,Kanpur Dehat,Kanpur Nagar,Kasganj,Kaushambi,Kheri (Lakhimpur Kheri),Kushinagar,Lalitpur,Lucknow,Maharajganj,Mahoba,Mainpuri,Mathura,Mau,Meerut,Mirzapur,Moradabad,Muzaffarnagar,Pilibhit,Pratapgarh,Prayagraj (Allahabad),RaeBareli,Rampur,Saharanpur,Sambhal,Shahjahanpur,Shamli,Shravasti,Siddharthnagar,Sitapur,Sonbhadra,Sultanpur,Unnao,Varanasi', 75, NULL),
    #     ('Uttarakhand', 'Almora,Bageshwar,Chamoli,Champawat,Dehradun,Haridwar,Nainital,Pauri Garhwal,Pithoragarh,Rudraprayag,Tehri Garhwal,Udham Singh Nagar,Uttarkashi', 13, NULL),
    #     ('West Bengal', 'Alipurduar,Bankura,Birbhum,Cooch Behar,Dakshin Dinajpur (South Dinajpur),Darjeeling,Hooghly,Howrah,Jalpaiguri,Jhargram,Kalimpong,Kolkata,Malda,Murshidabad,Nadia,North 24 Parganas,Paschim Medinipur (West Medinipur),Purba Medinipur (East Medinipur),Purulia,South 24 Parganas,Uttar Dinajpur (North Dinajpur)', 23, NULL)
    #             ''')

    # con.commit()
       
except:
    print("some error in database connection")






@app.route("/")
def home():
    data = {
        "message": "This is a Flask server code running",
        "status": "success"
    }
    return jsonify(data)


obj=user_model()

@app.route("/signup",methods=["POST"])
def post_controller():
    try:
        val=request.json
        name=val['name']
        email=val['email']
        phone=val['phone']
       
        sha256 = hashlib.sha256()
        sha256.update(val['password'].encode('utf-8'))
        hashed_password = sha256.hexdigest()

       
        return obj.register(name,email,phone,hashed_password)
    except Exception as e:
        return jsonify(error=str(e))
@app.route("/login",methods=['POST'])
def login():
    try:
        val=request.json
       
        email=val['email']
        password = val['password']

        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        hashed_password = sha256.hexdigest()

       
   
        return obj.login(email,hashed_password)
    except Exception as e:
        return jsonify(error=str(e))



@app.route("/edituser/<id>",methods=["PATCH"])
def edit_user_Details(id):
    val =request.get_json()
    return obj.edit_user_details(id,val)

##########################################

profile_obj = profile_model()

@app.route("/profile",methods=["POST"])
def get_profile_data():
    email=request.json.get('email',None)
    print (email)
    return profile_obj.get_user_data(email)

hotel_obj = hotel_model()

@app.route("/dashboard",methods=["GET"])
def user_deshboard():
    return hotel_obj.dashboard()



@app.route ("/insert/hotel/details",methods=["POST"])
def insert_hotel_deails():
    try:
        name = request.form.get('name')
        state = request.form.get('state')
        city = request.form.get('city')
        description = request.form.get('description')
        price_per_night = float(request.form.get('price_per_night'))
        available_rooms = int(request.form.get('available_rooms'))
        amenities = request.form.get('amenities')
        image = request.files.get('image')

        uniqueFileName=str(datetime.now().timestamp()).replace(".","")
        fileNameSplit =image.filename.split(".")
        imageExt=fileNameSplit[len(fileNameSplit)-1]
        imagePath=(f"hotelPicture/{uniqueFileName}.{imageExt}")
        image.save(f"hotelPicture/{uniqueFileName}.{imageExt}")

        return hotel_obj.insert_hotel_details(name,state,city,description,price_per_night,available_rooms,amenities,imagePath)
    except Exception as e:
        return jsonify(error=str(e))

   

@app.route ("/search/<state>/<city>",methods=["GET"])
def search_hotels(state,city):
   
    return hotel_obj.search_hotels(state,city)    





admin_obj = admin_model()

@app.route("/admin/signup", methods=["POST"])
def admin_signup():
    data = request.json  # Get the JSON data from the request

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    other_admin_info = data.get("other_admin_info")

    # Print the data for debugging
    print(username, email, first_name, last_name, phone_number, other_admin_info, password)

    # Call the admin_signup method with the extracted data
    return admin_obj.admin_signup(username, password, email, first_name, last_name, phone_number, other_admin_info)

@app.route("/admin/login",methods=["POST"])
def admin_login():
    email=request.json.get('email',None)
    password = request.json.get('password',None)
    print(email,password)

    return admin_obj.admin_login(email,password)



state_obj = stateCity_model()


@app.route("/name/state",methods=["GET"])
def nameOfState ():
    try:
        return state_obj.nameOfState()
    except Exception as e :
        return  jsonify(error=str(e))

@app.route("/nameOf/<state>/district",methods=["GET"])
def nameOfDistrict (state):
    try:
        print("this is a city controller ")
        return state_obj.nameOfDistrict(state)
    except Exception as e:
        return jsonify(error=str(e))
room_obj = room_model()

def image_byte_converter(image):
    image_data=image.read()
    return image_data




@app.route("/room/details/insert",methods=["POST"])
def room_details_insert ():
    try:
        hotel_id=request.form.get("hotel_id")
        room_type=request.form.get("room_type")
        description = request.form.get("description")
        price_per_night=request.form.get("price_per_night")
        maximum_guests=request.form.get("maximum_guests")
        other_room_info=request.form.get("other_room_info")
        image1 = image_byte_converter(request.files.get("image1"))
        image2 = image_byte_converter(request.files.get("image2"))
        image3 = image_byte_converter(request.files.get("image3"))
        image4 = image_byte_converter(request.files.get("image4"))
        image5 = image_byte_converter(request.files.get("image5"))
        adults=request.form.get("adults")
        kids=request.form.get("kids")
        numberOfRooms=request.form.get("numberOfRooms")

       
        return room_obj.room_details_insert(hotel_id,room_type,description,price_per_night,maximum_guests,str(other_room_info),adults,kids,numberOfRooms,image1,image2,image3,image4,image5)
    except Exception as e :
        return jsonify(error="error in server side ",msg=f"{e}")
   
@app.route("/search/<hotel_id>/rooms",methods=["GET"])
def search_room(hotel_id):
    return room_obj.search_room(hotel_id)############################################




if __name__ == "__main__":
    app.run(debug=True)

