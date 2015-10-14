#version 330
// Uniforms
uniform int whichRibs;

// Interpolated values from vertex shader
in vec4 normal;
in vec4 tangent;
in vec4 bitangent;
in vec4 light;
in vec4 eye;
in vec2 uv;

// Ouput data
out vec4 color;

vec4 bands(vec2 uv, vec4 n, vec4 t, vec4 b) {
    float pi = 3.14159265;
    float angle = pi*(fract(uv.x)*0.2 - 0.4);
    float s = sin(angle);
    float c = cos(angle);
    return normalize(c*n + s*t);
}

vec4 ribs(vec2 uv, vec4 n, vec4 t, vec4 b) {
    float pi = 3.14159265;
    float angle = pi*(fract(uv.y)*0.2 - 0.4);
    float s = sin(angle);
    float c = cos(angle);
    return normalize(c*n + s*b);
}

void main()
{
    vec4 basecolor = vec4(1,0,0,1);
    float ambient = 0.1;
    // need to normalize interpolated vectors
    vec4 l = normalize(light);
    vec4 n = normalize(normal);
    vec4 e = normalize(eye);
    vec4 t = normalize(tangent);
    vec4 b = normalize(bitangent);

    if (whichRibs == 0) {
        n = ribs(uv*30.0, n, t, b);
    } else {
        n = bands(uv*60.0, n, t, b);
    }
    
    float diffuse = clamp(dot(l,n),0,1);
    float intensity = max(ambient, diffuse);
    color = basecolor * intensity;

    if (diffuse > 0.0) {
        float specular = pow(clamp(dot(reflect(-l,n), e),0,1), 16);
        color += vec4(specular,specular,specular,1);
    }
    color = clamp(color,0,1);
    
}
