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
  // We want to do the reflection in world space, so we'll
  // Do the view transform in the fragment shader
  fragnormal =  model * normal;
  fraglight =  light;
  fragreflect = reflect(-fraglight, fragnormal);
  vec4 positionworldspace = model * position;
  // Where is the eye in worldspace?
  // This inverse is inefficient, but easier to do here
  frageye = inverse(view) * normalize(vec4(0.0,0.0,0.0,1.0) - positionworldspace);
  // Position is the same
  gl_Position = projection * view * positionworldspace;
}
