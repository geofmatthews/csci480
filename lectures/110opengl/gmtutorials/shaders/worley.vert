#version 330

in vec4 position;
in vec4 normal;
in vec4 tangent;
in vec4 bitangent;
in vec2 uv;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fraguv;
out vec4 fragnormal;
out vec4 fragtangent;
out vec4 fragbitangent;
out vec4 frageye;
out vec4 fragposition;
out vec4 positionworldspace;
out vec4 positionobjectspace;

void main()
{
  fraguv = uv;
  positionobjectspace = position;
  positionworldspace = model * position;
  // Let's do the lighting calculations in camera space
  mat4 vm = view * model;
  fragnormal =  vm * normal;
  fragtangent = vm * tangent;
  fragbitangent = vm * bitangent;
  vec4 positioncamspace  = vm * position;

  // Where is the eye in cameraspace?
  frageye = normalize(vec4(0.0,0.0,0.0,1.0) - positioncamspace);
  // Can use world position or object position for different effects
  fragposition = positioncamspace;
  gl_Position = projection * positioncamspace;
}
