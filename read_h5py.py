

# Input data from our own flavour of HDF5-dataset

import h5py
import numpy as np

class BioData:

    def __init__(self,fname):

        # This file is included in bioread
        self.hf = h5py.File(fname,'r')
        self.fname = fname

        bio = {}

        self.SR = None
        if 'participants' not in self.hf.attrs:
            print("# Error, missing participants attribute in the root.")
        self.participants = self.hf.attrs['participants']
        self.channels_by_type = {}
        for p in self.participants:
            for ch in self.hf[p].keys():
                nm = "{}-{}".format(p,ch)
                dset = self.hf[p][ch]
                if not self.SR: self.SR=dset.attrs['SR']
                assert self.SR==dset.attrs['SR']
                bio[nm]=dset ##np.array(dset[:]) # convert into numpy array just to be sure
                mod = dset.attrs['modality']
                self.channels_by_type[mod] = self.channels_by_type.get(mod,[])+[nm]

        bio['t']=np.arange(dset.shape[0])/self.SR

        self.bio = bio
        self.preprocessed = {}


    def get_ecg_channels(self):
        return self.channels_by_type['ecg']



    def get_participants(self):
        return self.participants



    def summary(self):
        ret = "Summary of {}\n".format(self.fname)
        for p in self.participants:
            ret += "\nParticipant {}\n".format(p)
            part = self.hf[p]
            for chn in part:
                ch = part[chn]
                nsamp = ch.size
                frq = ch.attrs['SR']
                dur = nsamp/frq
                ret += "∟ channel {} [ modality {} ] {} samples @ {:.1f} Hz; duration {:.1f} s\n".format(
                    chn,
                    ch.attrs['modality'],
                    nsamp,
                    frq,
                    dur
                )
        return (ret)