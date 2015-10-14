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

// Noise routines
float smerp(float a, float b, float x)
{
    x = x*2.0-1.0;
    float f = 0.5 + 0.75*x - 0.25*x*x*x;
    return mix(a,b,f);
}
int integerNoise(in int n)
{
    n = (n << 13) ^ n;
    return (n * (n*n*15731+789221) + 1376312589) & 0x7fffffff;
}

float noise(vec3 position)
// Returns float in range 0..1
{
  int n = integerNoise(int(position.x));
  n = integerNoise(n + int(position.y));
  n = integerNoise(n + int(position.z));
  return float(n % 1000000)/1000000.0;
}

float interpolatedNoise(in vec3 position)
{
  float x = position.x;
  float y = position.y;
  float z = position.z;
  float intX = floor(x);
  float intY = floor(y);
  float intZ = floor(z);
  float fracX = fract(x);
  float fracY = fract(y);
  float fracZ = fract(z);
  float v000 = noise(vec3(intX  , intY  , intZ  ));
  float v001 = noise(vec3(intX  , intY  , intZ+1));
  float v010 = noise(vec3(intX  , intY+1, intZ  ));
  float v100 = noise(vec3(intX+1, intY  , intZ  ));
  float v011 = noise(vec3(intX  , intY+1, intZ+1));
  float v110 = noise(vec3(intX+1, intY+1, intZ  ));
  float v101 = noise(vec3(intX+1, intY  , intZ+1));
  float v111 = noise(vec3(intX+1, intY+1, intZ+1));
  float v1 = smerp(v011, v111, fracX);
  float v2 = smerp(v001, v101, fracX);
  float v5 = smerp(v2,v1,fracY);
  float v3 = smerp(v010,v110,fracX);
  float v4 = smerp(v000,v100,fracX);
  float v6 = smerp(v4,v3,fracY);
  return smerp(v6, v5, fracZ);
}

float fbmNoise(in vec3 position)
{
  float total = 0.0;
  total += interpolatedNoise(position);
  total += interpolatedNoise(2.0*position)*0.5;
  total += interpolatedNoise(4.0*position)*0.25;
  total += interpolatedNoise(8.0*position)*0.125;
  total += interpolatedNoise(16.0*position)*0.0625;
  return total/1.9375;
}

void main()
{
    vec4 basecolor1 = vec4(0,.02,.01,1.0);
    vec4 basecolor2 = vec4(0,1,.5,1);
    vec4 pos;
    if (whichSpace == 0) {
        pos = position;
    } else {
        pos = positionWorld;
    }
    float noise = fbmNoise(pos.xyz*2.0);
    vec4 basecolor = mix(basecolor1, basecolor2, noise);
    
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
