Main colors extractor using SelfOrganizingMap
=============================================

Applies segmentation effect to an image with the specified number of colors and
extracts the best 2.

Flask app with HTML5 + Javascipt (using Camera API) frontend and Python
implementation of SOM.

Live Demo
---------

[dresser-toy-cam.herokuapp.com](http://dresser-toy-cam.herokuapp.com)

You have to trust me that no picture of you will ever be saved anywhere when
using this demo.

As far as I know, it works on `Google Chrome`, `Firefox`, `IE`, `Opera`, `Opera Mobile`.

Implementation details
----------------------

On each requests it trains a Self Organizing Map to cluster pixels in the image
based on their color and then scores the choosen centroids based on the number
of pixels that adhere to each one.

An additional weight is used to favor the mid-bright and nice colors over the
dark or too-bright and lame ones.

Performance
-----------

"Now, isn't that slow?" If you tried the demo you might actually had tought it
is broken. Well, it works but it is really-really slow.

It also gives approximative results, not always getting them right.

Conclusion
----------

It is a toy.

References
----------

Based on [SOM_Posterizer](https://github.com/iuliux/SOM_Posterizer)  
Uses [Camera.js](https://github.com/idevelop/camera.js)
