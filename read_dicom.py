try:
	import pydicom
except ImportError:
	import dicom as pydicom# maintain compatibility with dicom v1.0, known as pydicom

import argparse
import os

from collections import OrderedDict as odict
from pprint import pprint


# from ..slice_timing.src import slice_timing


curr_file_path, filename = os.path.split(os.path.realpath(__file__))
root_path = os.path.realpath(os.path.join(curr_file_path, '..'))
module_names = ['slice_timing']
os.sys.path.insert(1, root_path)
for module_ in module_names:
	module_path = os.path.join(root_path, module_)
	os.path.sys.insert(1, module_path)

print(os.sys.path)

print(slice_timing.slice_times)

def get_cli_args():
	arg_parser = argparse.ArgumentParser(description='Reads dicom header',
										 prog='read_dicom_header.py',
										 usage='%(prog)s --help for list of commands.')
	
	arg_parser.add_argument('dicom_filename', metavar='DicomFile', help='Dicom filename', type=str)
	arg_parser.add_argument('--bids_type', metavar='BIDS JSON Type',
							help='Type of BIDS JSON file to create %(choices)s', type=str,
							choices=['anat', 'fmap', 'func'])
	
	arg_parser.add_argument('--taskname', metavar='TaskName',
							help='%(metavar)s when BIDS JSON type is \'func\'', type=str)
	
	in_args = arg_parser.parse_args()
	return in_args


def select_fields():
	return odict({'EchoTime': '{}.EchoTime',
	              'EffectiveEchoSpacing': '{}.PixelBandwidth ** (-1)',
	              'FlipAngle': '{}.FlipAngle',
	              'MultibandAccelerationFactor': '{}.MultibandAccelerationFactor',
	              'NumberOfSlices': 'len({}.SourceImageSequence)',
	              'ParallelReductionFactorInPlane': '{}.ParallelReductionFactorInPlane',
	              'PhaseEncodeDirection': '{}.PhaseEncodeDirection',
	              'ProtocolName': '{}.ProtocolName',
	              'RepetitionTime': '{}.RepetitionTime',
	              'SequenceName': '{}.SequenceName',
	              'TaskName': '{}.taskname'
	              })


def fields_dict(fields_dict, header):
	final_fields_dict = odict()
	for alias, field_ in fields_dict.items():
		try:
			final_fields_dict.update({alias: eval(field_.format('header'))})
		except (AttributeError, SyntaxError):
			final_fields_dict.update({alias: (field_, AttributeError)})
	return final_fields_dict


in_args = get_cli_args()
hdr = pydicom.read_file(in_args.dicom_filename)
fields_str = select_fields()
fields_dict = fields_dict(fields_str, hdr)
pprint(dict(fields_dict))
# print(hdr['0008, 2112'])
print(fields_dict['ProtocolName'], fields_dict['NumberOfSlices'])
print(slice_timing.slice_times())#.slice_times())
"""
(0019, 1018) Private tag data                    OB: b'3500'
 (0008, 2112): <Sequence, length 35, at 284C5DA79A8>,
 (0008, 2112) Source Image Sequence               SQ: <Sequence, length 35, at 212E2F589A8>



"""
