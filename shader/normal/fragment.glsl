#version 330 core

in vec3 normal;

out vec4 color;

void main() {
    float gNorm = max(max(abs(normal.x), abs(normal.y)), abs(normal.z));

    if (gNorm == abs(normal.x)) {
        color = vec4(1.0, 0.0, 0.0, 1.0);
    } else if (gNorm == abs(normal.y)) {
        color = vec4(0.0, 1.0, 0.0, 1.0);
    } else {
        color = vec4(0.0, 0.0, 1.0, 1.0);
    }
}