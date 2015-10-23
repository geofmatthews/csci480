
#version 330
//Uniforms:
uniform float useKnot;
uniform float fogEnd;
// Ins:
in vec4 fragmentNormal;
in vec4 fragmentUpVector;
in vec4 fragmentPosition;
in vec4 fragmentTexposition;
in vec2 fragmentTexcoord;
in vec4 eyeVector;
// Outs:
out vec4 outputColor;

// Code for marble noise:
float cosineInterpolate(float a, float b, float x)
{
  float f = (1.0 - cos(x*3.14159265))*0.5;
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
  float v1 = cosineInterpolate(v011, v111, fracX);
  float v2 = cosineInterpolate(v001, v101, fracX);
  float v5 = cosineInterpolate(v2,v1,fracY);
  float v3 = cosineInterpolate(v010,v110,fracX);
  float v4 = cosineInterpolate(v000,v100,fracX);
  float v6 = cosineInterpolate(v4,v3,fracY);
  return cosineInterpolate(v6, v5, fracZ);
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
// Code for knot:
void hash(int x, int y, out float h1, out float h2)
{
    x = x % 16; // so it wraps on my cylinders!
    y = y % 16;
  int result1 = integerNoise(x);
  result1 = integerNoise(result1+y);
  int result2 = integerNoise(result1);
  h1 = float(result1 % 1024)/1024.0;
  h2 = float(result2 % 1024)/1024.0;
  }

vec4 normFromCircle(float x, float y, float radius, vec4 side, vec4 up, vec4 oldNorm) {
  vec4 newNorm = oldNorm;
  float halfroot2 = 0.70710678;
  float len = sqrt(x*x+y*y);
  float dist = len - halfroot2;
  if (abs(dist) < radius) {
    float hdist = dist/radius;
    float vdist = sqrt(1.0 - hdist*hdist);
    vec4 outVector = normalize(x*side + y*up);
    newNorm = normalize(hdist*outVector + 1*vdist*oldNorm);
  }
  return newNorm;
}

vec4 normFromLine(float x, float y, float radius, vec4 side, vec4 up, vec4 trueNorm, vec4 defaultNorm){
      vec4 newNorm = defaultNorm;
      float cx = 0.5*(x-y+1);
      float cy = 0.5*(y-x+1);
      float dx = cx-x;
      float dy = cy-y;
      float dist = sqrt(dx*dx+dy*dy);
      if (x*x+y*y < cx*cx+cy*cy) {
        dist = -dist;
      }
      if (abs(dist) < radius) {
        vec4 outVector = normalize(side + up);
        float hdist = dist/radius;
        float vdist = sqrt(1.0 - hdist*hdist);
        newNorm = normalize(hdist*outVector + 1*vdist*trueNorm);
      }
      return newNorm;
      }

     
vec4 newNormal(vec2 texcoord, vec4 oldNormal) {
  float lineRadius = 0.33;
  vec4 upVector = vec4(0.0, 1.0, 0.0, 0.0);
  vec4 sideVector = vec4(normalize(cross(upVector.xyz, oldNormal.xyz)),0.0);
  int intX = int(texcoord.x);
  int intY = int(texcoord.y);
  float x = texcoord.x - intX;
  float y = texcoord.y - intY;
  x = 2.0*x - 1.0;
  y = 2.0*y - 1.0;
  bool A = (x > -y);
  bool B = (x > y);
  float left, up, right, down, dummy;
  hash(intX, intY, left, up);
  hash(intX+1, intY, right, dummy);
  hash(intX, intY+1, dummy, down);
  float threshold = 0.5;
  vec4 newNorm = oldNormal;
  if (A && B) {
    if (right < threshold) {
      newNorm = normFromCircle(x,y,lineRadius,sideVector,upVector,oldNormal);
    } else {
      newNorm = normFromLine(x,y,lineRadius,sideVector,upVector,oldNormal,newNorm);
      newNorm = normFromLine(x,-y,lineRadius,sideVector,-upVector,oldNormal,newNorm);
    }
  }
  else if (!A && B) {
    if (up < threshold) {
      newNorm = normFromCircle(x,y,lineRadius,sideVector,upVector,oldNormal);
    } else {
      newNorm = normFromLine(x,-y,lineRadius,sideVector,-upVector,oldNormal,newNorm);
      newNorm = normFromLine(-x,-y,lineRadius,-sideVector,-upVector,oldNormal,newNorm);
    }
  }
  else if (!A && !B) {
    if (left < threshold) {
      newNorm = normFromCircle(x,y,lineRadius,sideVector,upVector,oldNormal);
    } else {
      newNorm = normFromLine(-x,-y,lineRadius,-sideVector,-upVector,oldNormal,newNorm);
      newNorm = normFromLine(-x,y,lineRadius,-sideVector,upVector,oldNormal,newNorm);
    }
  }
  else if (A && !B) {
    if (down < threshold) {
      newNorm = normFromCircle(x,y,lineRadius,sideVector,upVector,oldNormal);
    } else {
      newNorm = normFromLine(-x,y,lineRadius,-sideVector,upVector,oldNormal,newNorm);
      newNorm = normFromLine(x,y,lineRadius,sideVector,upVector,oldNormal,newNorm);
    }
  }
  return newNorm;
}  
  
void main()
{
    vec4 light = vec4(0.0, 1.0, -1.0, 1.0);
    vec4 veinColor = vec4(0.0,0.3,0.1,1.0);
    vec4 slabColor = vec4(0.1,0.7,0.2,1.0);
    veinColor = vec4(0.0,0.0,0.0,1.0);
    //slabColor = vec4(1.0,1.0,1.0,1.0);
    vec4 lightVector;
    vec4 reflectVector;
    vec4 normalVector;
    float intensity, specular, lambert;
    
    // Find marble color:
    vec4 texPosition = fragmentTexposition;
    float noise = fbmNoise(texPosition.xyz/2.0);
    vec4 color = mix(veinColor, slabColor, noise);
    
    lightVector = normalize(light - fragmentPosition);
    normalVector = normalize(fragmentNormal);
    
    // perturb normal for knot texture:
    if (useKnot != 0.0) {
        normalVector = newNormal(fragmentTexcoord*2, normalVector);
    }
    float cameraDistance = length(fragmentPosition.xyz);
    cameraDistance = smoothstep(5.0, fogEnd, cameraDistance);
    lambert = dot(normalVector, lightVector);
    intensity = max(0.4, lambert); 
    outputColor = intensity * color;
    if (lambert > 0.0) {
        reflectVector = reflect(-lightVector, normalVector);
        specular = pow(max(dot(normalize(reflectVector), normalize(eyeVector)), 0.0),
                       55);
        outputColor += vec4(specular,specular,specular,1.0);
    }
    outputColor *= 1.0-cameraDistance;
}
