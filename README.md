# Python-Spectometer
A spectometer analyzer written in python

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
