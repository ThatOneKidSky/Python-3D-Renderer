#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec4 color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec4 fragColor;

void main() {
    gl_Position = model * view * proj * vec4(position, 1.0);
    fragColor = vec4(1, 1, 1, 1);
}