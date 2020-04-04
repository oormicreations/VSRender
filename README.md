# VSRender

An addon for parallel rendering for video sequencer in blender.

**Requirements**

* Linux (_This addon was tested on Linus Mint 19_). Does not work on any other OS out of the box.
* Blender 2.80 or above (_This addon was tested in Blender 2.82_)
* [Optional] Ffmpeg must be installed and should be executable from anywhere in order to use the join video parts feature.

**Features**

* Splits the video sequencer render into many parts
* Renders the parts separately in background, utilizing all cores on your machine
* Joins the parts (if needed) using Ffmpeg

**Intro**

The current situation as far as the Blender Video Sequencer is concerned, is that it is awesome, but is extremely slow in rendering as it utilizes only one thread. Even if you have 16 cores, it does not help. VS is ok for small videos but the render times can go to many hours for long videos. So far many solutions were offered to solve this issue outside the main Blender dev community. I tried some, but unfortunately none worked well with the new versions (or on Linux). Many use the splitting method, and this addon uses the same approach. This addon is simple and very specific to my own needs. Hopefully it will be useful for you. It can be adapted for Windows etc by making some minor changes.

**Intro Video**

Coming Soon

**Installtion**

Download the VSRender.py file from this repository. Or get the zip file from the releases page.
Install from the Blender Menu > Edit > Preferences > Add-ons > Install. Pick this file. Enable this addon.
You will find the UI in the Video Sequencer window when you press N.

**Usage**

Once you finish editing your awesome video. Click the the **VSRender tab** in the "N" panel. 
Set the number of **Parts**. It can be any number but will be typically the number of cores you have in your machine.

Click the **Split** button. The frame range is split into specified parts. The frame count of each part is shown below this button. The last part frame count includes the remaining frames. This action creates shell scripts that contain the command for launching Blender in background with render arguments for specified frames.

Click the **Parallel Render** button to start rendering all parts at once.

Before you click render, tick the **Open Terminal** check box if you like to see the progress of renders in terminal windows. If it causes problems try unchecking it. (_Note: You can stop the renders by killing the process from System Monitor or from command line_)

When the render is over, click the **Join Parts** button to join them. This is useful when you have rendered videos not image sequences. It uses ffmpeg to concatenate the parts. So it must be installed to use this feature. You can join them via cli also.

**Out File Name** is the name of the joined video. You can use a custom ffmpeg **Command** to join them. The default **Extension** is mkv, but you can change it here before joining the parts.

**Help | Source | Updates** brings you to this page on GitHub.


**Known Issues**

* There is minimum error check at this point.
* It uses bash scripts so is sensitive to your Linux flavor or settings.
* If you find that the scripts are not executing, try setting the permissions. Linux Mint automatically sets the permissions somehow.
* It uses **gnome-terminal** to display the output of scripts. If you use some other terminal, please edit the code suitably.
* It uses the default 0 padding in frame numbers. If you changed it, it won't recognize the file part renders to join.
* **Always save your stuff!**


**Misc Info**

This plugin has been released under MIT license, which means it is free for any kind of use and modification, but has no warranties or liabilities. Please read the license before you download and use it. 

**About**


---

A FOSS Project by Oormi Creations

http://oormi.in

oormicreations@gmail.com


![logo](https://oormi.in/software/cbp/images/OormiLogo.png)

April 2020.









