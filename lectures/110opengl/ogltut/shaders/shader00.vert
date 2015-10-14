#version 330 core

// Input vertex buffer data
// Each execution of this shader gets one vertex from the buffer
in vec4 positionBuffer;

void main(){
    gl_Position = positionBuffer;
}

