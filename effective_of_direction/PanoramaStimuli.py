#!/usr/bin/env python
"""Moving target over a spinning drum."""

############################
#  Import various modules  #
############################

from VisionEgg import *

from VisionEgg.Core import *
from VisionEgg.FlowControl import Presentation, Controller, FunctionController
from VisionEgg.MoreStimuli import *
from VisionEgg.Textures import *
import os
from math import *
import time

from PIL import Image

start_default_logging()
watch_exceptions()
        
# Initialize OpenGL graphics screen.
screen = get_default_screen()
        

class GeneratingDataSet(object):
    #########################
    #  parameter in matlab  #
    #########################
    def __init__(self):
        self.Data_Parent_Folder = 'D:\\STMD_Dataset\\PanoramaStimuli\\'
        self.BackroundVelocity = 250; #% �����ٶ�
        self.BackroundDirection = 'Leftward'; #% ��������
        self.TargetNum = 'SingleTarget'; #% Ŀ�����
        self.TargetWidth = 5; #% Ŀ����
        self.TargetHeight = 5; #% Ŀ��߶�
        self.TargetVelocity = 250; #% ˮƽ�ٶ�
        self.TargetLuminance = 0; #% Ŀ������ֵ
        self.TargetDirection = 'Rightward'; #% Ŀ���˶�����
        self.CurveAmplitude = 15; #%���
        self.CurveTheta = 0;
        self.CurveTemFrequency = 2; #% �����˶���Ƶ������
        self.VideoSamplingFrequency = 1000; #% ����Ƶ��

    def parameter(self):
        ######################
        #  parameter in py2  #
        ######################
        self.V_B = self.BackroundVelocity # �����ٶ�
        self.TW = self.TargetWidth # Ŀ����
        self.TH = self.TargetHeight # Ŀ��߶�
        self.V_T = (-1)*self.TargetVelocity # ˮƽ�ٶ�
        self.TL = self.TargetLuminance # Ŀ������ֵ   
        self.max_vel = self.CurveAmplitude  # ���
        self.K_2 = self.CurveTemFrequency # �����˶���Ƶ������
        self.fps = self.VideoSamplingFrequency # ����Ƶ��

        ##################
        #  data folder   #
        ##################
        self.SubFolder = 'whiteBG' + \
                           '\\' + self.TargetNum + \
                           '-TW-' + str(self.TargetWidth) + \
                           '-TH-' + str(self.TargetHeight) + \
                           '-TV-' + str(self.TargetVelocity) + \
                           '-TL-' + str(self.TargetLuminance) + \
                           '-' + self.TargetDirection + \
                           '-Amp-' + str(self.CurveAmplitude) + \
                           '-Theta-' + str(self.CurveTheta) + \
                           '-TemFre-' + str(self.CurveTemFrequency) + \
                           '-SamFre-' + str(self.VideoSamplingFrequency) + '\\';
        


        # Initialize OpenGL graphics screen.

        

    def run(self): 
        #######################
        #  Create the target  #
        #######################

        # Create an instance of the Target2D class with appropriate parameters
        RGB = float(self.TL)/255
        target = Target2D(size  = (self.TW,self.TH),
                          color = (RGB,RGB,RGB,1.0), # Set the target color (RGBA) black
                          orientation = 0.0)
        #target_perspective = SimplePerspectiveProjection()
        # Create a viewport for the target
        target_viewport = Viewport(screen=screen, stimuli=[target])

        #####################
        #  Create the drum  #
        #####################
        # panorama.jpg
        # Get a texture                       

        filename = os.path.join(config.VISIONEGG_SYSTEM_DIR,"data","null.jpg")
        texture = Texture(filename)

        # Create an instance of SpinningDrum class
        drum = SpinningDrum(texture=texture, flat = 1, shrink_texture_ok=1,position = (0,155,0))
        #position = (0.0,0.0,0.0), orientation = 0.0,radius = 45
        #stimulus = TextureStimulus(texture = texture,
         #                        shrink_texture_ok=1)
        # position = (screen.size[0]/2.0,screen.size[1]/2.0),
          #                         anchor = 'center',



        # Create a perspective projection for the spinning drum
        #perspective = SimplePerspectiveProjection()



        # Create a viewport with this projection
        drum_viewport = Viewport(screen=screen, stimuli=[drum])
        # # projection = perspective,,
        #stimulus = TextureStimulus(texture = texture,
        #                           position = (screen.size[0]/2.0,screen.size[1]/2.0),
        #                           anchor = 'center',
        #                           shrink_texture_ok=1)

        #drum_viewport = Viewport(screen=screen, stimuli=[stimulus])
                            
        ##################################################
        #  Create an instance of the Presentation class  #
        ##################################################

        # Add target_viewport last so its stimulus is drawn last. This way the
        # target is always drawn after (on top of) the drum and is therefore
        # visible.
        p = Presentation(go_duration=(5000,'frames'),
                         viewports=[drum_viewport,target_viewport])

        ########################
        #  Define controllers  #
        ########################

        '''
        # calculate a few variables we need
        mid_x = screen.size[0]-20
        mid_y = screen.size[1]/2.0
        
        max_vel = self.max_vel  # ���
        K_2 = self.K_2          # �����˶���Ƶ������
        V_T = self.V_T          # ˮƽ�ٶ�
        

        # define target position as a function of time
        def get_target_position(t):
            #global mid_x, mid_y, max_vel, K_2, V_T
            return ( V_T*t+mid_x, # x
                     mid_y + max_vel*sin(2.0*pi*t*K_2) ) # y
        '''

        mid_x = screen.size[0]/2.0
        mid_y = screen.size[1]/2.0

        a = screen.size[0] / 2.5  # Length of the horizontal half axis of the ellipse
        b = screen.size[1] / 2.5 # Length of the vertical half axis of the ellipse
        V_T = self.V_T  # velocity

        # define target position as a function of time
        def get_target_position(t):
            omega = V_T / math.sqrt(a**2 * math.sin(t)**2 + b**2 * math.cos(t)**2)
            x = mid_x + a * math.cos(omega * t)
            y = mid_y + b * math.sin(omega * t)
            return (x, y)

        V_B = 0
        Scale = 5.7
        def get_drum_angle(t):
            return  (V_B/Scale)*t



        # Create instances of the Controller class
        target_position_controller = FunctionController(during_go_func=get_target_position)
        drum_angle_controller = FunctionController(during_go_func=get_drum_angle)

        #############################################################
        #  Connect the controllers with the variables they control  #
        #############################################################

        p.add_controller(target,'position', target_position_controller )
        p.add_controller(drum,'angular_position', drum_angle_controller )
        #p.add_controller(drum,'position', drum_angle_controller )

        #######################
        #  Run the stimulus!  #
        #######################

        #
        #t_dir = 'D:\\Code\\data\\STMD\\FPS1000_by_v\\'
        #base_dir = t_dir + vvv #+ 'index'
        #if not os.path.isdir(base_dir):
        #    base_dir = VisionEgg.config.VISIONEGG_SYSTEM_DIR
        save_directory = os.path.join(self.Data_Parent_Folder, self.SubFolder)

        if not os.path.isdir(save_directory):
            os.makedirs(save_directory)#mkdir
            if not os.path.isdir(save_directory):
                print "Error: cannot make movie directory '%s'."%save_directory
        #print "Saving movie to directory '%s'."%save_directory
        basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        p.export_movie_go(frames_per_sec=self.fps,filename_base=basename,path=save_directory)

        p.go()



if __name__ == '__main__':
    V_change_list = [300,500,1000]
    for v in V_change_list:
        GDS = GeneratingDataSet()
        GDS.TargetWidth = 5; # Ŀ����
        GDS.TargetHeight = 5; # Ŀ��߶�
        GDS.CurveAmplitude = 0
        GDS.TargetLuminance = 0
        GDS.VideoSamplingFrequency = 1000
        GDS.TargetVelocity = v
        GDS.parameter()
        GDS.run()

        del(GDS)

    '''
    GDS = GeneratingDataSet()
    GDS.Data_Parent_Folder = 'D:\\DataSet\\STMD\\Simulated-DataSet\\' #% ���ļ���
    GDS.BackgroundType = 'Complicated-Background\\CB-1'; #% ��������
    GDS.BackroundVelocity = 250; #% �����ٶ�
    GDS.BackroundDirection = 'Leftward'; #% ��������
    GDS.TargetNum = 'SingleTarget'; #% Ŀ�����
    GDS.TargetWidth = 5; #% Ŀ����
    GDS.TargetHeight = 5; #% Ŀ��߶�
    GDS.TargetVelocity = 250; #% ˮƽ�ٶ�
    GDS.TargetLuminance = 25; #% Ŀ������ֵ
    GDS.TargetDirection = 'Rightward'; #% Ŀ���˶�����
    GDS.CurveAmplitude = 15; #%���
    GDS.CurveTheta = 0;
    GDS.CurveTemFrequency = 2; #% �����˶���Ƶ������
    GDS.VideoSamplingFrequency = 1000; #% ����Ƶ��
    GDS.parameter()
    GDS.run()
    '''
