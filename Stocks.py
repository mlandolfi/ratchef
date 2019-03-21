# file to hold stocks class to store stock data
import json
import datetime
import statistics

""" notes
One would have to divide the standard deviation by the closing price to directly compare volatility for the two securities.
https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:standard_deviation_volatility
https://stattrek.com/statistics/dictionary.aspx?definition=z_score

Skewness:
when the plot is extended towards the right side more, it denotes positive skewness, wherein mode < median < mean. 
On the other hand, when the plot is stretched more towards the left direction, 
then it is called as negative skewness and so, mean < median < mode.

any symmetric data should have a skewness near zero. 
Negative values for the skewness indicate data that are skewed left (longer tail on left side of graph)
and positive values for the skewness indicate data that are skewed right. (longer tail on right side of graph)

Kurtosis: Measure of the peak of the graph


"""

class Stock(object):

	def __init__(self, symbol, dataFile):
		self.symbol = symbol
		self.volatility = 5	# 0-10
		self.values = {}	# key is time (second part of time), value is (value, volume)
		self.dataFile = dataFile
		self.dailyValuesInXY = False
		self.lastValueRecorded = ()
		self.previousValues = {}	# key is date, value is value {} ^^
		self.populationMeans = () #(volatility, volume) -> means of all recorded volatilities and volumes, including today
		self.stdDevs = () #(volatility, volume) -> numerical value used to indicate how widely individuals in a group vary. If individual observations vary greatly from the group mean, the standard deviation is big; and vice versa.
		self.zScores = () #(volatility, volume) -> z-score indicates how many standard deviations an element is from the mean, see website in notes for more info
		self.skewness = 0 #skewness is a measure of the asymmetry of the probability distribution of a real-valued random variable about its mean
		self.kurtosis = 0 #the sharpness of the peak of a frequency-distribution curve.
		# functions to execute on instantiation

	""" ############################ Functions that work with our data files ############################ """

	""" adds a time and value into self.values if it isn't already in there,
		also sets the self.lastValueRecorded to a tuple of (time, value, volume)
		if it's from a previous day it adds it to the previous day """
	def addValue(self, time, value, volume, day):
		if (day == datetime.date.today().strftime('%Y-%m-%d')):	# today so add it to self.values
			if (not time in self.values.keys()):
				self.lastValueRecorded = (value, volume, time)
				self.values[time] = (value, volume)
		else:	# not today so previous value
			if (not day in self.previousValues.keys()):
				self.previousValues[day] = {}
			if (not time in self.previousValues[day].keys()):
				self.previousValues[day][time] = (value, volume)

	""" returns a list of the daily values in (x,y) format where x is time ex. 9.55
		and y is the value of the stock at that time
		if this hasn't been called yet then it'll set self.dailyValuesInXY so it
		won't have to recalculate it next time """
	def getDailyValuesInXY(self):
		if (self.dailyValuesInXY):	return self.dailyValuesInXY
		xyValues = []
		for time in self.values:
			xValue = float(time.split(":")[0] + "." + time.split(":")[1])
			xyValues.append((xValue, self.values[time][0]))
		self.dailyValuesInXY = xyValues
		return xyValues

	def computeSkewnessLevel(self):

	""" ############################ Helper functions for update functions ############################ """

	""" returns a list containing all recorded values for this stock if index is 0, 
		or all recorded volumes for this stock if index is 1"""
	def collectRecordedValues(self, index):
		retList = []
		#going through all of today's recorded values if index is 0 or volumes if index 1
		for time, valueTuple in self.values.items():
			retList.append(valueTuple[index]) 
		#going through all of our past day recorded volumes
		for day in self.previousValues:
			for time in day:
				for valueTuple in time:
					retList.append(valueTuple[index]) ####Mike check this against what's commented
		"""
		for day, dayValues in self.previousValues.items(): 	
			for time, valueTuple in dayValues.items():
				retList.append(valueTuple[index]) 
		"""
		return retList

	"""Calculates z-score for this stock. Requires that self.populationMeans and self.stdDevs 
		have been set and updated.
		index is 0 if we are finding z-score of values (for volatility), 1 if z-score of volumes"""
	def zScore(self, index):
		#z = (X - μ) / σ, where X is latest recorded value, μ is the population mean, and σ is the standard deviation
		return (self.lastValueRecorded[index] - self.populationMeans[index]) / self.stdDevs[index]

	""" ############################ Update stock functions ############################ """

	"""Updates the population mean (all recorded items, from today and past). index 0 for values, 1 for volumes
		currenList is obtained from collectRecordedValuesFunction, which has the same index 0/1 rules."""
	def updatePopulationMean(self, index, currentList):
		self.populationMeans[index] = statistics.mean(currentList)

	"""Updates the stdDev (all recorded items, from today and past). index 0 for values, 1 for volumes"""
	def updateStdDev(self, index, currentList):
		self.stdDevs[index] = statistics.stddev(currentList)

	"""Requires that updatePopulationMeans/updateStdDev have both been called, in that order.
		Updates z-score for this stock. 
		index is 0 if we are finding z-score of values (for volatility), 1 if z-score of volumes"""
	def updateZScore(self, index, currentList):
		self.zScores[index] = zScore(index)

	"""Requires that updatePopulationMean() and updateStdDev() have both been called
		skewness of a normal distribution is 0
		negative values for skewness indicate that the data is skewed left
		positive values for skewness indicate that the data is skewed right"""
	def updateSkewness(self):
		#y_bar is mean, s is stdDev, N is number of data points
		num = 0
		denom = 0
		
		self.skewness = 


	def __str__(self):
		return self.symbol