# Author: Ryan Hamilton


import ee
import os
import csv
import json

from ee.ee_exception import EEException

ee.Initialize()


class Image(ee.Image):
    
    def __init__(self, constuctor) -> None:
        super().__init__(constuctor)


class Sample(Image):
    
    def __init__(self, collection, image) -> None:
        super().__init__(image)
        self._col = None
        self._img = image
        self._sample = None
        
        if not isinstance(collection, ee.FeatureCollection):
            self._col = ee.FeatureCollection(collection)
        else:
            self._col = collection    
            
    def generate_sample(self) -> ee.FeatureCollection:
    
        raise NotImplementedError
    
    def get_GeoJSON(self) -> dict:
    
        raise NotImplementedError
    
    def get_GeoJson_Large_FC(self) -> dict:
        
        raise NotImplementedError
    

class SampleRegions(Sample):

    def __init__(self, collection, image, configuration=None) -> None:
        super().__init__(collection, image)
        self._configeration = configuration
        self._config = {}
        self.set_config()
        
        self._sample = self.sampleRegions(**self._config)
    
    def set_config(self):
        """
        This method by defult will set the configuration for generating the sample
        """
        if self._configeration is not None:
            # TODO -> need to put type testing and make sure the correct keys 
            # are in the config
            self._config = self._configeration
        
        else:
            self._config.update( {
                'collection': self._col,
                'tileScale': 4,
                'scale': 10,
                'properties': None
            } )

    def get_GeoJSON(self) -> dict:
        
        """Used to take a earth engine server side object and convert it to a client side object.
         

        Raises:
            Exception: If the sample is empty will throw an error

        Returns:
            dict: python representation of a json file 
        """        
        
        if self._sample is None:
            raise Exception("The Sample Is Empty")
        
        geojson = self._col.getInfo()
        
        try:
            geojson = self._col.getInfo()
        
        
        except EEException as e:
            print(e)

        else:
            return geojson
    
    def get_GeoJson_Large_FC(self, split_property:str) -> dict:
        """Used to extract large sample point collections from earth engine api. Has a simialr purpose as get_GeoJSON method 
        The way it works is it takes split the feature collection intally by the field you want to split it on. It then attemps to 
        convert the ee objects into client side objects. 

        Args:
            split_property (str): the prpoerty we want tinfo = eeFeatCol.getInfo()
        """                
        
        export = []

        labels = self._col.aggregate_array(split_property).distinct().getInfo()

        splits = {
            k: self._col.filter(ee.Filter.eq(split_property, k)) for k in labels
        }
        
        for k, v in splits:
            
            length = v.size().getInfo()
            if length <= 5000:
                export.update({k: v.getInfo()})
            
            elif length > 5000:
                # TODO add logic that will split the object into chuncks of
                # 5000 or less
                # Idea map a index to each feature and select based on the feature
                pass
            
            else:
                continue


    def generate_sample(self) -> ee.FeatureCollection:
        
        """Used to access the sample property that stores the 
        the returned earth engine object from the sampleRegions
        method. A pixel value is returned for every band that is defined 
        in the input image

        Returns:
            ee.FeatureCollection: Containing a pixel value per band
        """        
        
        return self._sample 

    def write_to_csv(self, fname:str, path='./'):
        """This only works for sampels that have 5000 or less features cumlative in the 
        feature collection

        Args:
            fname (str): [description]
        """                
        
        if self._sample.size().getInfo() > 5000:
            raise EEException('Collection is to big... Exiting')
        
        
        data = self._sample.getInfo().get('features')
        rows = [i.get('properties') for i in data]
        
        header = list(rows[0].keys())
        
        with open(os.path.join(path, fname)) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            writer.writerows()
            csv_file.close()
            
