
#version 330

in vec4 position;
in vec4 normal;
uniform vec4 color;
uniform vec4 light;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec4 fragcolor;

void main()
{
  // Let's do the lighting calculations in camera space
  vec4 vertnormal =  normalize(view * model * normal);
  vec4 vertlight =  normalize(view * light);
  vec4 vertreflect = reflect(-light, normal);
  vec4 worldposition  = view * model * position;
  // Where is the eye in cameraspace?
  vec4 verteye = normalize(vec4(0.0,0.0,0.0,1.0) - worldposition);
  float ambient = 0.2;
  float diffuse = 0.8*clamp(dot(vertlight, vertnormal), 0.0, 1.0);
  fragcolor = (ambient + diffuse) *  color;
  if (dot(vertlight, vertnormal) > 0.0) {
    float specular = 0.8*pow(clamp(dot(vertreflect, verteye), 0.0, 1.0), 8);
    fragcolor += vec4(specular, specular, specular, 1.0);
  }
  fragcolor = clamp(fragcolor, 0.0, 1.0);
  gl_Position = projection * worldposition;
}

