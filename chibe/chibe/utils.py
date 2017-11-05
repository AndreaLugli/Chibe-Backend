def get_percentuale(percentuale_marketing):
	if percentuale_marketing <= 6.0:
		percentuale = 1
	elif (percentuale_marketing > 6.0) and (percentuale_marketing < 12.0):
		percentuale = "1+"
	elif percentuale_marketing == 12.0:
		percentuale = 2
	elif (percentuale_marketing > 12.0) and (percentuale_marketing < 18.0):
		percentuale = "2+"
	elif percentuale_marketing == 18.0:
		percentuale = 3	
	elif (percentuale_marketing > 18.0) and (percentuale_marketing < 24.0):
		percentuale = "3+"
	elif percentuale_marketing == 24.0:
		percentuale = 4	
	elif (percentuale_marketing > 24.0) and (percentuale_marketing < 30.0):
		percentuale = "4+"
	elif percentuale_marketing == 30.0:
		percentuale = 5	
	elif (percentuale_marketing > 30.0) and (percentuale_marketing < 36.0):
		percentuale = "5+"
	elif percentuale_marketing == 36.0:
		percentuale = 6	
	elif (percentuale_marketing > 36.0) and (percentuale_marketing < 42.0):
		percentuale = "6+"
	elif percentuale_marketing == 42.0:
		percentuale = 7	
	elif (percentuale_marketing > 42.0) and (percentuale_marketing < 48.0):
		percentuale = "7+"
	elif percentuale_marketing == 48.0:
		percentuale = 8	
	elif (percentuale_marketing > 48.0) and (percentuale_marketing < 54.0):
		percentuale = "8+"
	elif percentuale_marketing == 54.0:
		percentuale = 9	
	elif (percentuale_marketing > 54.0) and (percentuale_marketing < 60.0):
		percentuale = "9+"
	elif percentuale_marketing == 60.0:
		percentuale = 10
	elif (percentuale_marketing > 60.0) and (percentuale_marketing < 66.0):
		percentuale = "10+"
	elif percentuale_marketing == 66.0:
		percentuale = 11
	elif (percentuale_marketing > 66.0) and (percentuale_marketing < 72.0):
		percentuale = "11+"
	elif percentuale_marketing == 72.0:
		percentuale = 12
	elif (percentuale_marketing > 72.0) and (percentuale_marketing < 78.0):
		percentuale = "12+"
	elif percentuale_marketing == 78.0:
		percentuale = 13
	elif (percentuale_marketing > 78.0) and (percentuale_marketing < 84.0):
		percentuale = "13+"
	elif percentuale_marketing == 84.0:
		percentuale = 14
	elif (percentuale_marketing > 84.0) and (percentuale_marketing < 90.0):
		percentuale = "14+"
	elif percentuale_marketing == 90.0:
		percentuale = 15
	elif (percentuale_marketing > 90.0) and (percentuale_marketing < 96.0):
		percentuale = "15+"
	elif percentuale_marketing == 96.0:
		percentuale = 16

	return str(percentuale)