#version 330
// Use with worley.vert
// Adjust scaleCoords, dither, etc.

//Uniforms:
uniform vec4 color;
uniform vec4 light;

// Ins:
in vec2 fraguv;
in vec4 fragnormal;
in vec4 fragtangent;
in vec4 fragbitangent;
in vec4 fragposition;
in vec4 positionworldspace;
in vec4 positionobjectspace;
in vec4 positioncameraspace;
in vec4 frageye;

// Outs:
out vec4 outputColor;

int integerNoise(in int n)
// given an integer, return a pseudo-random integer
{
  n = (n << 13) ^ n;
  return (n * (n*n*15731+789221) + 1376312589) & 0x7fffffff;
}

float cellnoise(vec4 position)
// Returns float in range 0..1
{
    // There are frequently artifacts around the origin,
    // so we offset before doing our noise.
    position += vec4(100,100,100,0);
    int n = integerNoise(int(position.x));
    n = integerNoise(n + int(position.y));
    n = integerNoise(n + int(position.z));
    return float(n % 1000000)/1000000.0;
}

void voronoi_f1f2_3d(vec4 p, float jitter,
                     out float f1, out vec4 pos1,
                     out float f2, out vec4 pos2)
// Following implementation in _Advanced Renderman_,
// Apodaca and Gritz
{
    vec4 thiscell = vec4(floor(p.x)+0.5,
                         floor(p.y)+0.5,
                         floor(p.z)+0.5, 1.0);
    f1 = 10000.0;
    f2 = 10000.0;
    float i,j,k;
    for (i = -1; i <= 1; i += 1) {
        for (j = -1; j <= 1; j += 1) {
            for (k = -1; k <= 1; k += 1) {
                vec4 testcell = thiscell + vec4(i,j,k,0);
                vec4 pos = testcell +
                           jitter * (cellnoise(testcell) - 0.5);
                vec4 offset = pos - p;
                float dist = dot(offset, offset);
                if (dist < f1) {
                    f2 = f1;
                    pos1 = pos1;
                    f1 = dist;
                    pos1 = pos;
                } else if (dist < f2) {
                    f2 = dist;
                    pos2 = pos;
                }
            }
        }
    }
    f1 = sqrt(f1);
    f2 = sqrt(f2);
}

vec4 phong(vec4 color, vec4 normal, vec4 eye, vec4 reflect, vec4 light) {
  float ambient = 0.4;
  float diffuse = 0.6*clamp(dot(light, normal), 0.0, 1.0);
  vec4 phongColor = (ambient + diffuse) * color;
  if (diffuse > 0.0) {
    float specular = 0.4*pow(clamp(dot(reflect, eye), 0.0, 1.0), 8);
    phongColor += vec4(specular, specular, specular, 1.0);
  }
  return clamp(phongColor, 0.0, 1.0);
}  

void main()
{
  vec4 normal = normalize(fragnormal);
  vec4 tangent = normalize(fragtangent);
  vec4 bitangent = normalize(fragbitangent);
  vec4 reflect = normalize(reflect(-light, normal));
  vec4 eye = normalize(frageye);

  float f1, f2;
  vec4 pos1, pos2;
  float scaleCoords = 0.25;
  float dither = 0.2;
  voronoi_f1f2_3d(positionobjectspace*scaleCoords,
		  dither,
		  f1, pos1,
		  f2, pos2);
  // try f1, f2, 1-f1, f2-f1, etc.
  float worleyfunc = step((f2-f1), 0.0125);
  //float worleyfunc = (f2-f1);
  vec4 newcolor = clamp(color*worleyfunc, 0.0, 1.0);
  newcolor.a = 1.0;

  // alternatively, we can color with just cell noise
  if (0==1) {
    float noise = cellnoise(pos1);
    newcolor = vec4(noise, noise, noise, 1.0);
  }

  // to make good use of worley noise, we may need the
  // bumpmapping vectors and texture coords, hence this
  // hack to keep stuff from being optimized away:
  if (f1 > 1.0e10) {
    newcolor = newcolor+normal+tangent+bitangent+reflect+eye;
    newcolor.rg = newcolor.rg+fraguv;
  }
  outputColor = phong(newcolor, normal, eye, reflect, light);
}
