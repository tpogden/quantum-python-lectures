from pylab import figure,clf,draw,show,subplot2grid,setp
from pylab import exp,array,arange,zeros,linspace
from numpy import random

from scipy.optimize import curve_fit
from scipy.signal import fftconvolve as conv
from scipy.interpolate import interp1d as interp



def gaussian(x,c,w):
	""" Analytic Gaussian function with amplitude 'a', center 'c', width 'w'.
		The FWHM of this fn is 2*sqrt(2*log(2))*w 
		NOT NORMALISED """
	G = exp(-(x-c)**2/(2*w**2))
	G /= G.max()
	return G
	
def lorentzian(x,c,w):
	""" Analytic Lorentzian function with amplitude 'a', center 'c', width 'w'.
		The FWHM of this fn is 2*w 
		NOT NORMALISED """
	L = w**2 / ( (x-c)**2 + w**2 )
	L /= L.max()
	return L
	
def voigt(x,c1,w1,c2,w2):
	""" Voigt function: convolution of Lorentzian and Gaussian.
		Convolution implemented with the FFT convolve function in scipy.
		NOT NORMALISED """
	
	### Create larger array so convolution doesn't screw up at the edges of the arrays
	# this assumes nicely behaved x-array...
	# i.e. x[0] == x.min() and x[-1] == x.max(), monotonically increasing
	dx = (x[-1]-x[0])/len(x)
	xp_min = x[0] - len(x)/3 * dx
	xp_max = x[-1] + len(x)/3 * dx
	xp = linspace(xp_min,xp_max,3*len(x))
	
	L = lorentzian(xp,c1,w1)
	G = gaussian(xp,c2,w2)
	
	#convolve
	V = conv(L,G,mode='same')
	
	#normalise to unity height !!! delete me later !!!
	V /= V.max()
	
	#create interpolation function to convert back to original array size
	fn_out = interp(xp,V)
	
	return fn_out(x)
	
def generate_lineshapes(x,a,b,c,d):
	return lorentzian(x,a,b),gaussian(x,c,d),voigt(x,a,b,c,d)

def compare_lineshapes(wL,wG):
	""" create a plot comparing voigt with lorentzian and gaussian
		wL and wG are widths of Lorentzian and Gaussian, respectively """
		
	# generate some lineshape to analyse later
	x = arange(-20,20,0.01)
	yL,yG,yV = generate_lineshapes(x,0,wL,0,wG)
	y_noise = random.randn(len(x))*0.1
	yV += y_noise

	fig = figure(2)
	clf()

	ax = fig.add_subplot(111)
	
	ax.plot(x,yL/yL.max(),'b',lw=2,label='Lorentzian')
	ax.plot(x,yG/yG.max(),'r',lw=2,label='Gaussian')
	ax.plot(x,yV/yV.max(),'g--',lw=2,label='Voigt')
	
	# Add legend: loc=0 means find best position
	ax.legend(loc=0)
	
	ax.set_xlabel('Detuning (arb.)')
	ax.set_ylabel('Intensity (arb.)')
	
def fit_lineshape(x,y):
	""" Given array of x and y values, find best fit to 
		all three functions: Lorentzian, Gaussian and Voigt
		then compare the residuals for all 3. """
	
	### Create figure panels using subplot2grid
	fig = figure(1,figsize=(6,7))
	fig.subplots_adjust(left=0.15,bottom=0.08,top=0.97)
	#rows
	yy = 8
	#cols
	xx = 8
	
	#main panel
	ax = subplot2grid((yy,xx),(0,0),rowspan=yy-3,colspan=xx-1)

	#3 residual panels
	ax_LRes = subplot2grid((yy,xx),(yy-3,0),rowspan=1,colspan=xx-1,sharex=ax)	
	ax_GRes = subplot2grid((yy,xx),(yy-2,0),rowspan=1,colspan=xx-1,sharex=ax,sharey=ax_LRes)	
	ax_VRes = subplot2grid((yy,xx),(yy-1,0),rowspan=1,colspan=xx-1,sharex=ax,sharey=ax_LRes)

	#residual histogram panels
	ax_LHist = subplot2grid((yy,xx),(yy-3,xx-1),rowspan=1,colspan=1,sharey=ax_LRes)
	ax_GHist = subplot2grid((yy,xx),(yy-2,xx-1),rowspan=1,colspan=1,sharey=ax_GRes)
	ax_VHist = subplot2grid((yy,xx),(yy-1,xx-1),rowspan=1,colspan=1,sharey=ax_VRes)
	
	#turn off unwanted axes labels
	setp(ax_LRes.get_xticklabels(),visible=False)
	setp(ax_GRes.get_xticklabels(),visible=False)
	setp(ax.get_xticklabels(),visible=False)
	setp(ax_LHist.get_yticklabels(),visible=False)
	setp(ax_GHist.get_yticklabels(),visible=False)
	setp(ax_VHist.get_yticklabels(),visible=False)
	setp(ax_LHist.get_xticklabels(),visible=False)
	setp(ax_GHist.get_xticklabels(),visible=False)
	setp(ax_VHist.get_xticklabels(),visible=False)

	ax.set_ylabel('Intensity (arb.)')
	ax_VRes.set_xlabel('Detuning (arb.)')
	ax_LRes.set_ylabel('L.')
	ax_GRes.set_ylabel('G.')
	ax_VRes.set_ylabel('V.')
	
	### </ figure creation >
	
	# plot initial data
	ax.plot(x,y,'k.',alpha=0.6)
	
	# FITTING:
	
	# 1. Lorentzian
	pin = [0,1]
	popt, perr = curve_fit(lorentzian,x,y,p0=pin)
	y_L = lorentzian(x,*popt)
	y_LRes = y-y_L
	
	# 2. Gaussian
	pin = [0,1]
	popt, perr = curve_fit(gaussian,x,y,p0=pin)
	y_G = gaussian(x,*popt)
	y_GRes = y-y_G

	# 3. Voigt
	pin = [0,1,0,1]
	popt, perr = curve_fit(voigt,x,y,p0=pin)
	y_V = voigt(x,*popt)
	y_VRes = y-y_V
	
	
	## PLOTTING
	
	
	# add fits to main panel
	ax.plot(x,y_L,'b',lw=2,label = 'Lorentzian')
	ax.plot(x,y_G,'r',lw=2,label = 'Gaussian')
	ax.plot(x,y_V,'g--',lw=4,label = 'Voigt')

	ax.legend(loc=0)	

	# add residuals to sub-panels
	for axis in [ax_LRes,ax_GRes,ax_VRes,ax_LHist,ax_GHist,ax_VHist]:
		axis.axhline(0,color='k',linestyle='--')

	ax_LRes.plot(x,y_LRes,'b.')
	ax_GRes.plot(x,y_GRes,'r.')
	ax_VRes.plot(x,y_VRes,'g.')
	
	# Histograms
	histrange = (-0.15,0.15)
	ax_LHist.hist(y_LRes,bins=25,orientation='horizontal', \
			fc='b',alpha=0.6,range=histrange)
	ax_GHist.hist(y_GRes,bins=25,orientation='horizontal', \
			fc='r',alpha=0.6,range=histrange)
	ax_VHist.hist(y_VRes,bins=25,orientation='horizontal', \
			fc='g',alpha=0.6,range=histrange)

	show()
	
def main(wL,wG):
	#generate data
	x = arange(-30,30,0.2)
	yL,yG,yV = generate_lineshapes(x,0,wL,0,wG)
	y_noise = random.randn(len(x))*0.03
	yV += y_noise
	
	fit_lineshape(x,yV)
	
			
	
	
	