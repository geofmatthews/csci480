#version 330
// toon shading
uniform vec4 color;
in vec4 fragnormal, fragreflect, fraglight, frageye;
out vec4 outputColor;
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
  diffuse = diffuse * 4;
  diffuse = trunc(diffuse);
  diffuse = diffuse/4.0;
  outputColor = (ambient + diffuse) * color;
  if (dot(light,normal) > 10.0) {
    float specular = 0.8*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
    outputColor += vec4(specular, specular, specular, 1.0);
  }
  outputColor = clamp(outputColor, 0.0, 1.0);
}
