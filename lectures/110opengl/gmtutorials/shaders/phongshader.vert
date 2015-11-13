#version 330

in vec4 position;
in vec4 normal;
uniform vec4 light;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec4 fragnormal;
out vec4 fragreflect;
out vec4 fraglight;
out vec4 frageye;

void main()
{
  // Let's do the lighting calculations in camera space
  fragnormal =  view * model * normal;
  fraglight =  view * light;
  fragreflect = reflect(-fraglight, fragnormal);
  vec4 positioncamspace  = view * model * position;
  // Where is the eye in cameraspace?
  frageye = normalize(vec4(0.0,0.0,0.0,1.0) - positioncamspace);
  gl_Position = projection * positioncamspace;
}
