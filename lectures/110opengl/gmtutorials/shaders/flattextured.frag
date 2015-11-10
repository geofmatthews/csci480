
#version 330
uniform sampler2D sampler;
in vec2 fraguv;
out vec4 outputColor;
void main()
{
  outputColor = texture2D(sampler, fraguv);
}
