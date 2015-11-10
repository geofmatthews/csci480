#version 330
uniform vec2 scaleuv;
uniform vec4 color;
uniform vec4 light;
in vec4 fragnormal, fragtangent, fragbitangent, 
  fragreflect, frageye;
in vec2 fraguv;
out vec4 outputColor;

vec4 phong(vec4 color, vec4 normal, vec4 eye, vec4 reflect, vec4 light) {
  float ambient = 0.2;
  float diffuse = 0.8*clamp(dot(light, normal), 0.0, 1.0);
  vec4 phongColor = (ambient + diffuse) * color;
  if (diffuse > 0.0) {
    float specular = 0.5*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
    phongColor += vec4(specular, specular, specular, 1.0);
  }
  return clamp(phongColor, 0.0, 1.0);
}  

void main()
{
  vec4 normal = normalize(fragnormal);
  vec4 tangent = normalize(fragtangent);
  vec4 bitangent = normalize(fragbitangent);
  vec4 reflect = normalize(reflect(-light,normal));
  vec4 eye = normalize(frageye);

  vec2 texcoords = scaleuv * fraguv;
  vec2 texfrac = (texcoords - floor(texcoords)) - vec2(0.5,0.5);
  float x = texfrac.s;
  float y = texfrac.t;
  float r = sqrt(x*x + y*y);
  if (r < 0.35) {
    normal = normalize(normal + -x*tangent + -y*bitangent);
  }
  outputColor = phong(color, normal, eye, reflect, light);
}
