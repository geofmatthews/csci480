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

int integerNoise(in int n)
{
    n = (n << 13) ^ n;
    return (n * (n*n*15731+789221) + 1376312589) & 0x7fffffff;
}

float cellnoise(vec4 position)
// Returns float in range 0..1
{
    // There are frequently artifacts around the origin,
    // so we offset before doing our noise.
    position += vec4(100,100,100,0);
    int n = integerNoise(int(position.x));
    n = integerNoise(n + int(position.y));
    n = integerNoise(n + int(position.z));
    return float(n % 1000000)/1000000.0;
}


void voronoi_f1f2_3d(vec4 p, float jitter,
                     out float f1, out vec4 pos1,
                     out float f2, out vec4 pos2)
// Following implementation in _Advanced Renderman_,
// Apodaca and Gritz
{
    vec4 thiscell = vec4(floor(p.x)+0.5,
                         floor(p.y)+0.5,
                         floor(p.z)+0.5, 1.0);
    f1 = 10000.0;
    f2 = 10000.0;
    float i,j,k;
    for (i = -1; i <= 1; i += 1) {
        for (j = -1; j <= 1; j += 1) {
            for (k = -1; k <= 1; k += 1) {
                vec4 testcell = thiscell + vec4(i,j,k,0);
                vec4 pos = testcell +
                           jitter * (cellnoise(testcell) - 0.5);
                vec4 offset = pos - p;
                float dist = dot(offset, offset);
                if (dist < f1) {
                    f2 = f1;
                    pos1 = pos1;
                    f1 = dist;
                    pos1 = pos;
                } else if (dist < f2) {
                    f2 = dist;
                    pos2 = pos;
                }
            }
        }
    }
    f1 = sqrt(f1);
    f2 = sqrt(f2);
}

void main()
{
    vec4 pos;
    if (whichSpace == 0) {
        pos = position;
    } else {
        pos = positionWorld;
    }

    vec4 pos1, pos2;
    float f1, f2;
    float jitter = 0.2;
    float blockscale = 5.0;
    voronoi_f1f2_3d(pos*blockscale, jitter, f1, pos1, f2, pos2);
    float scalefactor = distance(pos1,pos2)/(distance(pos1,pos)+distance(pos,pos2));

    vec4 basecolor = 0.9*vec4(.8,.9,1,1);
    basecolor = smoothstep(0.05*scalefactor, 0.2*scalefactor, f2-f1)*basecolor;
    
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
