#version 330

in vec4 position;
in vec2 uv;
uniform vec2 scaleuv;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fraguv;

void main()
{
  fraguv = scaleuv * uv;
  vec4 worldposition  = view * model * position;
  gl_Position = projection * worldposition;
}
