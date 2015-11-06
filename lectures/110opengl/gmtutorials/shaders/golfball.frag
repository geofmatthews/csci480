#version 330
uniform vec2 scaleuv;
uniform vec4 color;
in vec4 fragnormal, fragtangent, fragbinormal, 
  fragreflect, fraglight, frageye;
in vec2 fraguv;
out vec4 outputColor;
void main()
{

  vec4 light, reflect, normal, tangent, binormal, eye;
  // need to normalize interpolated vectors
  light = normalize(fraglight);
  reflect = normalize(fragreflect);
  normal = normalize(fragnormal);
  tangent = normalize(fragtangent);
  binormal = normalize(fragbinormal);

  vec2 texcoords = scaleuv * fraguv;
  vec2 texfrac = (texcoords - floor(texcoords)) - vec2(0.5,0.5);
  float x = texfrac.s;
  float y = texfrac.t;
  float r = sqrt(x*x + y*y);
  if (r < 0.35) {
    normal = normalize(normal + -x*tangent + -y*binormal);
  }

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
