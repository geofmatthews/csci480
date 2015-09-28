#version 330 core

// Input vertex buffer data
// Each execution of this shader gets one vertex from the buffer
in vec2 uvBuffer;
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
out vec4 eye;
out vec2 uv;

void main(){
    uv = uvBuffer;
    light = V * lightDirection;
    normal =  V * M * normalBuffer;
    eye = -(V * M * positionBuffer);
    // opengl magic variable gl_InstanceID
    vec4 position = M * positionBuffer;
    position.x += 2*(gl_InstanceID - 2);
    gl_Position = P * V *  position;
}

