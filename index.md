---
layout: default
---

<!-- <div class="home"> -->

This is a series of self-study lectures on using Python for scientific 
computing at the graduate level in atomic physics and quantum optics.

<figure style="width: 33%; float: right;">
  <img  src="{{ site.baseurl }}/assets/gif/pixel_python.gif" />
</figure>

It aims to introduce you to using Python in both theoretical and experimental contexts through some common in-lab examples, like: 

- Reading data from a photon counter
- Binning and smoothing data
- Finding the steady state of an open quantum system
- Making a publication-quality plot

This is **not** an introduction to programming nor Python. You don't need to install anything to read the lectures, but if you want to download and use the example code it is a prerequisite that you already have Python working on your computer along with the standard scientific computing libraries: Numpy, Scipy and Matplotlib.

If you need help with Python or getting it installed there are many resources online, including the <a href="http://labs.physics.dur.ac.uk/computing/resources/python.php">Durham Physics Lab Guide to Python</a>. We&rsquo;ve listed more on the <a href="{{ site.baseurl }}/resources/">Resources</a> page.

The lectures are in four sections: I/O, Plotting, Data Analysis and Numerical Methods. 

  <!-- Each section has an associated problem for you to test your understanding.</p> -->

## Lectures

### I/O

  <ol>
    <li><a href="http://nbviewer.ipython.org/urls/dl.dropbox.com/s/nzeuexr03h3zmow/1_Reading-and-Writing-Files.ipynb?dl=0">Reading and Writing Files</a></li>
  </ol>

### Plotting

  <ol start="3">
    <li><a href="http://nbviewer.ipython.org/urls/dl.dropbox.com/s/nawiwv75cmk8p85/3_Lineshape-Comparison-and-Analysis.ipynb?dl=0">Lineshape Comparison and Analysis</a></li>
  </ol>

### Data Analysis

  <ol start="4">
    <li><a href="http://nbviewer.ipython.org/urls/dl.dropbox.com/s/e6xnie0z1g4j3mx/4_Smoothing-and-Binning-Data.ipynb">Smoothing and Binning Data</a></li>
  </ol>

### Integrating <abbr title="Ordinary Differential Equations">ODEs</abbr>

  <ol start="5">
    <li><a href="http://nbviewer.ipython.org/urls/dl.dropbox.com/s/24jy7cqans7lcyy/5_The-Explicit-Euler-Method-and-Order-of-Accuracy.ipynb">The Explicit Euler Method and Order of Accuracy</a></li>
    <li><a href="http://nbviewer.ipython.org/urls/dl.dropbox.com/s/1e3lwvtpqgo1789/6_The-Runge-Kutta-Method-Higher-Order-ODEs-and-Multistep-Methods.ipynb">The Runge-Kutta Method, Higher-Order ODEs and Multistep Methods</a></li>
    <li>Stiff Problems, Implicit Methods and Computational Cost{% include nf.html %}</li>
    <li><a href="http://nbviewer.ipython.org/urls/dl.dropbox.com/s/e14caw0z171igvo/8_Integrating-with-SciPy-and-QuTiP.ipynb">Integrating with SciPy and QuTiP</a></li>
  </ol>

<!-- Put in when the problems are ready -->

<!-- ## Problems

  <ol>
    <li>I/O{% include nf.html %}</li>
    <li>Plotting{% include nf.html %}</li>
    <li>Data Analysis{% include nf.html %}</li>
    <li>Numerical Methods{% include nf.html %}</li>
  </ol>
 -->
<!-- </div> -->