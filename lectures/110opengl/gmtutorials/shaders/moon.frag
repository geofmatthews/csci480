#version 330
uniform int usenormals;
uniform vec4 light;
uniform sampler2D colorsampler;
uniform sampler2D normalsampler;
in vec4 fragnormal, fragtangent, fragbitangent, frageye;
in vec2 fraguv;
out vec4 outputColor;
void main()
{
  vec2 texcoords = fraguv;
  vec4 color = texture2D(colorsampler, texcoords);
  vec4 bump = texture2D(normalsampler, texcoords);
  // need to normalize interpolated vectors
  vec4 normal = normalize(fragnormal);
  vec4 reflect = normalize(reflect(-light, normal));
  vec4 tangent = normalize(fragtangent);
  vec4 bitangent = normalize(fragbitangent);
  vec4 eye = normalize(frageye);
  // Use MAP order, multiply first
  if (usenormals == 1) {
    normal = normalize(0.5*(bump.r*2.0-1.0)*tangent
		       + 0.5*(bump.g*2.0-1.0)*bitangent
		       + (bump.b*2.0-1.0)*normal);
  } 
  float ambient = 0.1;
  float diffuse = 0.9*clamp(pow(dot(light, normal),0.25), 0.0, 1.0);
  outputColor = (ambient + diffuse) * color;
  // no specular for the moon:
  if (diffuse > 10000.0) {
    float specular = 0.8*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
    outputColor += vec4(specular, specular, specular, 1.0);
  }
  outputColor = clamp(outputColor, 0.0, 1.0);
}
