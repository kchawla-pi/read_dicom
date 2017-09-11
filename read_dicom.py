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
	module_path = os.path.join(root_path, module_, 'src')
	os.sys.path.insert(1, module_path)

import slice_timing

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
	              'RepetitionTime': '{}.RepetitionTime /1000',
	              'SequenceName': '{}.SequenceName',
	              'TaskName': '{}.taskname'
	              })


def fields_dict(fields_dict, header):
	final_fields_dict = odict()
	for alias, field_ in fields_dict.items():
		try:
			final_fields_dict.update({alias: eval(field_.format('header'))})
		except (AttributeError, SyntaxError):
			final_fields_dict.update({alias: (field_.format('header'), AttributeError)})
	return final_fields_dict


def add_slice_timings(fields_info):
	slice_timings, slice_scan_order = slice_timing.slice_times(
				rep_time= fields_info['RepetitionTime'],
				num_slices=fields_info['NumberOfSlices']
				)
	fields_info.update(odict({'SliceTimings': slice_timings,
	                   'SliceScanOrder': slice_scan_order,
	                    }))
	return fields_info


def dicom_info(dicom_path, taskname, bids_type):
	hdr = pydicom.read_file(dicom_path)
	fields_str = select_fields()
	fields_info = fields_dict(fields_str, hdr)
	fields_info = add_slice_timings(fields_info=fields_info)
	fields_info['TaskName'] = taskname
	output_as_str(fields_info)
	return fields_info
	
def output_as_str(fields_info):
	info_str = '\n'.join(['{}: {}'.format(alias, data) for alias, data in fields_info.items()])
	return info_str
	

def main(dicom_path=None, taskname=None, bids_type=None):
	if dicom_path:
		dicom_path, taskname, bids_type = dicom_path, taskname, bids_type
	else:
		in_args = get_cli_args()
		dicom_path, taskname, bids_type = in_args.dicom_filename, in_args.taskname, in_args.bids_type
		
	fields_info = dicom_info(dicom_path=dicom_path,
	                         taskname=taskname,
	                         bids_type=bids_type,
	                         )
	return fields_info
	

if __name__ == '__main__':
	dicom_path = os.path.realpath('C:\\Users\\kshit\\Dropbox\\workspace\\tic\\read_dicom\\dicom_files\\mocap_bold.dcm')
	taskname = 'test'
	bids_type = 'func'
	fields_info = main(dicom_path, taskname, bids_type)
	print(output_as_str(fields_info))

"""
(0019, 1018) Private tag data                    OB: b'3500'
 (0008, 2112): <Sequence, length 35, at 284C5DA79A8>,
 (0008, 2112) Source Image Sequence               SQ: <Sequence, length 35, at 212E2F589A8>



"""
