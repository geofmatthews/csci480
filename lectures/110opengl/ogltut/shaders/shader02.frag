#version 330 core

// Interpolated values from vertex shader
in vec4 incolor;

// Ouput data
out vec4 color;

void main()
{
	color = incolor;
}
