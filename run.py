from datamining.datamining import DataminingAPI, DataminingAlphaBox, DataminingResizeCrop, DataminingAlphaPose
from datamining.config.loader.yaml_loader import YamlLoader

configLoader = YamlLoader("configs/football_player_local2.yaml")

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
