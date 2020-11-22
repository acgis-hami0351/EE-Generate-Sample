import ee
import sample
import unittest


ee.Initialize()


class TestSampleRegionsConstruction(unittest.TestCase):
    
    image = 'users/ryangilberthamilton/BC/widgeon/stacks/widgeon_stack_2019'
    fc = 'users/ryangilberthamilton/widgeon/balanced/wd_tr_balanced'
    large_fc = 'users/ryangilberthamilton/widgeon/balanced/wd_va_balanced'
    

    def test_eeImage_Construction(self):
        obj = sample.SampleRegions(self.fc, self.image)
        self.assertIsInstance(obj, ee.Image)
    
    def test_generate_sample_retrun_type(self):
        obj = sample.SampleRegions(self.fc, self.image).generate_sample()
        self.assertIsInstance(obj, ee.FeatureCollection)