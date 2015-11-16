#version 330
// phong shading
uniform sampler2D posxsampler, negxsampler, posysampler,
                  negysampler, poszsampler, negzsampler;
in vec4 fragnormal, fragreflect, fraglight, frageye;
out vec4 outputColor;

vec4 texColor(vec4 normal, vec4 eye) {
  // everything is in world space, so we assume
  // origin of vectors is (0,0,0), and the planes
  // for the skybox are (1,0,0), (0,1,0), etc.
  vec4 posx = vec4(1.0, 0.0, 0.0, 0.0);
  vec4 posy = vec4(0.0, 1.0, 0.0, 0.0);
  vec4 posz = vec4(0.0, 0.0, 1.0, 0.0);
  // find reflected eye vector
  vec4 ray = reflect(-eye, normal);
  // for debugging purposes it's nice to see where the normal
  // hits the skybox:
  //ray = normal;
  // Find the closest plane in front of the ray vector
  vec4 hit;
  // X DIRECTION
  if ((abs(ray.x) > abs(ray.y)) && (abs(ray.x) > abs(ray.z))) {
    if (ray.x > 0) {
      // pos x
      hit = ray/dot(-posx, ray);
      return texture2D(posxsampler, vec2(-hit.z, -hit.y)*0.5 + vec2(0.5,0.5));
    } else {
      // neg x
      hit = ray/dot(posx, ray);
      return texture2D(negxsampler, vec2(hit.z, -hit.y)*0.5+vec2(0.5,0.5));
    }
  }
  // Y DIRECTION
  if (abs(ray.y) > abs(ray.z)) {
    if (ray.y > 0.0) {
      // pos y
      hit = ray/dot(-posy, ray);
      return texture2D(posysampler, vec2(-hit.x,-hit.z)*0.5 + vec2(0.5,0.5));
    } else {
      // neg y
      hit = ray/dot(posy, ray);
      return texture2D(negysampler, vec2(-hit.x,hit.z)*0.5 + vec2(0.5,0.5));
    }
  }
  // Z DIRECTION
  if (ray.z > 0.0) {
     // pos z
     hit = ray/dot(-posz, ray);
     return texture2D(poszsampler, vec2(hit.x,-hit.y)*0.5 + vec2(0.5,0.5));
  } else {
     // neg z
     hit = ray/dot(posz, ray);
     return texture2D(negzsampler, vec2(-hit.x,-hit.y)*0.5 + vec2(0.5,0.5));
  }
  // Did I miss something?
  return vec4(0,0,0,1.0);
}
     
void main()
{
  vec4 light, reflect, normal, eye, color;
  // need to normalize interpolated vectors
  light = normalize(fraglight);
  reflect = normalize(fragreflect);
  normal = normalize(fragnormal);
  eye = normalize(frageye);
  float ambient = 0.4;
  float diffuse = 0.6*clamp(dot(light, normal), 0.0, 1.0);
  color = texColor(normal, eye);
  outputColor = (ambient + diffuse) * color;
  if (dot(light,normal) > 0.0) {
    float specular = 0.4*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
    outputColor += vec4(specular, specular, specular, 1.0);
  }
  outputColor = clamp(outputColor, 0.0, 1.0);
}
