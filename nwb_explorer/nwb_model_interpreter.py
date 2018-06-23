"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import collections
import logging
import pygeppetto.model as pygeppetto
from pygeppetto.model.services.model_interpreter import ModelInterpreter
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.values import Point, ArrayElement, ArrayValue
from pygeppetto.model.variables import Variable
from pynwb import NWBHDF5IO, TimeSeries
import numpy as np
from pynwb.icephys import CurrentClampSeries, CurrentClampStimulusSeries, PatchClampSeries
from pynwb.image import IndexSeries
from pynwb.misc import AnnotationSeries
from pynwb.ogen import OptogeneticSeries
from pynwb.ophys import RoiResponseSeries
import time


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self):
        self.factory = GeppettoModelFactory()

    def importType(self, url, typeName, library, commonLibraryAccess):
        logging.debug('Creating a Geppetto Model')

        geppetto_model = self.factory.createGeppettoModel('GepettoModel')
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(name='nwblib', id='nwblib')
        geppetto_model.libraries.append(nwb_geppetto_library)

        # read data
        io = NWBHDF5IO(url, 'r')
        nwbfile = io.read()

        time_series_list = NWBModelInterpreter.get_timeseries(nwbfile)
        variables = []

        nwbType = pygeppetto.CompositeType(id=str('nwb'), name=str('nwb'), abstract= False)

        for i, time_series in enumerate(time_series_list):
            if isinstance(time_series, RoiResponseSeries): #TODO: just focus on numerical time series for now
                group = "group" + str(i)
                group_variable = Variable(id=group)
                group_type = pygeppetto.CompositeType(id=group, name=group, abstract= False)

                unit = time_series.unit
                timestamps_unit = time_series.timestamps_unit
                metatype = time_series.name

                mono_dimensional_timeseries_list = NWBModelInterpreter.get_mono_dimensional_timeseries(time_series.data[()])
                timestamps = [float(i) for i in time_series.timestamps[()]]

                time_series_time_variable = self.factory.createTimeSeries("time"+str(i), timestamps, timestamps_unit)
                group_type.variables.append(self.factory.createStateVariable("time", time_series_time_variable))

                for index, mono_dimensional_timeseries in enumerate(mono_dimensional_timeseries_list[:10]): #TODO: remove [:10] -> importTypes
                    name = metatype + str(index)
                    time_series_variable = self.factory.createTimeSeries(name+"variable", mono_dimensional_timeseries, unit)
                    group_type.variables.append(self.factory.createStateVariable(name, time_series_variable))

                group_variable.types.append(group_type)
                variables.append(group_variable)
                nwb_geppetto_library.types.append(group_type)

                nwbType.variables.append(self.factory.createStateVariable(group))


    #TODO: This need to be deleted
        mod = nwbfile.get_processing_module('ophys_module')
        rrs = mod['dff_interface'].get_roi_response_series()
        rrs_timestamps = rrs.timestamps
        time2 = self.factory.createTimeSeries('myTimeSeriesValue', rrs_timestamps[()].tolist(), 's')
        geppetto_model.variables.append(self.factory.createStateVariable('time', time2))

        # add type to nwb
        nwb_geppetto_library.types.append(nwbType)

        # add top level variables
        nwb_variable = Variable(id='nwb')
        nwb_variable.types.append(nwbType)
        geppetto_model.variables.append(nwb_variable)
        for variable in variables:
            geppetto_model.variables.append(variable)

        return geppetto_model

    def importValue(self, importValue):
        pass

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []

    @staticmethod
    def get_timeseries(node):
        time_series_list = []
        for child in node.children:
            if isinstance(child, TimeSeries):
                time_series_list.append(child)
            else:
                time_series_list += NWBModelInterpreter.get_timeseries(child)
        return time_series_list

    @staticmethod
    def get_mono_dimensional_timeseries(values):
        mono_time_series_list = []
        if isinstance(values, collections.Iterable):
            try:
                data = [float(i) for i in values]
                mono_time_series_list.append(data)
            except:
                for inner_list in values:
                    mono_time_series_list += NWBModelInterpreter.get_mono_dimensional_timeseries(inner_list)
        return mono_time_series_list
