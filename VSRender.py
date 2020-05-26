# VS Parallel Render by Oormi Creations
#http://oormi.in


bl_info = {
    "name": "VS Render",
    "description": "Renders the video sequencer in parallel utilizing all cores",
    "author": "Oormi Creations",
    "version": (0, 2, 0),
    "blender": (2, 80, 0),
    "location": "Video Sequencer > VS Render",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/oormicreations/VSRender",
    "tracker_url": "https://github.com/oormicreations/VSRender",
    "category": "Sequencer"
}

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       IntVectorProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

import os
import stat
from bpy import context
import codecs
import shutil
import platform

#globals
ranges = []
sframes = []
eframes = []   
issplit = False


def ShowMessageBox(message = "", title = "VS Render Says...", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


def printconsole(data, tag = "VS: "):
    if tag != "VS: ":
        tag = "VS: " + tag + ": "
        
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            #print(area.type)
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=tag+str(data), type="OUTPUT") 

def pc(data, tag = "VS: "):
   printconsole(data, tag)

def getrenderoutputpath():
    #check output path
    outpath =   bpy.context.scene.render.filepath
    
    if outpath == "/tmp/" or outpath == "":
        ShowMessageBox("Please set an Ouput path in Properties panel > Output Properties > Output")
        return None
    if outpath[-1] != "/":
        ShowMessageBox("Please set an Ouput path in Properties panel > Output Properties > Output and ensure that the path exists and that there is no file name prefix in the end of the path (It should have / as last character)")
        return None
    
    if outpath.find("//") >=0:
        outpath = bpy.path.abspath(outpath)
    
    return outpath

def splitparts(nparts, tool):

    outpath = getrenderoutputpath()
    if outpath == None:
        return
        
    fstart = bpy.context.scene.frame_start
    fend = bpy.context.scene.frame_end
    nframes = fend - fstart + 1
    printconsole(nframes, "nframes")
    
    partlen = int(nframes/nparts)
    rem = nframes%nparts
    printconsole(partlen, "plen")
    printconsole(partlen+rem, "lastpart")
    
    tool.vsr_partframes = partlen
    tool.vsr_partframeslast = partlen + rem
        
    global ranges
    global sframes
    global eframes
    ranges = []
    sframes = []
    eframes = []

    nextstart = 0
    fstartpart = fstart
        
    for p in range(1, nparts):
        fendpart = fstartpart + partlen -1
        
        rangestr = str(fstartpart) + "-" + str(fendpart)
        printconsole(rangestr)
        ranges.append(rangestr)
        sframes.append(fstartpart)
        eframes.append(fendpart)
        
        fstartpart = fendpart + 1
    
    
    fendpart = fstartpart + partlen + rem - 1
    rangestr = str(fstartpart) + "-" + str(fendpart)
    printconsole(rangestr)
    ranges.append(rangestr)
    sframes.append(fstartpart)
    eframes.append(fendpart)
    
    printconsole(ranges, "Ranges") 
    
    #save sh scripts
    #blendfilename = bpy.path.basename(bpy.context.blend_data.filepath)
    blendfilepath = bpy.context.blend_data.filepath
    
    blendexe = bpy.app.binary_path
    blendexe = blendexe.replace(" ", "\ ")
    blendfilepath = blendfilepath.replace(" ", "\ ")
    
    
    shscript = "#!/bin/bash\n\
echo \"" + blendexe + "\"\n\
x=\"" + blendfilepath + " -x 1 -s %&#1 -e %&#2 -a\"\n\
echo $x\n\
eval \"" + blendexe + "\" -b \"$x\"\n\
echo \"VSE Render : Part %&#3 Render Done\""

    
    printconsole(outpath, "Saving sh scripts")
    
    for n in range(0, len(sframes)):    
        shstr = shscript.replace("%&#1", str(sframes[n]))
        shstr = shstr.replace("%&#2", str(eframes[n]))
        shstr = shstr.replace("%&#3", str(n + 1))
        
        shfile = outpath + ranges[n] + ".sh"
        temp = codecs.open(shfile, "w", "utf-8")
        temp.write(shstr)
        temp.close()
        os.chmod(shfile, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        printconsole(shfile)



def startrender(term, ttype, tcmd):
    global ranges
    global sframes
    global eframes

    outpath = getrenderoutputpath()
    if outpath == None:
        return
    
    pc(len(ranges), "Start render ranges")

    if term:
        
        for n in range(0, len(ranges)):
            shstr = ""
            if ttype=="GN":
                shstr = "gnome-terminal --title=Rendering_Section_" + ranges[n] + " --command=\"bash -c './" + ranges[n] + ".sh;'\""
            if ttype=="XF":
                shstr = "xfce4-terminal --title=Rendering_Section_" + ranges[n] + " --command=\"bash -c './" + ranges[n] + ".sh;'\""
            if ttype=="KN":
                shstr = "konsole --title=Rendering_Section_" + ranges[n] + " --command=\"bash -c './" + ranges[n] + ".sh;'\""
            if ttype=="EM":
                shstr = "x-terminal-emulator --title=Rendering_Section_" + ranges[n] + " --command=\"bash -c './" + ranges[n] + ".sh;'\""
            if ttype=="SB":
                shstr = tcmd.replace("$scriptname", ranges[n] + ".sh")
                pc(shstr)
                #shstr = gnome-terminal --command="bash -c './$scriptname;'" # This works for example
            
            print(os.getcwd())
            os.chdir(outpath)
            print(os.getcwd())
            os.system(shstr)
    else:
        for n in range(0, len(ranges)):
            cmd = outpath + ranges[n] + ".sh"
            os.spawnl(os.P_NOWAIT, cmd, cmd)
            #pc(n + 1, cmd)
            pc(n + 1, "Launching part")



def concat(tool):
    outpath = getrenderoutputpath()
    if outpath == None:
        return

    tool.vsr_res = "Concat in progress..."
    ext = tool.vsr_ffmpegext
    ext = ext.replace(".", "")
    
    global ranges
    global sframes
    global eframes
    
    liststr = ""
    for n in range(0, len(ranges)):
        liststr += "file "  + '{0:04d}'.format(sframes[n]) + "-" + '{0:04d}'.format(eframes[n]) + "." + ext + "\n"
    
    temp = codecs.open(outpath + "list.txt", "w", "utf-8")
    temp.write(liststr)
    temp.close()
    
    pc(liststr)

    printconsole(os.getcwd())
    os.chdir(outpath)
    printconsole(os.getcwd())

    jname = tool.vsr_outfilename
    cmd = tool.vsr_ffmpegcmd
    cmd = cmd.replace("joinedoutput", jname)
    printconsole(cmd)

    res = os.system(cmd)
    printconsole(res, "concat res")
    if res:
        printconsole("Concat failed!")
        tool.vsr_res = "Concat failed!"
    else:
        printconsole("Concat success!")
        tool.vsr_res = "Concat success!"



def on_update_parts(self, context):
    context.scene.vsr_tool.vsr_partframes = 0
    context.scene.vsr_tool.vsr_partframeslast = 0
    
def on_update_termcmd(self, context):
    context.scene.vsr_tool.vsr_termen = context.scene.vsr_tool.vsr_ttype == "SB"
    pc(context.scene.vsr_tool.vsr_termen)


####################################################################

class CRP_OT_CRenderParts(bpy.types.Operator):
    bl_idname = "render.parts"
    bl_label = "Render Parts"
    bl_description = "Render all parts in parallel"


    def execute(self, context):
        scene = context.scene
        vsrtool = scene.vsr_tool

        pc(issplit)
        if issplit:
            startrender(vsrtool.vsr_term, vsrtool.vsr_ttype, vsrtool.vsr_termcmd)
        else:
            ShowMessageBox("Please Split into parts before rendering!")
        
        return{'FINISHED'}


class CSP_OT_CSplitParts(bpy.types.Operator):
    bl_idname = "split.parts"
    bl_label = "Split Parts"
    bl_description = "Split the render frame range into specified parts"


    def execute(self, context):
        scene = context.scene
        vsrtool = scene.vsr_tool
        vsrtool.vsr_res = " "
        
        #os check
        if platform.system() != 'Linux':
            ShowMessageBox("This addon may not run properly on your OS! Supported OS: Linux")
        
        global ranges
        global sframes
        global eframes
        global issplit

        pc(vsrtool.vsr_parts, "Parts")
        splitparts(vsrtool.vsr_parts, vsrtool)
        pc(ranges, "VSR Ranges")
        pc(sframes, "VSR SFrames")
        pc(eframes, "VSR EFrames")
        
        issplit = True
        
        return{'FINISHED'}


class CCC_OT_CConCat(bpy.types.Operator):
    bl_idname = "con.cat"
    bl_label = "Con Cat"
    bl_description = "Join the rendered parts."

    def execute(self, context):
        scene = context.scene
        vsrtool = scene.vsr_tool
        concat(vsrtool)
        
        return{'FINISHED'}  
    
class OBJECT_PT_VSPanel(bpy.types.Panel):

    bl_label = "VS Render 0.2.0"
    bl_idname = "OBJECT_PT_VS_Panel2"
    bl_category = "VS Render"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_context = "objectmode"


    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        vsrtool = scene.vsr_tool
        
        layout.prop(vsrtool, "vsr_parts")
        layout.operator("split.parts", text = "Split", icon='TRIA_RIGHT')
        layout.label(text = "Part Frame Count : " + str(vsrtool.vsr_partframes))
        layout.label(text = "Last Part Frame Count : " + str(vsrtool.vsr_partframeslast))
        layout.label(text = " ")
        layout.prop(vsrtool, "vsr_term")
        layout.prop(vsrtool, "vsr_ttype")
        row = layout.row(align=True)
        row.enabled = vsrtool.vsr_termen
        row.prop(vsrtool, "vsr_termcmd")
        
        layout.operator("render.parts", text = "Parallel Render", icon='RENDER_ANIMATION')
        layout.label(text = " ")
        layout.prop(vsrtool, "vsr_outfilename")
        layout.prop(vsrtool, "vsr_ffmpegcmd")
        layout.prop(vsrtool, "vsr_ffmpegext")
        layout.operator("con.cat", text = "Join Parts", icon='ADD')
        layout.label(text = vsrtool.vsr_res)        
        row = layout.row(align=True)
        row.operator("wm.url_open", text="Help | Source | Updates", icon='QUESTION').url = "https://github.com/oormicreations/VSRender"



class CCProperties(PropertyGroup):
    
    vsr_outfilename: StringProperty(
        name = "Out File Name",
        description = "Name of the joined movie",
        default = "joinedoutput"
      )
      
    vsr_ffmpegcmd: StringProperty(
        name = "Cmd",
        description = "Ffmpeg Command",
        default = "ffmpeg -f concat -safe 0 -i list.txt -c copy -y joinedoutput.mp4"
      )

    vsr_ffmpegext: StringProperty(
        name = "Ext",
        description = "Part File Extension",
        default = "mkv"
      )

    vsr_parts: IntProperty(
        name = "Parts",
        description = "Number of parts to split into. (= Number of parallel renders)",
        default = 8,
        min=1,
        max=256,
        update=on_update_parts        
      )   
    
    vsr_partframes: IntProperty(
        name = "Part Frames",
        description = "Number of part frames",
        default = 0
      )
      
    vsr_partframeslast: IntProperty(
        name = "Part Frames Last",
        description = "Number of last part frames",
        default = 0
      )
    
    vsr_term: BoolProperty(
        name = "Open Terminal",
        description = "Open terminal windows while rendering",
        default = True
    )

    vsr_res: StringProperty(
        name = "Result",
        description = "NA",
        default = " "
      )

    vsr_ttype: EnumProperty(
        items = [('GN', 'Gnome', 'Terminal type gnome'), 
                 ('KN', 'Konsole', 'Terminal type Konsole'),
                 ('XF', 'Xfce4', 'Terminal type xfce'),
                 ('EM', 'Generic', 'Terminal type generic'),
                 ('SB', 'Specified Below', "Terminal type as specified below")],
        name = "Terminal",
        update = on_update_termcmd        
    )
        
    vsr_termcmd: StringProperty(
        name = "Term Cmd",
        description = "Terminal Command for your specific terminal",
        default = "Write the command to launch the shellscripts here with a $scriptname as standin for script name"

      )
    
    vsr_termen: BoolProperty(
        name = "Enable Terminal Cmd",
        description = "En",
        default = False
    )
    
# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    OBJECT_PT_VSPanel,
    CCProperties,
    CSP_OT_CSplitParts,
    CRP_OT_CRenderParts,
    CCC_OT_CConCat
)

def register():
    bl_info['blender'] = getattr(bpy.app, "version")
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.vsr_tool = PointerProperty(type=CCProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.vsr_tool



if __name__ == "__main__":
    register()