import numpy as np
import pandas as pd
import math

# Function 1: Separation between star and candidate
#     Inputs: Candidate x-coordinate, candidate y-coordinate
#     Flags: Star x-coordinate, star y-coordinate
#     Returns: Separation between star and candidate in pixels
def sep_Pix(CandidateX, CandidateY, StarX, StarY):
    return math.sqrt(pow((CandidateX - StarX),2) + pow((CandidateY - StarY),2))

# Function 2: Convert a separation in pixels to a separation in arcseconds
#     Inputs: Separation in pixels
#     Flags: Pixel scale in arcseconds/pixel
#     Returns: Separation in arcseconds
def sep_Arcsec(SeparationPix, PixelScale):
    return SeparationPix * PixelScale

# Function 3: Convert a separation in arcseconds to a separation in AU
#     Inputs: Separation in arcseconds, distance in parsecs to star
#     Outputs: Separation in AU
def sep_AU(SeparationArcsec, Distance):
    return SeparationArcsec * Distance

# Function 4: Estimate the flux ratio of a star and a candidate companion
#     Inputs: Flux of star (counts), flux of candidate companion (counts)
#     Returns: Flux ratio
def fluxRatio(StarFlux, CandidateFlux):
    return StarFlux / CandidateFlux 

# Function 5: Determine ∆m between the candidate and companion
#     Inputs: Flux ratio
#     Returns: ∆m
def deltaM(FluxRatio):
    return 2.5 * math.log10(FluxRatio)

# Function 6: Calculate the absolute magnitude of the candidate
#     Inputs: ∆m, absolute magnitude of the star
#     Returns: Absolute magnitude of the candidate
def absMagCandidate(DeltaM, AbsMagStar):
    return AbsMagStar + DeltaM

# As a bonus activity, see if you can set up these functions below with as few lines as possible. This will involve calling functions 1-6 within your functions.
# Function 7: Calculate a separation between a star and candidate in AU
#     Inputs: Candidate x-coordinate, candidate y-coordinate, distance to star
#     Flags: Star x-coordinate, star y-coordinate
#     Returns: Separation in AU
#def sep_AU(CandidateX, CandidateY, StarX, StarY, Distance):
#    return sep_AU(sep_Arcsec(sep_Pix(CandidateX, CandidateY, StarX, StarY), PixelScale), Distance)

# Function 8: Calculate the absolute magnitude of the candidate
#     Inputs: Flux of star, flux of candidate companion, absolute magnitude of the star
#     Returns: Absolute magnitude of the candidate
def absMagCandidate2(StarFlux, CandidateFlux, AbsMagStar):
    return absMagCandidate(deltaM(fluxRatio(StarFlux, CandidateFlux)), AbsMagStar)

# Some code for testing the functions
# Was used for class on 7/5/23
# sp = math.sqrt(pow(4.893,2) + pow(21.920,2))
# time = 9
# total_pm = time * sp
# print(total_pm)
# print(sep_Arcsec(total_pm, 0.01)*10)
# # Stop the program
# exit()

# Open the Google Sheet containing the data
#     Flags: Google Sheet ID, Google Sheet name
#     Returns: Google Sheet
#def openGoogleSheet(GoogleSheetID, GoogleSheetName):
#   return openGoogleSheet(GoogleSheetID, GoogleSheetName)

# Test the functions by calling the data from the Google Sheet and 
# comparing the results. Print out a message with the results.
# Note that the Google Sheet fields needed to be rearranged 
# to allow for processing, so I reformatted it and exported to
# a CSV file.

# Read in the data from the Google Sheet
myData = pd.read_csv("Python Copy of SES294 Measurements - Star_Data.csv")

# For each row in the data, calculate the separation between the star and candidate in pixels, arcseconds, AU, FluxRatio, DeltaM, and Absolute Magnitude of the candidate 
for i in range(len(myData)):
    myData.loc[i, 'CalcSeparationPix'] = sep_Pix(myData.loc[i, 'CandidateX'], myData.loc[i, 'CandidateY'], myData.loc[i, 'StarX'], myData.loc[i, 'StarY'])
    myData.loc[i, 'CalcSeparationArcsec'] = sep_Arcsec(myData.loc[i, 'SeparationPix'], myData.loc[i, 'PixelScale'])
    myData.loc[i, 'CalcSeparationAU'] = sep_AU(myData.loc[i, 'SeparationArcsec'], myData.loc[i, 'Distance'])
    myData.loc[i, 'CalcFluxRatio'] = fluxRatio(myData.loc[i, 'StarFlux'], myData.loc[i, 'CandidateFlux'])
    myData.loc[i, 'CalcDeltaM'] = deltaM(myData.loc[i, 'CalcFluxRatio'])
    myData.loc[i, 'CalcAbsMagCandidate1'] = absMagCandidate(myData.loc[i, 'DeltaM'], myData.loc[i, 'AbsMagStar'])
    myData.loc[i, 'CalcAbsMagCandidate2'] = absMagCandidate2(myData.loc[i, 'StarFlux'], myData.loc[i, 'CandidateFlux'], myData.loc[i, 'AbsMagStar'])

# Make sure everything is rounded to 7 decimal places
myData = np.around(myData, decimals=2)
print(myData)

# For each calculated value, compare it to the value in the Google Sheet and print out whether it matches or not
for i in range(len(myData)):
    if myData.loc[i, 'SeparationPix'] == myData.loc[i, 'CalcSeparationPix']:
        # Print out the calculated value
        print("CalSeparationPix: " + str(myData.loc[i, 'CalcSeparationPix']))
        print("Separation in pixels matches for row " + str(i))
    else:
        print(myData.loc[i, 'SeparationPix'])
        print(myData.loc[i, 'CalcSeparationPix'])
        print("Separation in pixels does not match for row " + str(i))
    if myData.loc[i, 'SeparationArcsec'] == myData.loc[i, 'CalcSeparationArcsec']:
        # Print out the calculated value
        print("CalSeparationArcsec: " + str(myData.loc[i, 'CalcSeparationArcsec']))
        print("Separation in arcseconds matches for row " + str(i))
    else:
        print(myData.loc[i, 'SeparationArcsec'])
        print(myData.loc[i, 'CalcSeparationArcsec'])
        print("Separation in arcseconds does not match for row " + str(i))
    if myData.loc[i, 'SeparationAU'] == myData.loc[i, 'CalcSeparationAU']:
        # Print out the calculated value
        print("CalSeparationAU: " + str(myData.loc[i, 'CalcSeparationAU']))
        print("Separation in AU matches for row " + str(i))
    else:
        print(myData.loc[i, 'SeparationAU'])
        print(myData.loc[i, 'CalcSeparationAU'])
        print("Separation in AU does not match for row " + str(i))
    # Note: The following rounding is needed due to rounding errors in the Google Sheet vs. this code.
    #       The rounding errors are small enough that they do not affect the final calculations.
    #       This code could be improved to handle this problem more generally.
    if round(myData.loc[i, 'FluxRatio'], -2) == round(myData.loc[i, 'CalcFluxRatio'], -2):
        # Print out the calculated value
        print("CalcFluxRatio: " + str(myData.loc[i, 'CalcFluxRatio']))
        print("Flux ratio matches for row " + str(i))
    else:
        print(myData.loc[i, 'FluxRatio'])
        print(myData.loc[i, 'CalcFluxRatio'])
        print("Flux ratio does not match for row " + str(i))
    if myData.loc[i, 'DeltaM'] == myData.loc[i, 'CalcDeltaM']:
        # Print out the calculated value
        print("CalcDeltaM: " + str(myData.loc[i, 'CalcDeltaM']))
        print("Delta M matches for row " + str(i))
    else:
        print(myData.loc[i, 'DeltaM'])
        print(myData.loc[i, 'CalcDeltaM'])
        print("Delta M does not match for row " + str(i))
    if myData.loc[i, 'AbsMagCandidate'] == myData.loc[i, 'CalcAbsMagCandidate1']:
        # Print out the calculated value
        print("CalcAbsMagCandidate1: " + str(myData.loc[i, 'CalcAbsMagCandidate1']))
        print("Absolute magnitude of candidate matches for row " + str(i))
    else:
        print(myData.loc[i, 'AbsMagCandidate'])
        print(myData.loc[i, 'CalcAbsMagCandidate1'])
        print("Absolute magnitude of candidate does not match for row " + str(i))
    if myData.loc[i, 'AbsMagCandidate'] == myData.loc[i, 'CalcAbsMagCandidate2']:
        # Print out the calculated value
        print("CalcAbsMagCandidate2: " + str(myData.loc[i, 'CalcAbsMagCandidate2']))
        print("Absolute magnitude of candidate matches for row " + str(i))
    else:
        print(myData.loc[i, 'AbsMagCandidate'])
        print(myData.loc[i, 'CalcAbsMagCandidate2'])
        print("Absolute magnitude of candidate does not match for row " + str(i))
    print("\n")
