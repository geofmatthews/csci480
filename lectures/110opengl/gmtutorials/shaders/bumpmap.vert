#version 330

in vec4 position;
in vec4 normal;
in vec4 tangent;
in vec4 binormal;
in vec2 uv;
uniform vec4 light;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fraguv;
out vec4 fragnormal;
out vec4 fragtangent;
out vec4 fragbinormal;
out vec4 fraglight;
out vec4 frageye;

void main()
{
  fraguv = uv;
  // Let's do the lighting calculations in camera space
  mat4 vm = view * model;
  fragnormal =  vm * normal;
  fragtangent = vm * tangent;
  fragbinormal = vm * binormal;
  // Now have to do this in the fragment shader
  // fragreflect = reflect(-fraglight, fragnormal);
  fraglight =  view * light;
  vec4 worldposition  = vm * position;
  // Where is the eye in cameraspace?
  frageye = normalize(vec4(0.0,0.0,0.0,1.0) - worldposition);
  gl_Position = projection * worldposition;
}
