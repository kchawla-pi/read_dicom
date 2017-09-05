try:
    import pydicom
except ImportError:
    import dicom as pydicom  # maintain compatibility with dicom v1.0, known as pydicom

import argparse

from pprint import pprint

import helpers


# helpers.get_filelist()
def get_cli_args():
    arg_parser=argparse.ArgumentParser(description='Reads dicom header',prog='read_dicom_header.py',
                                       usage='%(prog)s --help for list of commands.')
    
    arg_parser.add_argument('dicom_filename',metavar='DicomFile',help='Dicom filename',type=str)
    arg_parser.add_argument('--bids_type',metavar='BIDS JSON Type',
                            help='Type of BIDS JSON file to create %(choices)s',type=str,
                            choices=['anat','fmap','func'])
    
    arg_parser.add_argument('--taskname',metavar='TaskName',
                            help='%(metavar)s when BIDS JSON type is \'func\'',type=str)
    
    in_args=arg_parser.parse_args()
    return in_args


# pprint(hdr.__dir__())

def select_fields():
    return {'EchoTime': 'EchoTime',
            'EffectiveEchoSpacing': 'PixelBandwidth',
            'FlipAngle': 'FlipAngle',
            'MultibandAccelerationFactor': 'Unknown DICOM Field',
            'NumberOfSlices': '[0x0019, 0x100b].value',
            'ParallelReductionFactorInPlane': 'Unknown DICOM Field',
            'PhaseEncodeDirection': 'Unknown DICOM Field',
            'ProtocolName': 'ProtocolName',
            'RepetitionTime': 'RepetitionTime',
            'SequenceName': 'SequenceName',
            'TaskName': 'taskname'
            }




in_args = get_cli_args()
hdr = pydicom.read_file(in_args.dicom_filename)
print(hdr.__dict__)

# pprint(select_fields())
