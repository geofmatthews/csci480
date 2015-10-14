#version 330 core

// Input vertex buffer data
// Each execution of this shader gets one vertex from the buffer
in vec4 positionBuffer;
in vec4 normalBuffer;

// Uniforms
// All executions of this shader get the same value for these
uniform mat4 M; // model
uniform mat4 V; // view
uniform mat4 P; // projection
uniform vec4 lightDirection;

// Values interpolated for fragment shader
out vec4 normal;
out vec4 light;

void main(){
    light = V * lightDirection;
    normal =  V * M * normalBuffer;
    gl_Position = P * V * M * positionBuffer;
}

