from flask import Flask,session,render_template,request,redirect,url_for,flash
from user import user_operation
from encryption import Encryption
import time
from email import encoders
from gtts import gTTS
import os
from playsound import playsound
import speech_recognition as sr
import pygame
import sounddevice as sd
import soundfile as sf
import numpy



file = "good"
i="0"


app=Flask(__name__)
app.secret_key = 'nahsgtwjmbhkacsbkjvjvsv' 

def texttospeech(text, filename):
    filename = filename + '.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except:
            print('Trying again')
    # Read the audio file
    data, samplerate = sf.read(filename)
    # Play the sound file
    sd.play(data, samplerate)
    # Wait until playback is finished
    sd.wait()
    #playsound(filename)
    os.remove(filename)
    return


def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        # Read the audio file
        data, samplerate = sf.read('speak.mp3')
        # Play the sound file
        sd.play(data, samplerate)
        # Wait until playback is finished
        sd.wait()
        #playsound('speak.mp3')
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
    except:
        response = 'N'
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['dotkom','dot','underscore','dollar','hash','star','plus','minus','space','dash','attherate','atedrate','at']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'dotkom':
                    temp=temp.replace('dotkom','.com')
                elif character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
                elif character == 'attherate':
                    temp=temp.replace('attherate','@')
                elif character == 'atedrate':
                    temp=temp.replace('atedrate','@')
                elif character == 'at':
                    temp=temp.replace('at','@')
   
    return temp



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choice')
def choice():
    global i, addr, passwrd
    text1 = "Welcome to our Voice Based Email. Choose either you want to login or register give your choice "
    texttospeech(text1, file + i)
    i = i + str(1)   

    texttospeech("Enter your choice", file + i)
    i = i + str(1)
    choice = speechtotext(10)

    if choice == 'login':
        return redirect(url_for('user_email'))
    elif(choice =='register'):
        return redirect(url_for('user_name'))
    else:
        msg = "You have choose an incorrect option. please choose a valid option." 
        texttospeech(msg, file + i)
        i = i + str(1)
        return redirect(url_for('choice'))


@app.route('/user_name')
def user_name():
    global i, addr, passwrd
    flag = True
    while flag:      
        texttospeech("Enter your name", file + i)
        i = i + str(1)
        name = speechtotext(10)

        if name != 'N':
            texttospeech("You meant " + name + ". please 'confirm' or say 'no' to enter again", file + i)
            i = i + str(1)
            say = speechtotext(3)
            if say.lower() == 'confirm' or say.lower() == 'yes':
                
                flag = False
                return render_template('user_name.html',name=name)
            
        else:
            texttospeech("Could not understand what you meant:", file + i)
            i = i + str(1)
            return redirect(url_for('user_name'))

@app.route('/user_create_email')
def user_create_email():
    global i, addr, passwrd
    flag = True
    while flag:
        texttospeech("create your Email id", file + i)
        i = i + str(1)
        name=request.args.get('name')
        email = speechtotext(10)
        if email != 'N':
            texttospeech("You meant " + email + ". please 'confirm' or say 'no' to enter again", file + i)
            i = i + str(1)
            say = speechtotext(3)
            if say.lower() == 'confirm' or say.lower() == 'yes':
                email = email.strip().replace(' ', '').lower()
                email = convert_special_char(email)
                flag = False
                return render_template('user_create_email.html',email=email,name=name)
            
        else:
            texttospeech("Could not understand what you meant:", file + i)
            i = i + str(1)
            return redirect(url_for('user_create_email',name=name))



@app.route('/user_create_password',methods=['GET','POST'])
def user_create_password():
    global i, addr, passwrd
    flag = True
    while flag:
        texttospeech("create your email password", file + i)
        i = i + str(1)
        email=request.args.get('email')
        name=request.args.get('name')
        password = speechtotext(10)

        if password != 'N':
            texttospeech("You meant " + password + ". please 'confirm' or say 'no' to enter again", file + i)
            i = i + str(1)
            say = speechtotext(3)
            if say.lower() == 'confirm' or say.lower() == 'yes':
                password = password.strip().replace(' ', '').lower()
                password = convert_special_char(password)
                flag = False
                return render_template('user_create_password.html',password=password,email=email,name=name)
        else:
            texttospeech("Could not understand what you meant:", file + i)
            i = i + str(1)
            return redirect(url_for('user_create_password',email=email,name=name))
				



@app.route('/user_signup',methods=['GET','POST'])
def user_signup():
    global i, addr, passwrd
    if(request.method=='POST'):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        e = Encryption()
        password = e.convert(password)
        ob = user_operation()
        ob.user_signup(name,email,password)
        msg = "Successfully Registered. Thank you. You can login now."
        texttospeech(msg, file + i)
        i = i + str(1)
        return redirect(url_for('user_email'))
		
		


@app.route('/user_email')
def user_email():
    global i, addr, passwrd
    flag = True
    while flag:
        texttospeech("Enter your Email", file + i)
        i = i + str(1)
        addr = speechtotext(10)
        if addr != 'N':
            addr = addr.strip().replace(' ', '').lower()
            addr = convert_special_char(addr)
            flag = False
            return render_template('user_email.html',email=addr)
                    
        else:
            texttospeech("Could not understand what you meant:", file + i)
            i = i + str(1)


@app.route('/confirm_user_email')
def confirm_user_email():
    global i
    email = request.args.get('email')
    texttospeech("You meant " + email + ". please 'confirm' or say 'no' to enter again", file + i)
    i = i + str(1)
    say = speechtotext(3)
    if say.lower() == 'confirm' or say.lower() == 'yes':
        return redirect(url_for('user_password'))
    else:
        return redirect(url_for('user_email'))

    
	


@app.route('/user_password',methods=['GET','POST'])
def user_password():
    global i, addr, passwrd
    flag = True
    while flag:
        texttospeech("Enter your password", file + i)
        i = i + str(1)
        passwrd = speechtotext(10)

        if passwrd != 'N':
            texttospeech("You meant " + passwrd + ". please 'confirm' or say 'no' to enter again", file + i)
            i = i + str(1)
            say = speechtotext(3)
            if say.lower() == 'confirm' or say.lower() == 'yes':
                passwrd = passwrd.strip().replace(' ', '').lower()
                passwrd = convert_special_char(passwrd)
                flag = False
                return render_template('user_password.html',password=passwrd,email=addr)

        else:
            texttospeech("Could not understand what you meant:", file + i)
            i = i + str(1)


		
@app.route('/user_login_verify',methods=['GET','POST'])
def user_login_verify():
	global i, addr, passwrd
	if(request.method=='POST'):
		email = request.form['email']
		password = request.form['password']
		e = Encryption()
		password = e.convert(password)
		ob = user_operation()
		rc = ob.user_login(email,password)
		if(rc==0):
			msg = "Invalid email Or password please try again"
			texttospeech(msg, file + i)
			i = i + str(1)
			return redirect(url_for('user_email'))
		else:
			msg = "Welcome "+ session['name']
			texttospeech(msg, file + i)
			i = i + str(1)
			return redirect(url_for('user_dashboard'))
			



@app.route('/user_logout')
def user_logout():
	global i, addr, passwrd
	if('email' in session):
		session.clear()
		msg = "Logged out successfully"
		texttospeech(msg, file + i)
		i = i + str(1)
		return redirect(url_for('user_login'))
	else:
		return redirect(url_for('index'))
	
@app.route('/user_dashboard')
def user_dashboard():
    global i, addr, passwrd
    flag = True
    while flag:
        if 'email' in session:
            msg = "Welcome " + session['name'] + " to V Mail"
            texttospeech(msg, file + i)
            i = i + str(1)
            ob = user_operation()
            record = ob.user_inbox_mails()
            return render_template('user_dashboard.html', record=record)
        else:
            msg = "You are not authorized! Please login first"
            texttospeech(msg, file + i)
            i = i + str(1)
            return redirect(url_for('user_email'))



@app.route('/user_command')
def user_command():
    global i, addr, passwrd
    flag = True
    while flag:
        try:        
            if('email' in session):
                msg = "Please say OK MAIL to get your virtual assistant"
                texttospeech(msg, file + i)
                i = i + str(1)

                say = speechtotext(8)
                if say.lower() == "ok mail":
                    flag = False
                    return redirect(url_for('user_assistant'))
            else:
                texttospeech("invalid command", file + i)
                i = i + str(1)
        except Exception as e:
            msg = "Your Voice is not audible."
            texttospeech(msg, file + i)
            i = i + str(1)
            return redirect(url_for('user_command'))





@app.route('/user_assistant')
def user_assistant():
    global i, addr, passwrd
    flag = True
    while flag:
        if('email' in session):
            msg = "Please tell a command to proceed like compose mail, read mail or logout"
            texttospeech(msg, file + i)
            i = i + str(1)

            command = speechtotext(5)
            
            if(command == "compose mail"):
                return redirect(url_for('user_compose_to'))
            elif(command == "read mail"):
                return redirect(url_for('user_read_mail'))
            elif(command == "logout" ):
                return redirect(url_for('user_logout'))
            
        else:
            msg = "invalid command"
            texttospeech(msg, file + i)
            i = i + str(1)
            return redirect(url_for('user_email'))








@app.route('/user_compose_to')
def user_compose_to():
    global i, addr, passwrd, s, item, subject, body
    text1 = "You have reached the page where you can compose and send an email. "
    texttospeech(text1, file + str(i))
    i = str(int(i) + 1)
    flag = True
    flag1 = True
    fromaddr = addr
    toaddr = list()
    while flag1:
        while flag:
            texttospeech("Enter receiver's email address:", file + str(i))
            i = str(int(i) + 1)
            to = speechtotext(15)
            if to != 'N':
                texttospeech("You meant " + to + ". please 'confirm' or say 'no' to enter again", file + str(i))
                i = str(int(i) + 1)
                say = speechtotext(5)
                if say.lower() == 'confirm' or say.lower() == 'yes':
                    to = to.strip().replace(' ', '').lower()
                    to = convert_special_char(to)
                    toaddr.append(to)
                    flag = False
                    return render_template('user_compose_to.html', receiver=to)
            else:
                texttospeech("Could not understand what you meant", file + str(i))
                i = str(int(i) + 1)
                return redirect(url_for('user_compose_to'))

            

        texttospeech("Do you want to enter more recipients? Say 'yes' or 'no'.", file + str(i))
        i = str(int(i) + 1)
        say1 = speechtotext(3)
        if say1.lower() == 'no':
            flag1 = False
        flag = True

    newtoaddr = list()
    for item in toaddr:
        item = item.strip()
        item = item.replace(' ', '')
        item = item.lower()
        item = convert_special_char(item)
        newtoaddr.append(item)
        print(item)



    
@app.route('/user_compose_subject')
def user_compose_subject():
    global i, addr, passwrd, s, item, subject, body
    flag = True
    while (flag):
        texttospeech("enter subject", file + i)
        i = i + str(1)
        rec = request.args.get('rec')
        subject = speechtotext(10)
        if subject != 'N':
            texttospeech("You meant " + subject + ". please 'confirm' or say 'no' to enter again", file + i)
            i = i + str(1)
            say = speechtotext(5)
            if say.lower() == 'confirm' or say.lower() == 'yes':
                flag = False
                return render_template('user_compose_subject.html',receiver=rec,subject=subject)
            
        else:
            texttospeech("could not understand what you meant", file + i)
            i = i + str(1)
            return redirect(url_for('user_compose_to',receiver = rec))


@app.route('/user_compose_message')
def user_compose_message():
    global i, addr, passwrd, s, item, subject, body
    flag = True
    while flag:
        texttospeech("enter body of the mail", file + i)
        i = i + str(1)
        rec = request.args.get('rec')
        sub = request.args.get('sub')
        body = speechtotext(20)
        if body != 'N':
            texttospeech("You meant " + body + ". please 'confirm' or say 'no' to enter again", file + i)
            i = i + str(1)
            say = speechtotext(5)
            if say.lower() == 'confirm' or say.lower() == 'yes':
                flag = False
                return render_template('user_compose_message.html',receiver=rec,subject=sub,message=body)
        else:
            texttospeech("could not understand what you meant", file + i)
            i = i + str(1)
            return redirect(url_for('user_compose_to',receiver = rec,subject = sub))	
            





@app.route('/user_compose_mail', methods=['GET', 'POST'])
def user_compose_mail():
    global i, addr, passwrd
    if 'email' in session:
        msg = "Are you sure you want to 'send' this mail or want to 'cancel'?"
        texttospeech(msg, file + i)
        i = i + str(1)

        if request.method == 'POST':
            rec = request.form['receiver']
            sub = request.form['subject']
            message = request.form['message']
        else:
            rec = request.args.get('receiver')
            sub = request.args.get('subject')
            message = request.args.get('message')
        
        try:
            data = speechtotext(5)
            if data:
                if data.lower() == 'yes' or  data.lower() == 'send':
                    ob = user_operation()
                    ob.user_send_mail(rec, sub, message)
                    msg = "Mail sent successfully"
                    texttospeech(msg, file + i)
                    i = i + str(1)
                    return redirect(url_for('user_dashboard'))
                elif data.lower() == 'cancel':
                    msg = "Your message is not sent"
                    texttospeech(msg, file + i)
                    i = i + str(1)
                    return redirect(url_for('user_dashboard'))
                else:
                    msg = "Invalid command"
                    texttospeech(msg, file + str(i))
                    i += 1
                    return redirect(url_for('user_compose_mail', receiver=rec, subject=sub, message=message))
        except Exception as e:
            msg = "Your voice is not audible."
            texttospeech(msg, file + str(i))
            i = i + str(1)
            return redirect(url_for('user_compose_mail', receiver=rec, subject=sub, message=message))
    else:
        msg = "You are not logged in yet"
        texttospeech(msg, file + i)
        i = i + str(1)
        return redirect(url_for('user_email'))






if __name__==("__main__"):
	app.run(debug=True)
