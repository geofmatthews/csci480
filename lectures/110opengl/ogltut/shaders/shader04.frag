#version 330 core

// Interpolated values from vertex shader
in vec4 normal;
in vec4 light;
in vec4 eye;

// Ouput data
out vec4 color;

void main()
{
    vec4 basecolor = vec4(1,0,0,1);
    float ambient = 0.2;
    // need to normalize interpolated vectors
    vec4 l = normalize(light);
    vec4 n = normalize(normal);
    vec4 e = normalize(eye);
    float diffuse = clamp(dot(l,n),0,1);
    float intensity = max(ambient, diffuse);
    color = basecolor * intensity;

    if (diffuse > 0.0) {
        float specular = pow(clamp(dot(reflect(-l,n),e),0,1), 16);
        color += vec4(specular,specular,specular,1);
    }
    color = clamp(color,0,1);
}
