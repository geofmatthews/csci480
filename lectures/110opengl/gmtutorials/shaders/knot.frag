#version 330
// Use with bumpmap.vert
//Uniforms:
uniform int useKnot;
uniform vec2 scaleuv;

// Ins:
in vec2 fraguv;
in vec4 fragnormal;
in vec4 fragtangent;
in vec4 fragbinormal;
in vec4 fragposition;
in vec4 frageye;
in vec4 fraglight;
// Outs:
out vec4 outputColor;

// Code for knot:

int integerNoise(in int n)
{
  n = (n << 13) ^ n;
  return (n * (n*n*15731+789221) + 1376312589) & 0x7fffffff;
}

void hash(int x, int y, out float h1, out float h2)
{
  x = x % 8; // so it wraps on cylinders!
  y = y % 8;
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

vec4 newNormal(vec2 texcoord, vec4 oldNormal, vec4 binorm, vec4 tan) {
  float lineRadius = 0.33;
  vec4 upVector = tan;
  vec4 sideVector = binorm;
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
  vec4 light = normalize(fraglight);
  vec4 veinColor = vec4(0.0,0.3,0.1,1.0);
  vec4 slabColor = vec4(0.1,0.7,0.2,1.0);
  veinColor = vec4(0.0,0.0,0.0,1.0);
  //slabColor = vec4(1.0,1.0,1.0,1.0);
  vec4 lightVector;
  vec4 reflectVector;
  vec4 normalVector, tangentVector, binormalVector, eyeVector;
  float intensity, specular, lambert;
  
  vec4 color = vec4(0.0, 1.0, 0.0, 1.0);
  
  lightVector = normalize(light - fragposition);
  normalVector = normalize(fragnormal);
  tangentVector = normalize(fragtangent);
  binormalVector = normalize(fragbinormal);
  
  // perturb normal for knot texture:
  if (useKnot == 0) {
    normalVector = newNormal(fraguv*scaleuv, normalVector, tangentVector, binormalVector);
  }
  float ambient = 0.2;
  float diffuse = 0.8*clamp(dot(lightVector, normalVector), 0.0, 1.0);
  outputColor = (ambient + diffuse) * color;
  if (diffuse > 0.0) {
    float specular = 0.8*pow(clamp(dot(reflectVector, eyeVector), 0.0, 1.0), 8);
    outputColor += vec4(specular, specular, specular, 1.0);
  }
  outputColor = clamp(outputColor, 0.0, 1.0);
}
