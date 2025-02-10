#version 330 core

in vec3 normal;
in vec3 depth;

out vec4 color;

void main() {
    float gNorm = max(max(abs(normal.x), abs(normal.y)), abs(normal.z));

    if (gNorm == abs(normal.x)) {
        color = vec4(depth.x/400,0,0, 1.0);
    } else if (gNorm == abs(normal.y)) {
        color = vec4(0,depth.x/400,0, 1.0);
    } else {
        color = vec4(0,0,depth.x/400, 1.0);
    }
}