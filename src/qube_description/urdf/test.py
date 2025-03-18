import re

# Import variables from test.py
box_width = "0.21"
angle_link_length = "0.15"
angle_link_width = "0.003"


# Read the template
with open("qube_template.xacro", "r") as f:
    xacro_content = f.read()

# Replace placeholders with actual values
xacro_content = re.sub(r"\$\{box_width\}", str(box_width), xacro_content)
xacro_content = re.sub(r"\$\{angle_link_length\}", str(angle_link_length), xacro_content)
xacro_content = re.sub(r"\$\{angle_link_width\}", str(angle_link_width), xacro_content)  # Example modification

# Write the new Xacro file
with open("qube_generated.xacro", "w") as f:
    f.write(xacro_content)

print("Generated qube_generated.xacro successfully!")






# <?xml version="1.0"?>

# <robot name="qube" xmlns:xacro="http://www.ros.org/wiki/xacro">
#   <xacro:include filename="$(find qube_description)/urdf/qube.macro.xacro"/>

#   <xacro:property name="box_width" value="${box_width}"/>
#   <xacro:property name="angle_link_length" value="${angle_link_length}"/>
#   <xacro:property name="angle_link_width" value="${angle_link_width}"/>

#   <link name="world"/>
#   <link name="base_link"/>

#   <joint name="base_joint" type="fixed">
#     <parent link="world"/>
#     <child link="base_link"/>
#     <origin xyz="0 0 0" rpy="0 0 0"/>
#   </joint>

#   <xacro:joint_model prefix=""/>
# </robot>
