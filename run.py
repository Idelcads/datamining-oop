from datamining.datamining import DataminingAPI, DataminingAlphaBox, DataminingResizeCrop, DataminingAlphaPose, DataminingDensePose
from datamining.config.loader.yaml_loader import YamlLoader

# listconfig = ["configs/Edouard.yaml","configs/Edouard2.yaml","configs/Edouard3.yaml","configs/Edouard4.yaml","configs/Edouard5.yaml"]
listconfig = ["configs/badinter.yaml"]

for configname in listconfig:
    configLoader = YamlLoader(configname)
    print(configname)
    for process in configLoader.cfg["PROCESS"]["ORDER"]:
        if process == 'loader':
            datamining = DataminingAPI(configLoader) # On télécharge les images avec flickr ou API si besoins
            datamining.run()
        elif process == 'bbox':
            datamining = DataminingAlphaBox(configLoader) # On extrait les bbox
            datamining.run()
        elif process == 'resize':
            datamining = DataminingResizeCrop(configLoader) # On resize et crop si besoin avec albumentation
            datamining.run()
        elif process == 'pose_estimation':
            datamining = DataminingAlphaPose(configLoader)
            datamining.run()
        elif process == 'densepose':
            datamining = DataminingDensePose(configLoader)
            datamining.run()
