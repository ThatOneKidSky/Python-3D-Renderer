#version 330 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 normal;

void main() {
    normal = aNormal;
    
    gl_Position = projection * view * model * vec4(aPosition, 1.0);
}