# wallp  
    
Random HD automatic dual monitor 3840x1080 wallpapers for KDE. Apply random Unsplash  
wallpapers from selected categories to a dual monitor setup on KDE from, built on PyQt6.  
Auto wallpaper timer, image save, and skip. Install script is for a systemd configuration.  
  
To Install:
```
git clone https://github.com/mistercamp/wallp.git  
cd wallp    
./install
```  
  
To Uninstall:
```
./uninstall
```  
  
How to use:  
START:
```
sudo systemctl start wallp.service
```
     
STOP:
```
sudo systemctl stop wallp.service
```  
  
Notes:  
If the 'save' option is enabled, wallpapers will be saved in /opt/wallp/img  
  
Available Options:  
Next Wallpaper   (Skip)  
Auto Wallpaper:  15min, 30min, 1hr, 3hr, 6hr, Off  
Save Wallpapers: On, Off  
Categories:      Space, Cars, Nature, Landscape, City, Night, Wallpapers  
Quit  


  
![ksnip_20231018-223741](https://github.com/mistercamp/wallp/assets/148037744/aa2afcca-4818-4053-9634-541e088a7e8a)
