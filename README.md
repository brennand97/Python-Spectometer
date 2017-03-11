# Python-Spectometer
A spectometer analyzer written in python.  Takes a webcam, designed for the Public Lab Spectrometer, then on a slected horizontal line measures the intensity of the diffracted light.  The raw data is then smoothed several times, atempting to make a balance between clean data and detailed data, from there the different derivative's local maximas are found, returned, and displayed on the intensity graph.

###Dependencies
* Numpy
* Mathplotlib
* OpenCV

###Use

To use include "capture" hand call the function ***retrieve_peaks(callback, peak_order)***.

####Arguments

* \<callback\>:     A function with arguments (\<list\> peaks, \<int\> width)
  - \<peaks\> is a list of tuples containing (\<x pixel-coord of peak\>, \<percent intensity value of peak\>)
  - \<width> is the width in pixels of the webcam
            
* \<peak_order\>:   A list of derivative orders where the peaks will be obtained.
  - To find the maxium peak values it should be _[1]_

####Optional Arguments (kwargs)

* \<y\>:            The y-value of the webcam where the spectrum is analyzed from the webcam

* \<interval\>:     Milliseconds between webcam draws and function callback

* \<windows\>:      Boolean
  - *True*, for having the intensity graph and webcam image pop up.
  - *False*, for not having the windows popup
