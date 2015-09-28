
#version 330

// Attributes:
in vec4 position;
in vec4 normal;
in vec2 texcoord;

// Uniforms:
uniform mat4 mvMatrix;
uniform mat4 pMatrix;

// Outs:
out vec4 fragmentPosition;
out vec4 fragmentNormal;
out vec2 fragmentTexcoord;
out vec4 eye;

void main()
{
    fragmentNormal = mvMatrix * normal;
    fragmentTexcoord = texcoord;
    fragmentPosition = mvMatrix * position;
    eye = -vec4(fragmentPosition.xyz, 0.0);
    gl_Position = pMatrix * fragmentPosition;   
}
