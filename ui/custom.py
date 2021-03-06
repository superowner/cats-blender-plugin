import bpy
import globs
import tools.common
import tools.supporter
import tools.armature_bones

from ui.main import ToolPanel
from ui.main import get_emtpy_icon

from tools.register import register_wrap
from tools.common import version_2_79_or_older


@register_wrap
class CustomPanel(ToolPanel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_custom_v3'
    bl_label = 'Custom Model Creation'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        if not version_2_79_or_older():  # TODO
            col = box.column(align=True)
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text='Not yet compatible with 2.8!', icon='INFO')
            col.separator()
            return

        row = col.row(align=True)
        row.operator('armature_custom.button', text='How to Use', icon='FORWARD')
        col.separator()

        row = col.row(align=True)
        row.prop(context.scene, 'merge_mode', expand=True)
        col.separator()

        # Merge Armatures
        if context.scene.merge_mode == 'ARMATURE':
            row = col.row(align=True)
            row.scale_y = 1.05
            row.label(text='Merge Armatures:')

            if len(tools.common.get_armature_objects()) <= 1:
                row = col.row(align=True)
                row.scale_y = 1.05
                col.label(text='Two armatures are required!', icon='INFO')
                return

            row = col.row(align=True)
            row.scale_y = 1.05
            row.prop(context.scene, 'merge_same_bones', text='Merge Same Bones Only')

            row = col.row(align=True)
            row.scale_y = 1.05
            row.prop(context.scene, 'merge_armature_into', text='Base', icon=globs.ICON_MOD_ARMATURE)
            row = col.row(align=True)
            row.scale_y = 1.05
            row.prop(context.scene, 'merge_armature', text='To Merge', icon_value=tools.supporter.preview_collections["custom_icons"]["UP_ARROW"].icon_id)

            if not context.scene.merge_same_bones:
                found = False
                base_armature = tools.common.get_armature(armature_name=context.scene.merge_armature_into)
                merge_armature = tools.common.get_armature(armature_name=context.scene.merge_armature)
                if merge_armature:
                    for bone in tools.armature_bones.dont_delete_these_main_bones:
                        if 'Eye' not in bone and bone in merge_armature.pose.bones and bone in base_armature.pose.bones:
                            found = True
                            break
                if not found:
                    row = col.row(align=True)
                    row.scale_y = 1.05
                    row.prop(context.scene, 'attach_to_bone', text='Attach to', icon='BONE_DATA')
                else:
                    row = col.row(align=True)
                    row.scale_y = 1.05
                    row.label(text='Armatures can be merged automatically!')

            row = col.row(align=True)
            row.scale_y = 1.2
            row.operator('armature_custom.merge_armatures', icon='ARMATURE_DATA')

        # Attach Mesh
        else:
            row = col.row(align=True)
            row.scale_y = 1.05
            row.label(text='Attach Mesh to Armature:')

            if len(tools.common.get_armature_objects()) == 0 or len(tools.common.get_meshes_objects(mode=1)) == 0:
                row = col.row(align=True)
                row.scale_y = 1.05
                col.label(text='An armature and a mesh are required!', icon='INFO')
                row = col.row(align=True)
                row.scale_y = 0.75
                row.label(text='Make sure that the mesh has no parent.', icon_value=get_emtpy_icon())
                return

            row = col.row(align=True)
            row.scale_y = 1.05
            row.prop(context.scene, 'merge_armature_into', text='Base', icon=globs.ICON_MOD_ARMATURE)
            row = col.row(align=True)
            row.scale_y = 1.05
            row.prop(context.scene, 'attach_mesh', text='Mesh', icon_value=tools.supporter.preview_collections["custom_icons"]["UP_ARROW"].icon_id)

            row = col.row(align=True)
            row.scale_y = 1.05
            row.prop(context.scene, 'attach_to_bone', text='Attach to', icon='BONE_DATA')

            row = col.row(align=True)
            row.scale_y = 1.2
            row.operator('armature_custom.attach_mesh', icon='ARMATURE_DATA')
