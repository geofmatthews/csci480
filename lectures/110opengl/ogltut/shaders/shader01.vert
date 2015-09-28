#version 330 core

// Input vertex buffer data
// Each execution of this shader gets one vertex from the buffer
in vec4 positionBuffer;

// Uniforms
// All executions of this shader get the same value for these
uniform mat4 M; // model
uniform mat4 V; // view
uniform mat4 P; // projection

void main(){
    gl_Position = P * V * M * positionBuffer;
}

