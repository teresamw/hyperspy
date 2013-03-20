# -*- coding: utf-8 -*-
# Copyright 2007-2011 The Hyperspy developers
#
# This file is part of  Hyperspy.
#
#  Hyperspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  Hyperspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  Hyperspy.  If not, see <http://www.gnu.org/licenses/>.

import traits.api as t
import traitsui.api as tu
from traitsui.menu import OKButton, ApplyButton, CancelButton, ModalButtons

class General(t.HasTraits):
    title = t.Str(t.Undefined)
    original_filename = t.File(t.Undefined)
    signal_kind = t.Str(t.Undefined)
    record_by = t.Enum('spectrum', 'image', default = t.Undefined)


class SEMParametersUI(t.HasTraits):
    
    beam_energy = t.Float(t.Undefined,
        label = 'Beam energy (keV)')
    live_time = t.Float(t.Undefined,
        label = 'Live time (s)')
    tilt_stage = t.Float(t.Undefined,
        label = 'Stage tilt (degree)')
    azimuth_angle = t.Float(t.Undefined,
        label = 'Azimuth angle (degree)')
    elevation_angle = t.Float(t.Undefined,
        label = 'Elevation angle (degree)')
        
    traits_view = tu.View(
        tu.Group('beam_energy',
        'live_time',
        'tilt_stage',
            label = 'SEM',show_border = True),
        tu.Group('azimuth_angle',
        'elevation_angle',
            label = 'EDS',show_border = True),
        kind = 'modal', buttons = [OKButton, CancelButton],
        title = 'SEM parameters definition wizard')  
        
class TEMParametersUI(t.HasTraits):
    
    beam_energy = t.Float(t.Undefined,
        label = 'Beam energy (keV)')
    live_time = t.Float(t.Undefined,
        label = 'Live time (s)')
    tilt_stage = t.Float(t.Undefined,
        label = 'Stage tilt (degree)')
    azimuth_angle = t.Float(t.Undefined,
        label = 'Azimuth angle (degree)')
    elevation_angle = t.Float(t.Undefined,
        label = 'Elevation angle (degree)')
        
    traits_view = tu.View(
        tu.Group('beam_energy',
        'live_time',
        'tilt_stage',
            label = 'TEM',show_border = True),
        tu.Group('azimuth_angle',
        'elevation_angle',
            label = 'EDS',show_border = True),
        kind = 'modal', buttons = [OKButton, CancelButton],
        title = 'TEM parameters definition wizard')   
        
       
