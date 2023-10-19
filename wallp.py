from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from split_image import split_image
import threading
import subprocess
import requests
import random
import shutil
import time
import json
import os


pwd =  os.getcwd()
stop_event = threading.Event()

timer_dict = {'10 Sec': 10, 
              '15 Min': 900,
              '30 Min': 1800,
              '1 Hour': 3600,
              '3 Hour': 10800,
              '6 Hour': 21600, 
              'Off': 'off'}


def get_command_str(filename, ext):
    return """
    dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
    var Desktops = desktops();
    var side = 0;
    for (i=0;i<Desktops.length;i++) {
            d = Desktops[i];  
            d.wallpaperPlugin = "org.kde.image";
            d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
            if (side==0) {
                d.writeConfig("Image", "file:/""" + filename + """_1""" + ext + """");
                side = 1;
            } else {
                d.writeConfig("Image", "file:/""" + filename + """_0""" + ext +  """");
                side = 0;        
            }}'
    """


def get_json(key):
    with open(pwd + '/settings.json' ,'r+') as file:
        file_data = json.load(file)
        return file_data[key]

def write_json(key, value, cat_flag):
    with open(pwd + '/settings.json' ,'r+') as file:
        file_data = json.load(file)
    if cat_flag == True:
        file_data["categories"][key] = value
    else:
        file_data[key] = value
    with open(pwd + '/settings.json' ,'w') as file:
        json.dump(file_data, file)

def set_next():
    query = get_query_category()      
    image_url = "https://source.unsplash.com/random/3840x1080/?" + query
    filename = 'img_' + str(time.strftime("%Y%m%d_%H%M%S")) + '.jpg'

    img = requests.get(image_url, stream = True)
    # Check if the image was retrieved successfully
    if img.status_code == 200:
        # Set decode_content value = True, else file size = 0
        img.raw.decode_content = True
        with open(pwd + '/tmp/' + filename,'wb') as file:
            shutil.copyfileobj(img.raw, file)
            if get_json("save") == "True":
                shutil.copyfile(pwd + '/tmp/' + filename, pwd + '/img/' + filename)
    try:
        split_image(pwd + '/tmp/' + filename, 1, 2, False, False, True, pwd + '/tmp/')
        filename, ext = os.path.splitext(filename)
        subprocess.run(get_command_str(pwd + '/tmp/' + filename, ext), shell = True, executable="/bin/bash")
        time.sleep(1)
        for f in os.listdir(pwd + '/tmp/'):
            os.remove(pwd + '/tmp/' + f)
    except:
        pass      
        

def start_timer(arg):
    bg_t = threading.Thread(target=timer_loop, args=(arg, ), daemon=True)
    bg_t.start()

def set_timer(value):
    stop_event.set()
    write_json("timer", value, False)
    print('Timer value set:', value)
    time.sleep(1.1)
    if value != 'off':
        stop_event.clear()
        start_timer(value)

def get_query_category():
    selected=[]
    for key, value in get_json("categories").items():
        if value == "True":
            selected.append(key)
    return random.choice(selected)

def set_categories(key):
    value = str(not eval(get_json("categories")[key]))
    write_json(key, value, True)
    print('Category set:', key, '=', value)
    
def set_save(value):
    write_json("save", value, False)
    print('Save set:', value)

def timer_loop(value):
    i = 0
    while True:
        set_next()        
        while i < int(value): 
            if stop_event.is_set():
                break       
            time.sleep(1)
            i+=1        
        if stop_event.is_set():
                break 
        if i == int(value):
            i=0

if __name__ == '__main__':
    ############## Init Settings ##############
    timer_val = get_json("timer")
    save_val = get_json("save")
    cat_sel = get_json("categories")
    if timer_val != 'off':
        start_timer(timer_val)

    ############### Menu Config ###############
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    # Adding an icon
    icon = QIcon(pwd + "/icon.png")
    # Adding item on the menu bar
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    # Create Menu
    menu = QMenu()

    ################ Next Menu ################    
    next = QAction("Next Wallpaper")
    next.triggered.connect(set_next)
    menu.addAction(next)
           
    ################ Timer Menu ###############     
    timer_choices= {}
    timer = menu.addMenu("Timer Settings")
    timer_group = QActionGroup(None)
    for key in timer_dict:
        timer_choices[key] = QAction(key, checkable = True)
        timer_choices[key].triggered.connect((lambda key=key: lambda: set_timer(timer_dict[key]))())
        timer.addAction(timer_choices[key])
        timer_group.addAction(timer_choices[key])        
        if timer_val == timer_dict[key]:
            timer_choices[key].setChecked(True)
    
    ################ Save Menu ################
    save = menu.addMenu("Save Pictures")  
    save_on = QAction("On", checkable = True)
    save_off = QAction("Off", checkable = True)
    
    if save_val == "True":
        save_on.setChecked(True)
    if save_val == "False":
        save_off.setChecked(True)
    
    save.addAction(save_on)
    save.addAction(save_off)
    
    save_group = QActionGroup(None)
    save_group.addAction(save_on)
    save_group.addAction(save_off)
    
    save_on.triggered.connect(lambda: set_save("True"))  
    save_off.triggered.connect(lambda: set_save("False"))      
    
    ############# Categories Menu #############
    cat_choices= {}
    categories = menu.addMenu("Categories") 
    for key in cat_sel:
        cat_choices[key] = QAction(key, checkable = True)
        if cat_sel[key] == "True":
            cat_choices[key].setChecked(True)
        cat_choices[key].triggered.connect((lambda key=key: lambda: set_categories(key))())
        categories.addAction(cat_choices[key])       
    
    ################ Quit Menu ################
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    ############### System Tray ###############
    tray.setContextMenu(menu)
    
    ################ Start App ################
    app.exec()
    
