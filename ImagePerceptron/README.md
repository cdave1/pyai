Perceptron
==========

A python implementation of a linear feedforward classifier, AKA [perceptron](http://en.wikipedia.org/wiki/Perceptron).

Usage
=====

Use the following to run the program:

    % python perceptron.py training_images_filename [maximum_epochs] [testing_filename]


Example (this will produce output similar to that found in "sampleoutput.txt"):
    % python perceptron.py image.data 150

Notes
=====

- The only required input parameter is "training_filename"
- If "maximum_epochs" is not specified, the percepton will go through a default maximum of 100 epochs.
- For the "testing_filename" to work, "maximum_epochs" must also be specified.
- The program will crash if no files are specified.


