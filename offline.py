from importlib.metadata import requires
from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np

# before handling the requests we have to extracting the features of all
# the images that we have in out dataset... in our case it is stored under static folder
if __name__ == '__main__':
    fe = FeatureExtractor()

    for img_path in sorted(Path("./static/img").glob("*.jpg")):
        print(img_path)  # e.g., ./static/img/xxx.jpg
        feature = fe.extract(img=Image.open(img_path))
        feature_path = Path("./static/feature") / (img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
        np.save(feature_path, feature)
