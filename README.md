# VSRender

An addon for parallel rendering for video sequencer in blender.

---

![logo](https://oormi.in/software/software_images/vsrenderthumb.jpg)

---


**Requirements**

* Linux (_This addon was tested on Linux Mint 19_). Does not work on any other OS out of the box.
* Blender 2.80 or above (_This addon was tested in Blender 2.82_)
* [Optional] Ffmpeg must be installed and should be executable from anywhere in order to use the join video parts feature. (_This addon was tested with ffmpeg 3.4.6_)

**Features**

* Splits the video sequencer render into many parts
* Renders the parts separately in background, utilizing all cores on your machine
* Joins the parts (if needed) using Ffmpeg

**Intro**

The current situation as far as the Blender Video Sequencer is concerned, is that it is awesome, but is extremely slow in rendering as it utilizes only one thread. Even if you have 16 cores, it does not help. VS is ok for small videos but the render times can go to many hours for long videos. So far many solutions were offered to solve this issue outside the main Blender dev community. I tried some, but unfortunately none worked well with the new versions (or on Linux). Many use the splitting method, and this addon uses the same approach. This addon is simple and very specific to my own needs. Hopefully it will be useful for you. It can be adapted for Windows etc by making some minor changes.

**Intro Video**

https://youtu.be/Y73kQxqMpew

**Download and Installtion**

Download the VSRender.py file from this repository. Or get the zip file from the releases page.
https://github.com/oormicreations/VSRender/releases

Install from the Blender Menu > Edit > Preferences > Add-ons > Install. Pick this file. Enable this addon.
You will find the UI in the Video Sequencer window when you press N.

**Usage**

Once you finish editing your awesome video. Click the the **VSRender tab** in the "N" panel. 
Set the number of **Parts**. It can be any number but will be typically the number of cores you have in your machine.

Click the **Split** button. The frame range is split into specified parts. The frame count of each part is shown below this button. The last part frame count includes the remaining frames. This action creates shell scripts that contain the command for launching Blender in background with render arguments for specified frames.

Click the **Parallel Render** button to start rendering all parts at once. Make sure that you have set a output render path in blender render settings in Output tab in properties window. If you wish to use the built in Join function, make sure that it does **not** contain a prefix for the file names or zero padding characters.

Before you click render, tick the **Open Terminal** check box if you like to see the progress of renders in terminal windows. If it causes problems try unchecking it. (_Note: You can stop the renders by killing the process from System Monitor or from command line_)

You can choose the **Terminal** type from the drop down box. Pick **Generic** if you are not sure. If your terminal program is not listed you can enter the command directly in the box below. Use $scriptname as a dummy name, this will be replaced by actual shell script file. For example this works for gnome:

`gnome-terminal --command="bash -c './$scriptname;'"`

When the render is over, click the **Join Parts** button to join them. This is useful when you have rendered videos not image sequences. It uses ffmpeg to concatenate the parts. So it must be installed to use this feature. You can join them via cli also.

**Out File Name** is the name of the joined video. You can use a custom ffmpeg **Command** to join them. The default **Extension** is mkv, but you can change it here before joining the parts.

**Help | Source | Updates** brings you to this page on GitHub.


**Known Issues**

* There is minimum error check at this point.
* It uses bash scripts so is sensitive to your Linux flavor or settings.
* If you find that the scripts are not executing, try setting the permissions. The addon will attempt to set the permissions by default. Linux Mint automatically sets the permissions somehow.
* It is tested on **gnome-terminal** only. If you use some other terminal, and it is not working, please edit the code suitably.
* It uses the default 0 padding in frame numbers. If you changed it, it won't recognize the file part renders to join.
* It will not recognize the parts if a file name prefix was set in the output render path, or if zero padding characters (e.g. ####) are set there. This is not an issue btw.
* Tip : Check in blender python console for helpful messages.
* **Always save your stuff!**

**What is new in version 0.2.0**
* Sanity checks for output path
* Supports relative paths
* Supports more terminal types
* Sets script permissions to rwx
* Some minor improvements


**Misc Info**

This plugin has been released under MIT license, which means it is free for any kind of use and modification, but has no warranties or liabilities. Please read the license before you download and use it. 

**About**

A FOSS Project by Oormi Creations.

http://oormi.in

A limited support is available via email.

oormicreations@gmail.com


![logo](https://oormi.in/software/cbp/images/OormiLogo.png)

May 2020.









