#version 330
// Uniforms
uniform sampler2D colorTexture;
uniform sampler2D normalTexture;

// Interpolated values from vertex shader
in vec4 normal;
in vec4 tangent;
in vec4 bitangent;
in vec4 light;
in vec4 eye;
in vec2 uv;

// Ouput data
out vec4 color;

void main()
{
    vec4 basecolor = texture2D(colorTexture, uv*2);
    vec4 normalmap = texture2D(normalTexture, uv*2);
    // scale normalmap to +- 1
    normalmap = 2.0*normalmap - 1.0;
    
    // need to normalize interpolated vectors
    vec4 l = normalize(light);
    vec4 n = normalize(normal);
    vec4 e = normalize(eye);
    vec4 t = normalize(tangent);
    vec4 b = normalize(bitangent);
    // perturb normal with normalmap
    n = normalize(normalmap.r*t + normalmap.g*b + normalmap.b*n);
    
    float ambient = 0.1;
    float diffuse = clamp(dot(l,n),0,1);
    float intensity = max(ambient, diffuse);
    color = basecolor * intensity;

    if (diffuse > 0.0) {
        float specular = pow(clamp(dot(reflect(-l,n), e),0,1), 16);
        color += 0.5*vec4(specular,specular,specular,1);
    }
    color = clamp(color,0,1);
    
}
