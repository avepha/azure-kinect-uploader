import io
from PIL import Image
from pyk4a import PyK4A
from datetime import datetime
import boto3
from decouple import config

DEVICE_ID = 'test-device'

session = boto3.Session(
    aws_access_key_id=config('AWS_KEY'),
    aws_secret_access_key=config('AWS_SECRET'),
)

def get_path_dir():
    return "%s/%s-%s/%s" % (DEVICE_ID, datetime.now().month, datetime.now().year, datetime.now().isoformat())

def main():
    s3 = session.client('s3')
    k4a = PyK4A()
    k4a.start()
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    capture = k4a.get_capture()

    path_dir = get_path_dir()

    raw_ir = capture.ir
    ir_bytes = io.BytesIO()
    Image.fromarray(raw_ir).save(ir_bytes, format='png')
    ir_bytes.seek(0)
    ir_key = "%s/%s" % (path_dir, 'ir_img.png')

    s3.put_object(Body=ir_bytes, Bucket='kinect-uploader', Key=ir_key)

    raw_color = capture.color
    color_bytes = io.BytesIO()
    Image.fromarray(raw_color).save(color_bytes, format='png')
    color_bytes.seek(0)
    color_key = "%s/%s" % (path_dir, 'color_img.png')
    s3.put_object(Body=color_bytes, Bucket='kinect-uploader', Key=color_key)

    raw_depth = capture.depth
    depth_bytes = io.BytesIO()
    Image.fromarray(raw_depth).save(depth_bytes, format='png')
    depth_bytes.seek(0)
    depth_key = "%s/%s" % (path_dir, 'depth_img.png')
    s3.put_object(Body=depth_bytes, Bucket='kinect-uploader', Key=depth_key)

    raw_point_cloud = capture.depth_point_cloud
    key = "%s/%s" % (path_dir, 'point_cloud_raw')
    s3.put_object(Body=raw_point_cloud.tobytes(), Bucket='kinect-uploader', Key=key)

    key = "%s/%s" % (path_dir, 'raw_color')
    s3.put_object(Body=raw_color.tobytes(), Bucket='kinect-uploader', Key=key)

    key = "%s/%s" % (path_dir, 'raw_depth')
    s3.put_object(Body=raw_color.tobytes(), Bucket='kinect-uploader', Key=key)

    key = "%s/%s" % (path_dir, 'raw_ir')
    s3.put_object(Body=raw_ir.tobytes(), Bucket='kinect-uploader', Key=key)


if __name__ == "__main__":
    main()
