
#version 330
uniform sampler2D sampler;
uniform float fade;
in vec2 fraguv;
out vec4 outputColor;
void main()
{
  outputColor = fade*texture2D(sampler, fraguv);
}
