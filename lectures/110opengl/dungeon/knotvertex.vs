
#version 330
// Uniforms:
uniform mat4 mMatrix;
uniform mat4 vMatrix;
uniform mat4 pMatrix;
// Ins:
in vec4 position;
in vec4 normal;
in vec2 texcoord;
// Outs:
out vec4 fragmentPosition;
out vec4 fragmentTexposition;
out vec4 fragmentNormal;
out vec4 fragmentUpVector;
out vec2 fragmentTexcoord;
out vec4 eyeVector;

void main()
{
    vec4 upVector = vec4(0.0, 1.0, 0.0, 0.0);
    mat4 mvMatrix = vMatrix * mMatrix;
    fragmentNormal = mvMatrix * normal;
    fragmentUpVector = mvMatrix * upVector;
    fragmentTexcoord = texcoord;
    fragmentTexposition = mMatrix * position;
    fragmentPosition = vMatrix * fragmentTexposition;
    eyeVector = -vec4(fragmentPosition.xyz, 0.0);
    gl_Position = pMatrix * fragmentPosition;   
}
