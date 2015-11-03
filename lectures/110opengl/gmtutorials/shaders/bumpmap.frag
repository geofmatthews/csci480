#version 330
uniform int makebumps;
uniform sampler2D colorsampler;
uniform sampler2D bumpsampler;
in vec4 fragnormal, fragtangent, fragbinormal, 
  fraglight, frageye;
in vec2 fraguv;
out vec4 outputColor;
void main()
{
  vec2 texcoords = fraguv;
  texcoords.s *= 3.0;
  texcoords.t *= 1.5;
  vec4 color = texture2D(colorsampler, texcoords);
  vec4 bump = texture2D(bumpsampler, texcoords);
  // need to normalize interpolated vectors
  vec4 light = normalize(fraglight);
  vec4 normal = normalize(fragnormal);
  vec4 reflect = normalize(reflect(-light, normal));
  vec4 tangent = normalize(fragtangent);
  vec4 binormal = normalize(fragbinormal);
  vec4 eye = normalize(frageye);
  // Use MAP order, multiply first
  if (makebumps == 1) {
    normal = normalize((bump.r*2.0-1.0)*tangent
			       + (bump.g*2.0-1.0)*binormal
			       + (bump.b*2.0-1.0)*normal);
  } 
  float ambient = 0.2;
  float diffuse = 0.8*clamp(dot(light, normal), 0.0, 1.0);
  outputColor = (ambient + diffuse) * color;
  if (diffuse > 0.0) {
    float specular = 0.8*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
    outputColor += vec4(specular, specular, specular, 1.0);
  }
  outputColor = clamp(outputColor, 0.0, 1.0);
}
