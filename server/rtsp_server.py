import cv2
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import GLib, Gst, GstRtspServer

DEVICE_ID = 0
FPS = 30
IMAGE_WIDTH = 480
IMAGE_HEIGHT = 360
PORT = 8000


class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        super(SensorFactory, self).__init__()
        self.cap = cv2.VideoCapture(DEVICE_ID)
        self.number_frames = 0
        self.duration = 1 / FPS * Gst.SECOND
        self.launch_string = f'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             f'caps=video/x-raw,format=RGB,width={IMAGE_WIDTH},height={IMAGE_HEIGHT},framerate={FPS}/1 ' \
                             f'! videoflip method=counterclockwise ! videoflip method=vertical-flip ' \
                             f'! videoconvert ! video/x-raw,format=I420 ' \
                             f'! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             f'! rtph264pay config-interval=1 name=pay0 pt=96'

    def on_need_data(self, src, length):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(
                    frame, (IMAGE_WIDTH, IMAGE_HEIGHT), interpolation=cv2.INTER_LINEAR)
                data = frame.tobytes()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.number_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.number_frames += 1
                src.emit('push-buffer', buf)

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self):
        super(GstServer, self).__init__()
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.set_service(str(PORT))
        self.get_mount_points().add_factory('/stream', self.factory)
        self.attach(None)


if __name__ == '__main__':
    print("Server: Setting up the RTSP stream...")
    Gst.init(None)
    server = GstServer()
    loop = GLib.MainLoop()
    print("Server: Starting the RTSP stream...")
    loop.run()
    print("Server: RTSP stream ended")
