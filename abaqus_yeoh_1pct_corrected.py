# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2022 replay file
# Internal Version: 2021_09_15-13.57.30 176069
# Run by austa on Thu Oct 24 18:39:42 2024

prx=99.900000
r=142#this is the radius of the tumor

pr=prx%100
r=r+prx//100
jobname='Job-{}'.format(int(prx*10))
output_path = '{}node_displacements{}.txt'.format(r,pr)
# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=147.885177612305, 
    height=123.589408874512)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=5000.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3080.35, 
    farPlane=6347.74, width=32248.3, height=9577.41, cameraPosition=(4167.78, 
    -2831.48, 4714.05), cameraTarget=(4167.78, -2831.48, 0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=2976.07, 
    farPlane=6452.02, cameraUpVector=(-0.0342617, 0.999413, 0))
session.viewports['Viewport: 1'].view.setValues(cameraUpVector=(-0.001985, 
    0.999998, 0))
s.rectangle(point1=(0.0, 0.0), point2=(275.0, 125.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=4311.5, 
    farPlane=5116.59, width=6348.86, height=1885.55, cameraPosition=(553.514, 
    181.486, 4714.05), cameraTarget=(553.514, 181.486, 0))
s.undo()
s.rectangle(point1=(-1300.0, 1000.0), point2=(0.0, -400.0))
s.ObliqueDimension(vertex1=v[3], vertex2=v[0], textPoint=(-611.788818359375, 
    813.78369140625), value=2000.0)
s.ObliqueDimension(vertex1=v[2], vertex2=v[3], textPoint=(162.615509033203, 
    321.734832763672), value=2500.0)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3883.13, 
    farPlane=5544.96, width=16401.9, height=4871.19, cameraPosition=(678.097, 
    -211.503, 4714.05), cameraTarget=(678.097, -211.503, 0))
s.CircleByCenterPerimeter(center=(0.0, 2100.0), point1=(0.0, 1850.0))
s.CoincidentConstraint(entity1=v[4], entity2=g[4], addUndoState=False)
s.RadialDimension(curve=g[6], textPoint=(398.221862792969, 1825.48095703125), 
    radius=r)
s.autoTrimCurve(curve1=g[6], point1=(115.39501953125, 1959.85583496094))
s.autoTrimCurve(curve1=g[5], point1=(-73.2588500976562, 2101.16455078125))
s.autoTrimCurve(curve1=g[4], point1=(7.67376708984375, 2000.12316894531))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].view.setValues(nearPlane=5941.01, 
    farPlane=6865.24, width=9076.24, height=2591.01, viewOffsetX=-38.0519, 
    viewOffsetY=-80.2202)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
#mdb.models['Model-1'].Material(name='Material-1')
#mdb.models['Model-1'].materials['Material-1'].Elastic(table=((6150.0, 0.49), ))
#mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', material='Material-1', thickness=None)
mdb.models['Model-1'].Material(name='Material-1')
# Yeoh hyperelastic parameters for 1% agarose hydrogel (E = 6150 Pa, nu = 0.49)
# C10 = E/6, C20 = -0.1*C10, C30 = 0.01*C10 (SimLet, 2026, WELSIM)
# D1 = 6*(1-2*nu)/E  [near-incompressible volumetric relation]
# C10=1025.0, C20=-102.5, C30=10.25, D1=1.9512195121951235e-05
mdb.models['Model-1'].materials['Material-1'].Hyperelastic(
    type=YEOH,
    testData=OFF,
    volumetricResponse=VOLUMETRIC_DATA,   # use D-parameters (compressible)
    moduliTimeScale=LONG_TERM,            # 48 h → equilibrium response
    table=((1025.0, -102.5, 10.25, 1.9512195121951235e-05, 0.0, 0.0), )
)
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', material='Material-1', thickness=None)

p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(faces=faces, name='all')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
#edit
#mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', nlgeom=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p1 = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
p.Set(edges=edges, name='top')
#: The set 'top' has been created (1 edge).
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#10 ]', ), )
p.Set(edges=edges, name='c')
#: The set 'c' has been created (1 edge).
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#2 ]', ), )
p.Set(edges=edges, name='left')
#: The set 'left' has been created (1 edge).
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#8 ]', ), )
p.Set(edges=edges, name='right')
#: The set 'right' has been created (1 edge).
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#4 ]', ), )
p.Set(edges=edges, name='bottom')
#: The set 'bottom' has been created (1 edge).
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].edges
side1Edges1 = s1.getSequenceFromMask(mask=('[#10 ]', ), )
region = a.Surface(side1Edges=side1Edges1, name='Surf-1')


mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude= pr, amplitude=UNSET)



a = mdb.models['Model-1'].rootAssembly
region = a.instances['Part-1-1'].sets['bottom']
mdb.models['Model-1'].YsymmBC(name='BC-1', createStepName='Step-1', 
    region=region, localCsys=None)
a = mdb.models['Model-1'].rootAssembly
region = a.instances['Part-1-1'].sets['right']
mdb.models['Model-1'].XsymmBC(name='BC-2', createStepName='Step-1', 
    region=region, localCsys=None)
a = mdb.models['Model-1'].rootAssembly
region = a.instances['Part-1-1'].sets['top']
mdb.models['Model-1'].YsymmBC(name='BC-3', createStepName='Step-1', 
    region=region, localCsys=None)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
v1 = a.instances['Part-1-1'].vertices
verts1 = v1.getSequenceFromMask(mask=('[#8 ]', ), )
region = a.Set(vertices=verts1, name='Set-1')
mdb.models['Model-1'].EncastreBC(name='BC-4', createStepName='Step-1', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
    bcs=OFF, predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Part-1-1'].edges
pickedEdges = e1.getSequenceFromMask(mask=('[#10 ]', ), )
a.seedEdgeBySize(edges=pickedEdges, size=50.0, deviationFactor=0.1, 
    constraint=FINER)
a = mdb.models['Model-1'].rootAssembly
partInstances =(a.instances['Part-1-1'], )


a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
pickedRegions = f1.getSequenceFromMask(mask=('[#1 ]', ), )
a.deleteMesh(regions=pickedRegions)
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Part-1-1'].edges
pickedEdges = e1.getSequenceFromMask(mask=('[#10 ]', ), )
a.seedEdgeBySize(edges=pickedEdges, size=50.0, deviationFactor=0.1, 
    constraint=FINER)
a = mdb.models['Model-1'].rootAssembly
partInstances =(a.instances['Part-1-1'], )
a.generateMesh(regions=partInstances)
session.viewports['Viewport: 1'].view.setValues(nearPlane=5855.89, 
    farPlane=6950.35, width=9579.53, height=2739.18, viewOffsetX=-123.129, 
    viewOffsetY=-157.795)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.Job(name=jobname, model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
    multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
mdb.jobs[jobname].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Job Job-1: Abaqus/Standard completed successfully.
#: Job Job-1 completed successfully. 
o3 = session.openOdb(name='c:/temp/{}.odb'.format(jobname))
#: Model: d:/temp/Job-1.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       7
#: Number of Node Sets:          8
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    spectrum='Blue to red')
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))

#code for extract the top node coords and disps
import sys
print(sys.version)
print(sys.path)
from odbAccess import *
import numpy as np

# Open the ODB file
odb_path = r"c:\temp\{}.odb".format(jobname) # Replace with your actual ODB file path
odb = openOdb(path=odb_path)

# Access the last step (or modify to access the specific step you're interested in)
last_step = odb.steps['Step-1']

# Access the displacement field output
disp_field = last_step.frames[-1].fieldOutputs['U']

# Get the instance and node set for 'top'
top_set = odb.rootAssembly.instances['PART-1-1'].nodeSets['TOP']

# Extract the node coordinates and displacements
node_data = []
disp_subset = disp_field.getSubset(region=top_set)

# Loop over the nodes in the node set
for node in top_set.nodes:
    node_label = node.label
    coords = node.coordinates

    # Find the corresponding displacement value by node label
    for disp in disp_subset.values:
        if disp.nodeLabel == node_label:
            print(disp.data)
            print(coords)
            # Append node label, coordinates, and displacements (X, Y, Z)
            node_data.append([node_label, coords[0], coords[1], disp.data[0], disp.data[1]])
            break  # Exit the loop once the displacement is found for the node

# Write the node data to a text file as a substitute for Excel output in Python 2.7
  # Replace with your desired output path

with open(output_path, 'w') as f:
    # Write the header
    f.write('radius:'+str(r)+'\n')
    f.write('p:'+str(pr)+'\n')
    f.write('Node Label\tX\tY\tU1\tU2\n')
    
    
    # Write the node data
    for node in node_data:
        f.write('{}\t{}\t{}\t{}\t{}\n'.format(
            node[0], node[1], node[2]-node[2], node[3], node[4]
        ))

# Close the ODB file
odb.close()

print('Data extracted and saved to {}'.format(output_path))













