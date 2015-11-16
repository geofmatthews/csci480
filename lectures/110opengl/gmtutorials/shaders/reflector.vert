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
  fragnormal =   model * normal;
  fraglight =   light;
  fragreflect = reflect(-fraglight, fragnormal);
  vec4 positionworldspace =  model * position;
  vec4 positioncameraspace = view * positionworldspace;
  // Where is the eye in worldspace?
  // This inverse is inefficient, but easier to do here
  frageye =  inverse(view) * normalize(vec4(0.0,0.0,0.0,1.0) - positioncameraspace);
  gl_Position = projection * positioncameraspace;
}
