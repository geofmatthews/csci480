/*

	Copyright 2013 Etay Meiri

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Tutorial 43 - Shadow mapping with point lights
*/
#include <math.h>
#include <GL/glew.h>
#include <GL/freeglut.h>
#include <string>
#include <assert.h>
#include <float.h>

#include "engine_common.h"
#include "util.h"
#include "pipeline.h"
#include "camera.h"
#include "texture.h"
#include "lighting_technique.h"
#include "glut_backend.h"
#include "mesh.h"
#include "shadow_map_technique.h"
#include "shadow_map_fbo.h"
#ifndef WIN32
#include "freetypeGL.h"
#endif
using namespace std;

#define WINDOW_WIDTH  1000
#define WINDOW_HEIGHT 1000


struct CameraDirection
{
    GLenum CubemapFace;
    Vector3f Target;
    Vector3f Up;
};

CameraDirection gCameraDirections[NUM_OF_LAYERS] = 
{
    { GL_TEXTURE_CUBE_MAP_POSITIVE_X, Vector3f(1.0f, 0.0f, 0.0f),  Vector3f(0.0f, -1.0f, 0.0f) },
    { GL_TEXTURE_CUBE_MAP_NEGATIVE_X, Vector3f(-1.0f, 0.0f, 0.0f), Vector3f(0.0f, -1.0f, 0.0f) },
    { GL_TEXTURE_CUBE_MAP_POSITIVE_Y, Vector3f(0.0f, 1.0f, 0.0f),  Vector3f(0.0f, 0.0f, -1.0f) },
    { GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, Vector3f(0.0f, -1.0f, 0.0f),  Vector3f(0.0f, 0.0f, 1.0f) },
    { GL_TEXTURE_CUBE_MAP_POSITIVE_Z, Vector3f(0.0f, 0.0f, 1.0f),  Vector3f(0.0f, -1.0f, 0.0f) },
    { GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, Vector3f(0.0f, 0.0f, -1.0f),  Vector3f(0.0f, -1.0f, 0.0f) }
};

#ifndef WIN32
Markup sMarkup = { (char*)"Arial", 64, 1, 0, 0.0, 0.0,
                   {.1,1.0,1.0,.5}, {1,1,1,0},
                   0, {1,0,0,1}, 0, {1,0,0,1},
                   0, {0,0,0,1}, 0, {0,0,0,1} };
#endif

class Tutorial43 : public ICallbacks
{
public:

    Tutorial43() 
#ifndef WIN32
           : m_fontRenderer2(sMarkup)
#endif
    {
        m_pGameCamera = NULL;
        m_scale = 0.0f;
        m_pointLight.AmbientIntensity = 0.1f;
        m_pointLight.DiffuseIntensity = 0.9f;
        m_pointLight.Color = Vector3f(1.0f, 1.0f, 1.0f);
        m_pointLight.Attenuation.Linear = 0.0f;
        m_pointLight.Position  = Vector3f(2.0, 8.0, 0.0f);

        m_persProjInfo.FOV = 90.0f;
        m_persProjInfo.Height = WINDOW_HEIGHT;
        m_persProjInfo.Width = WINDOW_WIDTH;
        m_persProjInfo.zNear = 1.0f;
        m_persProjInfo.zFar = 100.0f;  
        
        m_frameCount = 0;
        m_fps = 0.0f;
    }

    ~Tutorial43()
    {
        SAFE_DELETE(m_pGameCamera);
    }    

    bool Init()
    {
        Vector3f Pos(0.0f, 8.0f, -10.0f);
        Vector3f Target(0.0f, -0.5f, 1.0f);
        Vector3f Up(0.0, 1.0f, 0.0f);

        if (!m_shadowMapFBO.Init(WINDOW_WIDTH, WINDOW_HEIGHT)) {
            printf("Error initializing the shadow map FBO\n");
            return false;
        }

        m_pGameCamera = new Camera(WINDOW_WIDTH, WINDOW_HEIGHT, Pos, Target, Up);
      
        if (!m_lightingEffect.Init()) {
            printf("Error initializing the lighting technique\n");
            return false;
        }

        m_lightingEffect.Enable();

        m_lightingEffect.SetColorTextureUnit(COLOR_TEXTURE_UNIT_INDEX);
        m_lightingEffect.SetShadowMapTextureUnit(SHADOW_TEXTURE_UNIT_INDEX);		
        m_lightingEffect.SetPointLight(m_pointLight);
     //   m_lightingEffect.SetShadowMapSize((float)WINDOW_WIDTH, (float)WINDOW_HEIGHT);
        GLExitIfError;
        if (!m_shadowMapEffect.Init()) {
            printf("Error initializing the shadow map technique\n");
            return false;
        }     
        GLExitIfError;
        m_shadowMapEffect.Enable();
        m_shadowMapEffect.SetLightWorldPos(m_pointLight.Position);
        GLExitIfError;
		if (!m_quad.LoadMesh("models/quad.obj")) {
            return false;
        }

        m_quad.GetOrientation().m_scale = Vector3f(10.0f, 10.0f, 10.0f);
        m_quad.GetOrientation().m_rotation = Vector3f(90.0f, 0.0f, 0.0f);

		m_pGroundTex = new Texture(GL_TEXTURE_2D, "models/checkers.png");

        if (!m_pGroundTex->Load()) {
            return false;
        }

        
        if (!m_mesh.LoadMesh("../tutorial25/sphere.obj")) {
	//	if (!m_mesh.LoadMesh("models/phoenix_ugv.md2")) {
			return false;
		}
        
        m_mesh.GetOrientation().m_pos = Vector3f(0.0f, 3.0f, 0.0f);

#ifndef WIN32
        if (!m_fontRenderer.InitFontRenderer()) {
            return false;
        }
        
        if (!m_fontRenderer2.InitFontRenderer()) {
            return false;
        }
#endif
        
        m_time = glutGet(GLUT_ELAPSED_TIME);
        
        glEnable(GL_TEXTURE_CUBE_MAP);
        
        return true;
    }

    void Run()
    {
        GLUTBackendRun(this);
    }
    

    virtual void RenderSceneCB()
    {   
        CalcFPS();
        
        m_scale += 0.05f;

        m_pGameCamera->OnRender();
//
        ShadowMapPass();
        RenderPass();
        
   //     RenderFPS();

        glutSwapBuffers();
    }

    void ShadowMapPass()
    {
        glCullFace(GL_FRONT);
        
        m_shadowMapEffect.Enable();
        GLExitIfError;        
        
        PersProjInfo ProjInfo;
        ProjInfo.FOV = 90.0f;
        ProjInfo.Height = WINDOW_HEIGHT;
        ProjInfo.Width = WINDOW_WIDTH;
        ProjInfo.zNear = 1.0f;
        ProjInfo.zFar = 100.0f;  

        glClearColor(FLT_MAX, FLT_MAX, FLT_MAX, FLT_MAX);
                       
        for (uint i = 0 ; i < NUM_OF_LAYERS ; i++) {
            m_shadowMapFBO.BindForWriting(gCameraDirections[i].CubemapFace);
            glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);                       
            m_shadowMapEffect.ApplyOrientation(m_mesh.GetOrientation(), 
                                                 m_pointLight.Position, 
                                                 gCameraDirections[i].Target, 
                                                 gCameraDirections[i].Up, 
                                                 ProjInfo);
            m_mesh.Render();
            GLExitIfError;        
            
       /*      m_pShadowMapEffect->ApplyOrientation(m_quad.GetOrientation(), m_pointLight.Position, gCameraDirections[i].Target, 
                                                 gCameraDirections[i].Up, 
                                                 ProjInfo);*/
        
        // Render the quad
     //   m_quad.Render();
        }        
    }
        
    void RenderPass()
    {
        glCullFace(GL_BACK);
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        m_lightingEffect.Enable();
             
        m_shadowMapFBO.BindForReading(SHADOW_TEXTURE_UNIT);
                
        m_lightingEffect.SetEyeWorldPos(m_pGameCamera->GetPos());
        
        m_lightingEffect.ApplyOrientation(m_quad.GetOrientation(), *m_pGameCamera, m_persProjInfo);
         
        // Render the quad
        m_pGroundTex->Bind(COLOR_TEXTURE_UNIT);
        m_quad.Render();
        GLExitIfError;        

        // Render the object
        m_lightingEffect.ApplyOrientation(m_mesh.GetOrientation(), *m_pGameCamera, m_persProjInfo);         
        m_mesh.Render();        
        GLExitIfError;        
    }
    virtual void IdleCB()
    {
        RenderSceneCB();
    }

    virtual void SpecialKeyboardCB(int Key, int x, int y)
    {
        m_pGameCamera->OnKeyboard(Key);
    }


    virtual void KeyboardCB(unsigned char Key, int x, int y)
    {
        switch (Key) {
            case 'q':
                glutLeaveMainLoop();
                break;
        }
    }


    virtual void PassiveMouseCB(int x, int y)
    {
        m_pGameCamera->OnMouse(x, y);
    }
    
    
    virtual void MouseCB(int Button, int State, int x, int y)
    {
    }


private:
    
    void CalcFPS()
    {
        m_frameCount++;
        
        int time = glutGet( GLUT_ELAPSED_TIME );

        if (time - m_time > 1000) {
            m_fps = (float)m_frameCount * 1000.0f / (time - m_time);
            m_time = time;
            m_frameCount = 0;
        }
    }
        
    void RenderFPS()
    {
        char text[32];
        ZERO_MEM(text);        
        SNPRINTF(text, sizeof(text), "FPS: %.2f", m_fps);
#ifndef WIN32
        m_fontRenderer.RenderText(10, 10, text);        
#endif
    }       

    LightingTechnique m_lightingEffect;
    ShadowMapTechnique m_shadowMapEffect;
    Camera* m_pGameCamera;
    float m_scale;
    PointLight m_pointLight;
    Mesh m_mesh;
    Mesh m_quad;	
    PersProjInfo m_persProjInfo;
    Texture* m_pGroundTex;
    ShadowMapFBO m_shadowMapFBO;
    int m_time;
    int m_frameCount;
    float m_fps;        
#ifndef WIN32
    FontRenderer m_fontRenderer;
    FontRenderer m_fontRenderer2;
#endif
};


int main(int argc, char** argv)
{
    Magick::InitializeMagick(*argv);
    GLUTBackendInit(argc, argv);

    if (!GLUTBackendCreateWindow(WINDOW_WIDTH, WINDOW_HEIGHT, 32, false, "Tutorial 43")) {
        return 1;
    }

    Tutorial43 App;

    if (!App.Init()) {
        return 1;
    }

    App.Run();

    return 0;
}