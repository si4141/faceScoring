"""
画像から顔の部分を切り出すモジュール
* prepare_data/assetにcascade fileを設置のこと
* 元データの拡張子は、PICTURE_SUFFIXESで指定
"""
import cv2
from pathlib import Path
from logging import getLogger, basicConfig, DEBUG
from settings import ROOT_PATH, RAW_DATA_PATH, TRIMMED_DATA_PATH

CASCADE_FILE = ROOT_PATH.joinpath('prepare_data/asset/haarcascade_frontalface_default.xml')
if not CASCADE_FILE.exists():
    raise FileNotFoundError(f'Cascade file is not found at {CASCADE_FILE}')
cascade = cv2.CascadeClassifier(str(CASCADE_FILE))

PICTURE_SUFFIXES = ['.jpg', '.png', '.bmp']


def trim_face(path_to_img, save_to, logger=None):
    """
    画像ファイルから顔部分を切り出して指定したパスに保存
    複数検出したら全て連番にして全て保存

    :param path_to_img: str : 画像ファイル
    :param save_to: str : 保存先のファイルパス
    :param logger:
    :return: None
    """
    logger = logger or getLogger()

    logger.info(f'Trim face in {path_to_img}')

    img = cv2.imread(path_to_img)
    img_gray = cv2.imread(path_to_img, 0)

    face = cascade.detectMultiScale(img_gray, scaleFactor=1.2, minNeighbors=2, minSize=(50, 50))

    logger.debug(f'Detected face location: {face}')

    for num, loc in enumerate(face):
        x, y, w, h = loc
        face_picture = img[y:y+h, x:x+w]

        picture_save_to = f'{Path(save_to).parent.joinpath(Path(save_to).stem)}_{num}.jpg'
        cv2.imwrite(picture_save_to, face_picture)
        logger.info(f'File saved at {picture_save_to}')


def trim_all_face_in_directory(input_directory: Path, output_directory: Path, logger=None):
    """
    フォルダを指定して、フォルダ内の画像ファイルすべてに対して顔画像を切り抜いて保存
    画像ファイルは、PICTURE_SUFFIXESで定義した拡張子で判定

    :param input_directory: Path: 画像があるディレクトリのパス
    :param output_directory: Path: 保存先のディレクトリ
    :param logger:
    :return: None
    """
    logger = logger or getLogger(__name__)

    picture_suffixes = PICTURE_SUFFIXES

    if not input_directory.is_dir() or not output_directory.is_dir():
        error_path = input_directory if not input_directory.is_dir() else output_directory
        error_msg = f'{error_path} is not directory. If you want to trim face on single file, use trim_face().'

        raise ValueError(error_msg)

    pictures = [img for img in input_directory.glob('*') if img.suffix in picture_suffixes]

    if not pictures:
        raise FileNotFoundError(f'No picture files found in {input_directory}')

    for picture in pictures:
        trim_face(
            str(picture),
            str(output_directory.joinpath(f'{picture.stem}.jpg')),
            logger
        )


if __name__ == '__main__':
    basicConfig(level=DEBUG)
    trim_all_face_in_directory(
        RAW_DATA_PATH,
        TRIMMED_DATA_PATH
    )
