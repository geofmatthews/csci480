
#version 330
uniform sampler2D samplercolor;
uniform sampler2D samplernoise;
uniform float threshold;
in vec4 fragnormal, fragreflect, fraglight, frageye;
in vec2 fraguv;
out vec4 outputColor;
void main()
{
  vec4 color = texture2D(samplercolor, fraguv);
  vec4 noise = texture2D(samplernoise, fraguv);
  if (noise.r > threshold) {
    discard;
  }

  vec4 light, reflect, normal, eye;
  // need to normalize interpolated vectors
  light = normalize(fraglight);
  reflect = normalize(fragreflect);
  normal = normalize(fragnormal);
  eye = normalize(frageye);
  float ambient = 0.2;
  float diffuse = 0.8*clamp(dot(light, normal), 0.0, 1.0);
  outputColor = (ambient + diffuse) * color;
  if (diffuse > 0.0) {
     float specular = 0.8*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
     outputColor += vec4(specular, specular, specular, 1.0);
  }
  outputColor = clamp(outputColor, 0.0, 1.0);
}
