from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from pathlib import Path
import cv2
import os
from os.path import isfile, join


class MyVideo(BoxLayout):
    def __init__(self, **kwargs):
        super(MyVideo, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        # display video to mobile user from local 'videos' folder
        self.player = VideoPlayer(source='videos/sample2.mkv', state='play', options={'allow_stretch': True})
        self.add_widget(self.player)
        # a button to add overlay(dot) inside video
        self.submit = Button(text="Insert Overlay", size=(200, 50), size_hint=(None, None),
                             background_color=(0, 1, 0, 1), pos_hint={'x': .3, 'y': .2})
        self.submit.bind(on_release=self.insert_dot)
        self.add_widget(self.submit)

    def frames_to_video(self, input_path, output_path, fps):
        image_array = []
        files = [f for f in os.listdir(input_path) if isfile(join(input_path, f))]
        files.sort(key=lambda x: int(x[5:-4]))
        for i in range(len(files)):
            img = cv2.imread(input_path + files[i])
            size = (img.shape[1], img.shape[0])
            img = cv2.resize(img, size)
            image_array.append(img)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        for i in range(len(image_array)):
            out.write(image_array[i])
        out.release()
        self.player.source = output_path

    def insert_dot(self, instance):
        # read displayed video
        cap = cv2.VideoCapture(self.player.source)
        fps = cap.get(cv2.CAP_PROP_FPS)
        x = int((self.player.width / 2) - 50)
        y = int((self.player.height / 2) - 50)
        print(x)
        print(y)
        count = 1
        while True:
            # Capture frames in the video
            has_frame, frame = cap.read()
            # describe the type of font to be used.
            font = cv2.FONT_HERSHEY_SIMPLEX
            # inserting a dot on each frame
            cv2.putText(frame,
                        '.',
                        (x, y),
                        font, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)

            # Save the each resulting frame with dot in local 'images' folder
            if not has_frame:
                break
            Path("images").mkdir(parents=True, exist_ok=True)
            cv2.imwrite("images/frame" + str(count) + ".jpg", frame)  # Save frame as JPG file
            count = count + 1

        # release the cap object
        cap.release()
        # convert frames with dot to video and display to the user
        self.frames_to_video("images/", "videos/sample3.mkv", fps)


class VideoOverlayApp(App):
    def build(self):
        return MyVideo()


if __name__ == "__main__":
    VideoOverlayApp().run()
