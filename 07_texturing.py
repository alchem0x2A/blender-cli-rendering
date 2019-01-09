# blender --background --python 07_texturing.py -- </path/to/output/image> <resolution_percentage> <num_samples>

import bpy
import sys
import math
import os

sys.path.append(os.getcwd())

import utils

def set_scene_objects():
	bpy.ops.mesh.primitive_monkey_add(location=(- 1.8, 0.0, 1.0), rotation=(0.0, 0.0, - math.pi * 60.0 / 180.0), calc_uvs=True)
	current_object = bpy.context.object
	current_object.name = "Suzanne_Left"
	utils.add_subdivision_surface_modifier(current_object, 4)
	mat = bpy.data.materials.new("Material_Left")
	mat.use_nodes = True
	utils.clean_nodes(mat.node_tree.nodes)
	utils.build_pbr_textured_nodes(
		mat.node_tree, 
		color_texture_path="./assets/textures/[2K]Leather05/Leather05_col.jpg", 
		roughness_texture_path="./assets/textures/[2K]Leather05/Leather05_rgh.jpg", 
		normal_texture_path="./assets/textures/[2K]Leather05/Leather05_nrm.jpg", 
		displacement_texture_path="./assets/textures/[2K]Leather05/Leather05_disp.jpg"
	)
	current_object.data.materials.append(mat)

	bpy.ops.mesh.primitive_monkey_add(location=(0.0, 0.0, 1.0), rotation=(0.0, 0.0, - math.pi * 60.0 / 180.0), calc_uvs=True)
	current_object = bpy.context.object
	current_object.name = "Suzanne_Center"
	utils.add_subdivision_surface_modifier(current_object, 4)
	mat = bpy.data.materials.new("Material_Center")
	mat.use_nodes = True
	utils.clean_nodes(mat.node_tree.nodes)
	utils.build_pbr_textured_nodes(
		mat.node_tree, 
		color_texture_path="./assets/textures/[2K]Metal07/Metal07_col.jpg", 
		metallic_texture_path="./assets/textures/[2K]Metal07/Metal07_met.jpg", 
		roughness_texture_path="./assets/textures/[2K]Metal07/Metal07_rgh.jpg", 
		normal_texture_path="./assets/textures/[2K]Metal07/Metal07_nrm.jpg", 
		displacement_texture_path="./assets/textures/[2K]Metal07/Metal07_disp.jpg"
	)
	current_object.data.materials.append(mat)

	bpy.ops.mesh.primitive_monkey_add(location=(+ 1.8, 0.0, 1.0), rotation=(0.0, 0.0, - math.pi * 60.0 / 180.0), calc_uvs=True)
	current_object = bpy.context.object
	current_object.name = "Suzanne_Right"
	utils.add_subdivision_surface_modifier(current_object, 4)
	mat = bpy.data.materials.new("Material_Right")
	mat.use_nodes = True
	utils.clean_nodes(mat.node_tree.nodes)
	utils.build_pbr_textured_nodes(
		mat.node_tree,
		color_texture_path="./assets/textures/[2K]Fabric02/fabric02_col.jpg",
		roughness_texture_path="./assets/textures/[2K]Fabric02/fabric02_rgh.jpg",
		normal_texture_path="./assets/textures/[2K]Fabric02/fabric02_nrm.jpg",
		displacement_texture_path="./assets/textures/[2K]Fabric02/fabric02_disp.jpg"
	)
	current_object.data.materials.append(mat)

	bpy.ops.mesh.primitive_plane_add(radius=6.0, calc_uvs=True)
	current_object = bpy.context.object
	current_object.name = "Floor"
	mat = bpy.data.materials.new("Material_Plane")
	mat.use_nodes = True
	utils.clean_nodes(mat.node_tree.nodes)
	utils.build_pbr_textured_nodes(
		mat.node_tree,
		color_texture_path="./assets/textures/[2K]Marble01/Marble01_col.jpg",
		roughness_texture_path="./assets/textures/[2K]Marble01/Marble01_rgh.jpg",
		normal_texture_path="./assets/textures/[2K]Marble01/Marble01_nrm.jpg",
		displacement_texture_path="./assets/textures/[2K]Marble01/Marble01_disp.jpg"
	)
	current_object.data.materials.append(mat)

	bpy.ops.mesh.primitive_plane_add(radius=6.0, location=(0.0, 4.0, 0.0), rotation=(math.pi * 90.0 / 180.0, 0.0, 0.0), calc_uvs=True)
	current_object = bpy.context.object
	current_object.name = "Wall"
	mat = bpy.data.materials.new("Material_Plane")
	mat.use_nodes = True
	utils.clean_nodes(mat.node_tree.nodes)
	utils.build_pbr_textured_nodes(
		mat.node_tree,
		color_texture_path="./assets/textures/[2K]Marble01/Marble01_col.jpg",
		roughness_texture_path="./assets/textures/[2K]Marble01/Marble01_rgh.jpg",
		normal_texture_path="./assets/textures/[2K]Marble01/Marble01_nrm.jpg",
		displacement_texture_path="./assets/textures/[2K]Marble01/Marble01_disp.jpg"
	)
	current_object.data.materials.append(mat)

	bpy.ops.object.empty_add(location=(0.0, -0.70, 1.0))
	focus_target = bpy.context.object
	return focus_target

def set_camera_params(camera, dof_target):
	camera.data.sensor_fit = 'HORIZONTAL'
	camera.data.sensor_width = 36.0
	camera.data.sensor_height = 24.0
	camera.data.lens = 72
	camera.data.dof_object = dof_target
	camera.data.cycles.aperture_type = 'RADIUS'
	camera.data.cycles.aperture_size = 0.100
	camera.data.cycles.aperture_blades = 6

# Args
output_file_path = str(sys.argv[sys.argv.index('--') + 1])
resolution_percentage = int(sys.argv[sys.argv.index('--') + 2])
num_samples = int(sys.argv[sys.argv.index('--') + 3])

# Parameters
hdri_path = "./assets/HDRIs/green_point_park_2k.hdr"

# Scene Building
scene = bpy.data.scenes["Scene"]
world = scene.world

## Reset
utils.clean_objects()

## Suzannes
focus_target = set_scene_objects()

## Camera
bpy.ops.object.camera_add(view_align=False, location=[0.0, - 14.0, 2.0])
camera = bpy.context.object

utils.add_track_to_constraint(camera, focus_target)
set_camera_params(camera, focus_target)

## Lights
utils.build_environmental_light(world, hdri_path)

## Composition
utils.build_scene_composition(scene)

# Render Setting
utils.set_cycles_renderer(scene, resolution_percentage, output_file_path, camera, num_samples, use_denoising=True)

# Render
bpy.ops.render.render(animation=False, write_still=True)