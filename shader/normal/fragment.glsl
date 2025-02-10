#version 330 core

in vec3 fragColor;

out vec4 color;

void main() {
    float gNorm = max(max(abs(fragColor.x), abs(fragColor.y)), abs(fragColor.z));

    if (gNorm == abs(fragColor.x)) {
        color = vec4(1.0, 0.0, 0.0, 1.0);
    } else if (gNorm == abs(fragColor.y)) {
        color = vec4(0.0, 1.0, 0.0, 1.0);
    } else {
        color = vec4(0.0, 0.0, 1.0, 1.0);
    }
}