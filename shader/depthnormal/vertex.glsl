#version 330 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 depth;
out vec3 normal;

void main() {
    vec4 pos = projection * view * model * vec4(aPosition, 1.0);
    depth = vec3(pos.z,pos.z,pos.z);
    normal = aNormal;
    
    gl_Position = pos;
}