import ee
import os
import json
import sample

ee.Initialize()

# changes the working dir to the folder that this script lives in
script_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_folder)


def main():
    
    # set up your earth engine assest
    eeImage = ''
    eeFeatCol = fc_from_json('./wd_tr_balanced.json')

    # construct the sample, in this example we are accepting the defult configuration
    sample_obj = sample.SampleRegions(eeFeatCol, eeImage)

    # extract the sample
    
    # extract server side object
    server_side_obj = sample_obj.generate_sample()
    
    # extract a client side object
    client_side_obj = sample_obj.get_GeoJSON()
    
    # write out csv
    sample_obj.write_to_csv('test.csv') 

    pass
    
def fc_from_json(path_to_json):
    """
    Helper function will be used to construct a ee.FeatureCollection from 
    a json file
    """
    
    with open(path_to_json, 'r') as read_file:
        json_obj = json.load(read_file)
        return ee.FeatureCollection(json_obj)


if __name__ == "__main__":
    main()