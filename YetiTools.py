bl_info = {
    "name": "YetiTools",
    "description": "Tools we use at yeTiVision studio..",
    "author": "Roman Chumak (p4ymak)",
    "version": (0, 10, 12),
    "blender": (2, 77, 0),
    "location": "View3D > Toolbar > YetiTools",
    "category": "Object",
    'wiki_url': '',
    'tracker_url': 'http://www.p43d.com'
    }

import bpy, math, addon_utils
from bpy.props import *

"""
--------------------------------------------------------
Variables
--------------------------------------------------------
"""



"""
--------------------------------------------------------
REiterater
--------------------------------------------------------
"""

bpy.types.Scene.ctrlc = ""
def REiterater():

    selobjs = bpy.context.selected_objects
    bpy.context.area.type = 'INFO'
    bpy.ops.info.report_copy()
    bpy.ops.info.select_all_toggle()
    bpy.context.area.type = 'VIEW_3D'


    if bpy.data.window_managers["WinMan"].clipboard != "":
        bpy.types.Scene.ctrlc = bpy.data.window_managers["WinMan"].clipboard

   
    act = bpy.context.active_object
    oblist = []
    
    for ob in bpy.context.selected_objects:
        oblist.append(ob.name)
    bpy.ops.object.select_all(action='DESELECT')
    
    for ob in oblist:

        bpy.data.objects[ob].select = True
        bpy.context.scene.objects.active = bpy.data.objects[ob]

        exec(bpy.types.Scene.ctrlc)
        bpy.data.objects[ob].select = False

    for ob in oblist:
        bpy.data.objects[ob].select = True
    bpy.data.window_managers["WinMan"].clipboard = ""
    print("-----------------Blender Clipboard")
    print(bpy.data.window_managers["WinMan"].clipboard)
    print("-----------------My one Clipboard")
    print(bpy.types.Scene.ctrlc)


class REiteraterOperator(bpy.types.Operator):
    """Repeat selected last operations for all selected objects"""
    bl_idname = "object.reiterater"
    bl_label = "RE:iterate"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        REiterater()
        return {"FINISHED"}



"""
--------------------------------------------------------
Mapper
--------------------------------------------------------
"""

def Mapper():
    act = bpy.context.active_object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project()
    bpy.ops.uv.seams_from_islands()
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.uv.pack_islands(margin=0.001)
    bpy.ops.object.editmode_toggle()

class MapperOperator(bpy.types.Operator):
    """Smart UV Project for selected objects"""
    bl_idname = "object.mapper"
    bl_label = "Mapper"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        Mapper()
        return {"FINISHED"}


"""
--------------------------------------------------------
UniBoo
--------------------------------------------------------
"""

def UniBooing():
    act = bpy.context.active_object
    delete_origins = True
    oblist = []
    for ob in bpy.context.selected_objects:
        oblist.append(ob.name)
    if oblist.__len__() != 0:
        oblist.remove(act.name)
    for ob in oblist:
        name = str(ob)
        act.modifiers.new("UniBoo", type='BOOLEAN')
        act.modifiers["UniBoo"].operation = 'UNION'
        act.modifiers["UniBoo"].object = bpy.data.objects[name]
        bpy.ops.object.modifier_apply(modifier='UniBoo')
    if delete_origins == True:
        act.select = False
        bpy.ops.object.delete()
        if oblist.__len__() != 0:
            act.select = True

class UniBooOperator(bpy.types.Operator):
    """Apply Union Boolean to all selected objects"""
    bl_idname = "object.uniboo"
    bl_label = "UniBoo"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        UniBooing()
        return {"FINISHED"}




"""
--------------------------------------------------------
LockLayer
--------------------------------------------------------
"""

def LockLayer():

    objects_on_layers = []
    for l in range(0,20):
        if bpy.context.scene.layers[l] == True:
            objects_on_layers += [ob for ob in bpy.context.scene.objects if ob.layers[l]]
    for ob in objects_on_layers:
        ob.hide_select = True

def UnLockLayer():

    objects_on_layers = []
    for l in range(0,20):
        if bpy.context.scene.layers[l] == True:
            objects_on_layers += [ob for ob in bpy.context.scene.objects if ob.layers[l]]
    for ob in objects_on_layers:
        ob.hide_select = False


class LockLayerOperator(bpy.types.Operator):
    """Restrict viewport selection on selected layers"""
    bl_idname = "object.locklayer"
    bl_label = ""
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        LockLayer()
        return {"FINISHED"}

class UnLockLayerOperator(bpy.types.Operator):
    """Allow viewport selection on selected layers"""
    bl_idname = "object.unlocklayer"
    bl_label = ""
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        UnLockLayer()
        return {"FINISHED"}


"""
--------------------------------------------------------
ShowWire
--------------------------------------------------------
"""

def ShowWire():

    for ob in bpy.context.selected_objects:
        ob.show_wire = True
        ob.show_all_edges = True 

def HideWire():

    for ob in bpy.context.selected_objects:
        ob.show_wire = False
        ob.show_all_edges = False


class ShowWireOperator(bpy.types.Operator):
    """Show wire and draw all edges on selected objects"""
    bl_idname = "object.showwirer"
    bl_label = ""
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        ShowWire()
        return {"FINISHED"}

class HideWireOperator(bpy.types.Operator):
    """Hide wire on selected objects"""
    bl_idname = "object.hidewirer"
    bl_label = ""
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        HideWire()
        return {"FINISHED"}



"""
--------------------------------------------------------
PIndexer
--------------------------------------------------------
"""

def PIndexer():
    act = bpy.context.active_object
    oblist = []
    for ob in bpy.context.selected_objects:
        oblist.append(ob.name)
    for ob in oblist:
        name = str(ob)
        bpy.data.objects[name].pass_index = bpy.context.scene.pinteger

class PIndexerOperator(bpy.types.Operator):
    bl_idname = "object.pindexer"
    bl_label = "PIndexer"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        PIndexer()
        return {"FINISHED"}


"""
--------------------------------------------------------
PIselect
--------------------------------------------------------
"""

bpy.types.Scene.pinteger = bpy.props.IntProperty(default=0, min=0, step=1)
def PIselect():
    obs = bpy.data.objects
    pii = bpy.context.scene.pinteger
    object = ""
    for ob in obs:
        object = bpy.data.objects[ob.name]
        object.select = False
        if object.pass_index == pii:
            object.select = True

class PIsecelctOperator(bpy.types.Operator):
    bl_idname = "object.piselect"
    bl_label = "Select by PI"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        PIselect()
        return {"FINISHED"}



"""
--------------------------------------------------------
Leeloo
--------------------------------------------------------
"""
def Leelooer():
    addonpath = addon_utils.paths()[1]
    leeloopath = addonpath + "/Leeloo.blend\\NodeTree\\"

    if bpy.data.filepath == "":
        bpy.ops.object.notsaved_operator('INVOKE_DEFAULT')
    else:
        if 'Leeloo' not in bpy.data.node_groups:
            bpy.ops.wm.append(directory=leeloopath, filename="Leeloo", link=False)
        Lilu = bpy.data.node_groups["Leeloo"]

        filelength = len(bpy.data.filepath)
        blendfilename = bpy.data.filepath[0: filelength - 6]
        Lilu.nodes["Passes Output"].base_path = blendfilename + "_" + "Multipass/"

        pilist = []
        x = ""
        for i in bpy.data.objects:
            if i.pass_index not in pilist:
                pilist.append(i.pass_index)
        print(pilist)
        for i in range(10):
            if i in pilist:
                x = "IOB" + str(i)
                print(x)
                Lilu.nodes[x].outputs[0].enabled = True
                Lilu.links.new(Lilu.nodes["Passes Output"].inputs[8+i], Lilu.nodes[x].outputs[0])
            else:
                x = "IOB" + str(i)
                Lilu.nodes[x].outputs[0].enabled = False


        malist = []
        x = ""
        for i in bpy.data.materials:
            if i.pass_index not in malist:
                malist.append(i.pass_index)
        print(malist)
        for i in range(10):
            if i in malist:
                x = "IMA" + str(i)
                print(x)
                Lilu.nodes[x].outputs[0].enabled = True
                Lilu.links.new(Lilu.nodes["Passes Output"].inputs[18+i], Lilu.nodes[x].outputs[0])
            else:
                x = "IMA" + str(i)
                Lilu.nodes[x].outputs[0].enabled = False

class LeelooOperator(bpy.types.Operator):
    """Leeloo Dallas mul-ti-pass.."""
    bl_idname = "object.leeloo"
    bl_label = "Leeloo"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        Leelooer()
        return {"FINISHED"}



"""
--------------------------------------------------------
Zorro
--------------------------------------------------------
"""

def Zorro():
    if bpy.data.filepath == "":
        bpy.ops.object.notsaved_operator('INVOKE_DEFAULT')
    else:
        masked = []

        selobjs = bpy.context.selected_objects
        filelength = len(bpy.data.filepath)
        blendfilename = bpy.data.filepath[0: filelength - 6]
        obname = bpy.context.active_object.name
        bpy.context.scene.render.filepath = blendfilename + "_Multipass/Masks/" + obname + "/" + obname + "_mask_"
        bpy.context.scene.render.resolution_percentage = 100
        bpy.context.scene.render.use_overwrite = True
        bpy.context.scene.render.use_file_extension = True
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.image_settings.color_mode = 'BW'
        bpy.context.scene.render.image_settings.color_depth = '8'
        bpy.context.scene.render.image_settings.compression = 0

        bpy.context.scene.view_settings.view_transform = "Default"
        bpy.context.scene.view_settings.exposure = 0
        bpy.context.scene.view_settings.gamma = 1
        bpy.context.scene.view_settings.look = "None"
        bpy.context.scene.view_settings.use_curve_mapping = False
        bpy.context.scene.sequencer_colorspace_settings.name = "sRGB"

        bpy.context.scene.render.engine = 'BLENDER_RENDER'
        bpy.context.scene.world.horizon_color = (0, 0, 0)

        bpy.context.space_data.show_only_render = True
        bpy.context.space_data.viewport_shade = 'TEXTURED'
        bpy.context.scene.game_settings.material_mode = 'GLSL'
        mat = bpy.data.materials.new("DarkMatter")
        for i in bpy.data.objects:
            if i.type == 'MESH' or i.type == 'CURVE' or i.type == 'SURFACE' and len(i.material_slots) == 0:
                i.data.materials.append(mat)

        for i in bpy.data.materials:
            i.diffuse_color = 0,0,0
            i.specular_intensity = 0
            i.emit = 1
            i.use_nodes = False

        mswh = bpy.data.materials.new("MaskWhite")
        mswh.diffuse_color = 1,1,1
        for i in selobjs:
            for m in i.material_slots:
                m.material = mswh
                m.material.emit = 1
                m.material.specular_intensity = 0
                m.material.use_nodes = False

        bpy.ops.object.select_all(action='DESELECT')


        bpy.context.space_data.show_background_images = False
        bpy.context.scene.render.use_antialiasing = True
        bpy.context.scene.render.antialiasing_samples = '16'
        bpy.ops.render.opengl(animation=True, sequencer=False, write_still=False, view_context=True)
        bpy.ops.render.view_show()

class ZorroOperator(bpy.types.Operator):
    """OpenGL Render Mask for Selected Objects"""
    bl_idname = "object.zorro"
    bl_label = "Zorro"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        Zorro()
        return {"FINISHED"}

"""
--------------------------------------------------------
FBX Export
--------------------------------------------------------
"""
def FBX_Batch():

    import bpy
    import os

    # export to blend file location
    basedir = os.path.dirname(bpy.data.filepath)

    if not basedir:
        raise Exception("Blend file is not saved")

    scene = bpy.context.scene

    obj_active = scene.objects.active
    selection = bpy.context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')

    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)

    dir = directory + "/fbx/" 

    if not os.path.exists(dir):
        os.makedirs(dir)


    for obj in selection:

        obj.select = True

        # some exporters only use the active object
        scene.objects.active = obj

        name = bpy.path.clean_name(obj.name)
        fbx = "fbx"
        fn = os.path.join(basedir, fbx, name)
        print(basedir)
            
        bpy.ops.export_scene.fbx(filepath = fn + ".fbx", global_scale=1, use_mesh_modifiers=True, use_selection=True, version='BIN7400', object_types={'MESH'}, bake_anim=False )

        obj.select = False

        print("written:", fn)


    scene.objects.active = obj_active

    for obj in selection:
        obj.select = True

class FBXBatchOperator(bpy.types.Operator):
    """Batch Export selected objects to FBX files.."""
    bl_idname = "object.fbxbatch"
    bl_label = "Export static FBX"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        FBX_Batch()
        return {"FINISHED"}


"""
--------------------------------------------------------
MatNamer
--------------------------------------------------------
"""

def MatNamer():
    for ob in bpy.context.selected_objects:
        for matslot in bpy.data.objects[ob.name].material_slots:
            if bpy.data.materials[matslot.name].texture_slots[0] != None:
                texsname = bpy.data.materials[matslot.name].texture_slots[0].texture.name
                bpy.data.materials[matslot.name].name = bpy.data.textures[texsname].image.name


class MatNamerOperator(bpy.types.Operator):
    """Rename materials by textures"""
    bl_idname = "object.matnamer"
    bl_label = "Matnamer"
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        MatNamer()
        return {"FINISHED"}


"""
--------------------------------------------------------
LowestPoint
--------------------------------------------------------
"""
def LowestPoint():
    Scene_Name = bpy.context.scene.name
    #print('----')
    vertglob = []
    lowest = []

    ob = bpy.context.active_object
    if bpy.data.objects[ob.name].type == 'MESH':
        meshname = bpy.data.objects[ob.name].data.name
        mat = ob.matrix_world
        vertglob[:]={}
        firstv = mat*bpy.data.meshes[meshname].vertices[0].co
        vz = firstv[2]
        for v in bpy.data.meshes[meshname].vertices:
            vg=mat*v.co
            vertglob.append(vg)
          
           # print('obsp ', v.co)
           # print('glob ', vg)

            if vg[2] <= vz:
                vz = vg[2]
        
        lowest[:]=[]
        for v in vertglob:
            if abs(v[2] - vz) <= 0.000001:
                lowest.append(v)
        
        lx = 0
        ly = 0
        lz = 0
        
        for v in lowest:
            lx += v[0]
            ly += v[1]
            lz += v[2]
            
        lx = lx / len(lowest)
        ly = ly / len(lowest) 
        lz = lz / len(lowest)
    
    
#    print('lowest num ', len(lowest))
#    print('lowest',vz)
    
#    print('Average ', lx,ly,lz)
        bpy.data.scenes[Scene_Name].cursor_location = lx,ly,lz

class LowestPointOperator(bpy.types.Operator):
    """Find the Lowest meridian"""
    bl_idname = "object.lowestpoint"
    bl_label = ""
    bl_options = {"UNDO"}
    def invoke(self, context, event):
        LowestPoint()
        return {"FINISHED"}




"""
--------------------------------------------------------
Errors
--------------------------------------------------------
"""
class SaveFirstOperator(bpy.types.Operator):
    bl_idname = "object.notsaved_operator"
    bl_label = "Blender File need to be saved first.."

    def execute(self, context):
        self.report({'WARNING'}, "ballala")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)





"""
--------------------------------------------------------
UI
--------------------------------------------------------
"""

class YetiToolPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "YetiTools"

    def draw(self, context):
        layout = self.layout 
        row = layout.row(align=True)
        row.operator("object.locklayer", icon="RESTRICT_SELECT_ON")
        row.operator("object.unlocklayer", icon="RESTRICT_SELECT_OFF")
        row.separator()
        row.operator("object.showwirer", icon="MESH_GRID")
        row.operator("object.hidewirer", icon="MESH_PLANE")
        row.separator()
        row.operator("object.lowestpoint", icon="HAND")

        col = layout.column(align=True)
        col.separator()   
        col.operator("object.reiterater", icon="RADIO")
        col.separator()
        col.operator("object.uniboo", icon="MESH_CUBE")
        col.operator("object.mapper", icon="TEXTURE")
        col.separator()

        row = layout.row(align=True)
        row.prop(bpy.context.scene, "pinteger", text="PI")
        row.operator("object.piselect")
        col = layout.column(align=True)
        col.operator("object.pindexer", icon="RENDERLAYERS")

        col.separator()
        col.operator("object.leeloo", icon="IMAGE_COL")
        col.separator()
        col.operator("object.zorro", icon="MOD_MASK")
        col.separator()
        col.operator("object.matnamer", icon="MATERIAL")
        col.separator()
        col.operator("object.fbxbatch", icon="EXPORT")


def register():
    bpy.utils.register_class(YetiToolPanel)
    bpy.utils.register_class(UniBooOperator)
    bpy.utils.register_class(REiteraterOperator)
    bpy.utils.register_class(MapperOperator)
    bpy.utils.register_class(PIndexerOperator)    
    bpy.utils.register_class(PIsecelctOperator)
    bpy.utils.register_class(LeelooOperator)
    bpy.utils.register_class(ZorroOperator)
    bpy.utils.register_class(SaveFirstOperator)
    bpy.utils.register_class(LockLayerOperator)
    bpy.utils.register_class(UnLockLayerOperator)
    bpy.utils.register_class(ShowWireOperator)
    bpy.utils.register_class(HideWireOperator)
    bpy.utils.register_class(MatNamerOperator)
    bpy.utils.register_class(FBXBatchOperator)
    bpy.utils.register_class(LowestPointOperator)

def unregister():
    bpy.utils.unregister_class(YetiToolPanel)
    bpy.utils.unregister_class(UniBooOperator)
    bpy.utils.unregister_class(REiteraterOperator)
    bpy.utils.unregister_class(MapperOperator)
    bpy.utils.unregister_class(PIndexerOperator)
    bpy.utils.unregister_class(PIsecelctOperator)
    bpy.utils.unregister_class(LeelooOperator)
    bpy.utils.unregister_class(ZorroOperator)
    bpy.utils.unregister_class(SaveFirstOperator)
    bpy.utils.unregister_class(LockLayerOperator)
    bpy.utils.unregister_class(UnLockLayerOperator)
    bpy.utils.unregister_class(ShowWireOperator)
    bpy.utils.unregister_class(HideWireOperator)
    bpy.utils.unregister_class(MatNamerOperator)
    bpy.utils.unregister_class(FBXBatchOperator)
    bpy.utils.unregister_class(LowestPointOperator)
