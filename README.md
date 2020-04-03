# VSRender

An addon for parallel rendering for video sequencer in blender.

**Dependencies**

Ffmpeg must be installed and should be executable from anywhere.
Linux (This addon was tested on Linus Mint 19). Does not work on any other OS out of the box.
Blender 2.80 or above (This addon was test in Blender 2.82)

**Features**

* Splits the render into many parts
* Renders the parts separately in background, utilizing all cores on your machine
* Joins the parts (if needed) using Ffmpeg

**Intro**

The current situation as far as the Blender Video Sequencer is concerned, is that it is awesome, but is extremely slow in rendering as it utilizes only one thread. Even if you have 16 cores, it does not help. VS is ok for small videos but the render times can go to many hours for long videos. So far many solutions were offered to solve this issue outside the main Blender dev community. Many use the splitting method, and this addon uses the same approach. I tried some, but unfortunately none worked well with the new versions (or on Linux). This addon is simple and very specific to my own needs. Hopefully it will be useful for you. It can be adapted for Windows etc by making some minor changes.

**Intro Video**

Coming Soon

**Installtion**

Download the VSRender.py file from this repository. Or get the zip file from the releases page.
Install from the Blender Menu > Edit > Preferences > Add-ons > Install. Pick this file. Enable this addon.
You will find the UI in the Video Sequencer window when you press N.

**Usage**

Once you finish editing your awesome video. Click the the **VSRender tab** in the "N" panel. 
Set the number of **Parts**. It can be any number but will be typically the number of cores you have in your machine.

Click the **Split** button. The frame range is split into specified parts. The frame count of each part is shown below this button. The last part frame count includes the remaining frames. This action creates shell scripts that contain he command for launching Blender in background with render arguments for specified frames.

Click the **Parallel Render** button to start rendering all parts at once.

Tick the **Open Terminal** check box if you like to see the progress of renders in terminal windows. If it causes problems try unchecking it. (_Note: You can stop the renders by killing the process from System Monitor or from command line_)












