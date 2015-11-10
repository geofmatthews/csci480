
vec4 phong(vec4 color, vec4 normal, vec4 eye, vec4 reflect, vec4 light) {
  float ambient = 0.2;
  float diffuse = 0.8*clamp(dot(light, normal), 0.0, 1.0);
  vec4 phongColor = (ambient + diffuse) * color;
  if (diffuse > 0.0) {
    float specular = 0.8*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
    phongColor += vec4(specular, specular, specular, 1.0);
  }
  return clamp(phongColor, 0.0, 1.0);
}  
