
#version 330

// Arrays of samplers are going through revision, so...
uniform sampler2D s0;
uniform sampler2D s1;
uniform sampler2D s2;
uniform sampler2D s3;
uniform sampler2D s4;
uniform sampler2D s5;
uniform sampler2D s6;
uniform sampler2D s7;
in vec4 fragnormal, fragreflect, fraglight, frageye;
in vec2 fraguv;
out vec4 outputColor;
void main()
{
  float frac = 1.0/8.0;
  vec4 color = frac*texture2D(s0,fraguv) +
               frac*texture2D(s1,fraguv) + 
               frac*texture2D(s2,fraguv) + 
               frac*texture2D(s3,fraguv) + 
               frac*texture2D(s4,fraguv) + 
               frac*texture2D(s5,fraguv) + 
               frac*texture2D(s6,fraguv) + 
               frac*texture2D(s7,fraguv);
  outputColor = color;
}
