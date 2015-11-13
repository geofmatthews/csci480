#version 330
// phong shading
uniform vec4 color;
uniform sampler2D posx, negx, posy, negy, posz, negz;
in vec4 fragnormal, fragreflect, fraglight, frageye;
out vec4 outputColor;

vec4 texColor(vec4 normal, vec4 eye) {
  // everything is in world space, so we assume
  // origin of vectors is (0,0,0), and the planes
  // for the skybox are (1,0,0), (0,1,0), etc.
  vec4 posx = vec4(1.0, 0.0, 0.0, 0.0);
  vec4 negx = -posx;
  vec4 posy = vec4(0.0, 1.0, 0.0, 0.0);
  vec4 negy = -posy;
  vec4 posz = vec4(0.0, 0.0, 1.0, 0.0);
  vec4 negz = -posz;
  // find reflected eye vector
  vec4 refl = reflect(-eye, normal);
  // Find the closest plane in front of the refl vector
  float t = 1000.0;
  vec4 
  dotposx = dot(refl, posx);
  if 


  }
  
    

void main()
{
  vec4 light, reflect, normal, eye;
  // need to normalize interpolated vectors
  light = normalize(fraglight);
  reflect = normalize(fragreflect);
  normal = normalize(fragnormal);
  eye = normalize(frageye);
  float ambient = 0.2;
  float diffuse = 0.8*clamp(dot(light, normal), 0.0, 1.0);
  outputColor = (ambient + diffuse) * color;
  if (dot(light,normal) > 0.0) {
    float specular = 0.8*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
    outputColor += vec4(specular, specular, specular, 1.0);
  }
  outputColor = clamp(outputColor, 0.0, 1.0);
}
