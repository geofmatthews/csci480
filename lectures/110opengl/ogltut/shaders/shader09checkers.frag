#version 330
// Uniforms
uniform int whichSpace;

// Interpolated values from vertex shader
in vec4 position;
in vec4 positionWorld;
in vec4 positionCamera;
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
    vec4 pos;
    if (whichSpace == 0) {
        pos = position;
    } else if (whichSpace == 1) {
        pos = positionWorld;
    } else {
        pos = positionCamera;
    }
    ivec4 intpos = ivec4(floor(4*pos));
    int oddeven = int(mod(intpos.x+intpos.y+intpos.z,2));
    vec4 basecolor;
    if (oddeven==0) {
        basecolor = vec4(1,0,0,1);
    } else {
        basecolor = vec4(1,1,1,1);
    }
    
    // need to normalize interpolated vectors
    vec4 l = normalize(light);
    vec4 n = normalize(normal);
    vec4 e = normalize(eye);
    vec4 t = normalize(tangent);
    vec4 b = normalize(bitangent);
    
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
