
#version 330

// Uniforms:
uniform vec4 light;
uniform int whichTexture;

// Ins:
in vec4 fragmentNormal;
in vec4 fragmentPosition;
in vec2 fragmentTexcoord;
in vec4 eye;

// Color:
out vec4 outputColor;

void main()
{
    vec4 lightVector;
    vec4 eyeVector, reflectVector;
    vec4 normalVector;
    float intensity, specular, lambert;
    
    lightVector = normalize(light - fragmentPosition);
    normalVector = normalize(fragmentNormal);
    lambert = dot(fragmentNormal, lightVector);
    intensity = max(0.25, lambert);    
    if (whichTexture == 0) {
        outputColor = vec4(1.0, 0.0, 0.0, 1.0)*intensity;
    }
    else {
        outputColor = vec4(0.0, 0.0, 1.0, 1.0)*intensity;
    }
    if (lambert > 0.0) {
        eyeVector = normalize(eye);
        reflectVector = reflect(-lightVector, normalVector);
        specular = pow(max(dot(reflectVector, eyeVector), 0.0),
                       32);
        outputColor += vec4(specular,specular,specular,1.0);
    }
}
