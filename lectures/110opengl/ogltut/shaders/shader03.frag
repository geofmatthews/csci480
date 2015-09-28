#version 330 core

// Interpolated values from vertex shader
in vec4 normal;
in vec4 light;

// Ouput data
out vec4 color;

void main()
{
    float ambient = 0.2;
    // need to normalize interpolated vectors
    vec4 l = normalize(light);
    vec4 n = normalize(normal);    
    float diffuse = clamp(dot(l,n),0,1);
    float intensity = max(ambient, diffuse);
    color = vec4(1,0,0,1) * intensity;
}
