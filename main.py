import pyttsx3
import datetime 
import calendar
import speech_recognition as sr
import wikipedia 
import webbrowser as wb
import time
import wolframalpha
import pyautogui 
import psutil 
import pyjokes 
import requests
import json

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def say(audio):
    engine.say(audio)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print('recognizing')
        query = r.recognize_google(audio, language='en-in')
    except Exception as e:
        print(e)
        say('sorry i couldn\'t understand Say that again please...')
        return "None"
    print(query)
    return query

def time_():
    time  = datetime.datetime.now().strftime("%H:%M")
    say('current time is {} '.format(time))

def date():
    date = [datetime.datetime.now().day,
            calendar.month_name[datetime.datetime.now().month],
            datetime.datetime.now().year]
    
    def ord(n):
        return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))
    
    say('today is {0} of {1} {2}'.format(ord(date[0]),date[1],date[2]))

def start():
    say('{}, I\'M DeskMate. What can i Help You?'.format((
        "Good Morning" if datetime.datetime.now().hour < 12 else
        "Good Afternoon" if 12 < datetime.datetime.now().hour < 5 else
        "Good Evening"
    )))

def wiki(query):
    query = query.replace('wikipedia','')
    say('Searching')
    output = wikipedia.summary(query,sentences = 3)
    say('according to wikipedia{}'.format(output))
    
def youtube(query):
    
    say("What should I search?")
    term = command().lower()
    say("looking for {} on YouTube".format())
    wb.open("https://www.youtube.com/results?search_query="+term)
    time.sleep(5)

def google(query):
    say("What should I search?")
    term = command().lower()
    say('looking of {} on Google'.format(term))
    wb.open('https://www.google.com/search?q='+term)

def whereis(query):
    location =  query.replace('where is','')
    say('user askd for {}'.format(location))
    wb.open("https://www.google.com/maps/place/" + location + "")

def calculate(query):
    app_id = "RRVELJ-VLX76T84TK"
    client = wolframalpha.Client(app_id)
    indx = query.lower().split().index('calculate')
    query = query.split()[indx + 1:]
    res = client.query(' '.join(query))
    answer = next(res.results).text
    query = query.replace('calculate','')
    print("The answer is " + answer)
    say(query,'=',answer) 

def screenshot():
    img = pyautogui.screenshot()
    img.save("\screenshots")

def cpu():
    usage = str(psutil.cpu_percent())
    battery = psutil.sensors_battery()
    say('currently CPU usage is '+usage)
    say("And Battery is at {}".format(battery.percent))

def jokes():
    say(pyjokes.get_joke())

def remember():
    say("What should I remember ?")
    temp = command()
    say("You asked me to remember "+temp)
    remember = open('memory.txt','w')
    remember.write(temp)
    remember.close()

def takenote():
    say("What should i write, sir")
    note = command()
    file = open('note.txt', 'w')
    say("Sir, Should i include date and time")
    dt = command()
    if 'yes' in dt or 'sure' in dt:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        file.write(strTime)
        file.write(" :- ")
        file.write(note)
        say('done')
    else:
        file.write(note)

def weather():
    api_key = "455b1cf8f3a7e7c14353afd45e61555a"
    base_url = "http://api.openweathermap.org/data /2.5/weather?q="
    say(" City name ")
    print("City name : ")
    city_name = command()
    complete_url = base_url + "appid =" + api_key + "&q =" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))
    else:
        say(" City Not Found ") 

def news():
     
    try:
        jsonObj = urlopen('''news api link''')
        data = json.load(jsonObj)
        i = 1        
        say('here are some top news from the times of india')  
        for item in data['articles']:         
            say(str(i) + '. ' + item['title'] + '\n')
            i += 1          
    except Exception as e:
        print(str(e)) 
def gen():
    client = wolframalpha.Client('"wolfram alpha api"')
    res = client.query(query)
    try:
        print (next(res.results).text)
        say (next(res.results).text)
    except StopIteration:
        print ("No results") 

if __name__ == '__main__':
    start()
    while True:
        query = command()
        if 'date' in query:date()
        elif 'time' in query:time_()
        elif 'wikipedia' in query:wiki(query)
        elif 'YouTube' in query:youtube(query)
        elif 'search' in query: google(query)
        elif 'where is' in query: whereis(query)
        elif 'calculate' in query: calculate(query)
        elif 'what is' in query or 'who is in query': gen()
        elif 'screenshot' in query: screenshot()
        elif 'joke' in query : jokes()
        elif 'remember that' in query : remember()
        elif 'do you remember anything' in query :
            remember =open('memory.txt', 'r')
            say("You asked me to remeber "+remember.read())
        elif 'take notes' in query : takenote()
        elif "show note" in query:
            say("Showing Notes")
            file = open("note.txt", "r")
            print(file.read())
            say(file.read()) 
        elif 'weather' in query : weather()
        elif 'news' in query: news()
        elif 'exit' in query:
            say('bye! have a great day')
            break
