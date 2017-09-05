try:
    import pydicom
except ImportError:
    import dicom as pydicom # maintain compatibility with dicom v1.0, known as pydicom
import os


from pprint import pprint


def get_filelist(path='.', exts=('.dcm', '')):

    walked = [
        [os.path.join(root, file_) for file_ in all_files if os.path.splitext(file_)[1] in exts
            ]
            for root, subdir, all_files in os.walk(path)
        ]
    return [walked_ for walked_ in walked if walked_][0]


def read_binary(filepath):
    with open(filepath, 'rb') as dicom_read_obj:
        dicom_bin = dicom_read_obj.read()
    return dicom_bin
    
    
def pprint_dicoms(path='.', pause=True):
    dicom_files = get_filelist(path=path)
    for dicom_file_ in dicom_files:
        # header=dicom.read_binary(dicom_file_)#, force=True)
        # print(header)
        try:
            header = pydicom.read_file(dicom_file_)#, force=True)
        except (KeyError, pydicom.errors.InvalidDicomError):
            print('-'*3, 'excepted')
            header = read_binary(dicom_file_)
        finally:
            try:
                print('v'*10, dicom_file_, 'v'*10)
                pprint(header)
            except UnboundLocalError:
                print('No header variable')
            else:
                print('^'*10,dicom_file_,'^'*10)
            print()
        if pause:
            abort = input('Enter: more, q: exit :')
            if abort:
                os.sys.exit()
        
def get_fields_from_file(filepath):
    with open(filepath, 'r') as read_obj:
        field_text = read_obj.read()
    field_text = field_text.replace(':', '\n')
    fields = field_text.split('\n')
    fields = [elem_ for elem_ in fields if not elem_.startswith(' ')]
    if fields[-1] == '':
        fields.pop()
    
    pprint(fields)
    
        
def main():
    pprint_dicoms()
    
    
def get_real_fields():
    raw_str =    """
        print('ProtocolName: {0}'.format(hdr.ProtocolName))
        print('SequenceName: {0}'.format(hdr.SequenceName))
        print('RepetitionTime: {0}'.format(hdr.RepetitionTime))
    
        print('TaskName: {0}'.format(in_args.taskname))
        print('EchoTime: {0}'.format(hdr.EchoTime))
        print('NumberOfSlices: {0}'.format(hdr[0x0019, 0x100b].value))  # This may not be the correct field
        print('EffectiveEchoSpacing: {0}'.format( 1/hdr.PixelBandwidth ))
        print('FlipAngle: {0}'.format( hdr.FlipAngle ))
    
        print('MultibandAccelerationFactor: {0}'.format( 'Unknown DICOM Field' ))
        print('ParallelReductionFactorInPlane: {0}'.format( 'Unknown DICOM Field' ))
        print('PhaseEncodeDirection: {0}'.format( 'Unknown DICOM Field'))
        """
    raw_list = raw_str.replace('hdr.','))')
    raw_list = raw_list.replace('in_args.', '))')
    raw_list = raw_list.split('))')
    raw_list = [elem_.strip() for elem_ in raw_list]
    for idx, elem_ in enumerate(raw_list):
        if 'Unknown DICOM Field' in elem_:
            raw_list[idx] = 'Unknown DICOM Field'
        elif '.value' in elem_:
            raw_list[idx] = '[0x0019, 0x100b].value'
        elif not elem_.isalpha():
            raw_list[idx] = ''
    # for idx in
    raw_list = [elem_ for elem_ in raw_list if elem_ != '']
    return raw_list

def make_fields_dict():
    fields_alias=['ProtocolName',
                  'SequenceName',
                  'RepetitionTime',
                  'TaskName',
                  'EchoTime',
                  'NumberOfSlices',
                  'EffectiveEchoSpacing',
                  'FlipAngle',
                  'MultibandAccelerationFactor',
                  'ParallelReductionFactorInPlane',
                  'PhaseEncodeDirection',
                  ]
    
    fields_actual=['ProtocolName',
                   'SequenceName',
                   'RepetitionTime',
                   'taskname',
                   'EchoTime',
                   '[0x0019, 0x100b].value',
                   'PixelBandwidth',
                   'FlipAngle',
                   'Unknown DICOM Field',
                   'Unknown DICOM Field',
                   'Unknown DICOM Field',
                   ]
    return {alias:actual for alias,actual in zip(fields_alias,fields_actual)}


def helper():
    # test_key = 'EchoTime'
    missing_fields=list()
    for field_ in fields:
        try:
            print(field_,':',eval('.'.join(['hdr',field_])))
        except AttributeError:
            missing_fields.append(field_)
    
    print()
    print(missing_fields)
    

    
    
if __name__ == '__main__':
    # main()
    # get_fields_from_file('fields.txt')
    pprint(get_real_fields())

# dicom._dicom_dict


