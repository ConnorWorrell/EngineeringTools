#!/usr/bin/python

# This program is used to calculate the profiles for threads and 
#     thread on thread interactions.

#Copyright (C) 2022 Connor Worrell
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see http://www.gnu.org/licenses/.

print ("""\nThreadCalculator.py Calculator  Copyright (C) 2022 Connor Worrell 
This program comes with ABSOLUTELY NO WARRANTY; for details refer to the license file.\n""")

import math

class ThreadProfile:
    def __init__(self, threadText, rightHand=True):
        self.threadText = threadText
        self.maxMajorDiameter = None
        self.nominalMajorDiameter = None
        self.minMajorDiameter = None
        self.maxPitchDiameter = None
        self.nominalPitchDiameter = None
        self.minPitchDiameter = None
        self.maxMinorDiameter = None
        self.nominalMinorDiameter = None
        self.minMinorDiameter = None
        self.maxRootDiameter = None
        self.minRootDiameter = None
        self.nominalRootDiameter = None
        self.tensileStressArea = None
        self.isExternal = None
        self.tpi = None
        self.pitch = None
        self.units = None
        self.rightHand = rightHand
        self.threadCallout = None

        if self.threadText is not None:
            self.IdentifyUNThread(self.threadText, self.isExternal)

    def IdentifyUNThread(self, thread, isExternal=None):
        # Assuming Unified National Thread Series
        self.units = "in"

        # Replace explicitely defined numbers:
        HoleLookup = {"#0": .06, "#1": .073, "#2": .086, "#3": .099, "#4": .112, "#5": .125, "#6": .128, "#8": .164, "#10": .19, "#12": .126}
        for i in HoleLookup.keys():
            if i in thread:
                thread = thread.replace(i, str(HoleLookup[i]))

        threadsplit = thread.replace(" ","-").split("-")

        MajorDiamStr = threadsplit[0]
        if "/" in MajorDiamStr:
            MajorDiam = float(MajorDiamStr.split("/")[0]) / float(MajorDiamStr.split("/")[1])
        else:
            MajorDiam = str(MajorDiamStr)
        TPI = int(threadsplit[1])

        ThreadDensityLookup = {
                # Thread Identifier | Density | Basic Major Diam
                "0-80":    ["UNF" , .0600],
                "1-64":    ["UNC" , .0730],
                "1-72":    ["UNF" , .0730],
                "2-56":    ["UNC" , .0860],
                "2-64":    ["UNF" , .0860],
                "3-48":    ["UNC" , .0990],
                "3-56":    ["UNF" , .0990],
                "4-40":    ["UNC" , .1120],
                "4-48":    ["UNF" , .1120],
                "5-40":    ["UNC" , .1250],
                "5-44":    ["UNF" , .1250],
                "6-32":    ["UNC" , .1280],
                "6-40":    ["UNF" , .1280],
                "8-32":    ["UNC" , .1640],
                "8-36":    ["UNF" , .1640],
                "10-24":   ["UNC" , .1900],
                "10-32":   ["UNF" , .1900],
                "12-24":   ["UNC" , .2160],
                "12-28":   ["UNF" , .2160],
                "12-32":   ["UNEF", .2160],
                "1/4-20":  ["UNC" , .2500],
                "1/4-28":  ["UNF" , .2500],
                "1/4-32":  ["UNEF", .2500],
                "5/16-18": ["UNC" , .3125],
                "5/16-24": ["UNF" , .3125],
                "5/16-32": ["UNEF", .3125],
                "3/8-16":  ["UNC" , .3750],
                "3/8-24":  ["UNF" , .3750],
                "3/8-32":  ["UNEF", .3750],
                "7/16-14": ["UNC" , .4375],
                "7/16-20": ["UNF" , .4375],
                "7/16-28": ["UNEF", .4375],
                "1/2-13":  ["UNC" , .5000],
                "1/2-20":  ["UNF" , .5000],
                "1/2-28":  ["UNEF", .5000],
                "9/16-12": ["UNC" , .5625],
                "9/16-18": ["UNF" , .5625],
                "9/16-24": ["UNEF", .5625],
                "5/8-11":  ["UNC" , .6250],
                "5/8-18":  ["UNF" , .6250],
                "5/8-24":  ["UNEF", .6250],
                "3/4-10":  ["UNC" , .7500],
                "3/4-16":  ["UNF" , .7500],
                "3/4-20":  ["UNEF", .7500],
                "7/8-9":   ["UNC" , .8750],
                "7/8-14":  ["UNF" , .8750],
                "7/8-20":  ["UNEF", .8750],
                "1-8":     ["UNC" , 1.000],
                "1-12":    ["UNF" , 1.000],
                "1-20":    ["UNEF", 1.000]
                }

        DiamTPI = "-".join(threadsplit[0:2])
        if DiamTPI in ThreadDensityLookup.keys():
                ThreadDensity = ThreadDensityLookup[DiamTPI][0]
                MajorDiam = ThreadDensityLookup[DiamTPI][1]
                DiameterPitchOverride = DiamTPI
        else:
            ThreadDensity = "UNS"
            MajorDiam = float(MajorDiam)
            TPI = float(TPI)
            DiameterPitchOverride = None

        self.tpi = float(TPI)
        self.pitch = 1/self.tpi

        ClassFinder = " ".join(threadsplit[2:])

        if "1" in ClassFinder:
            Class = 1
        elif "2" in ClassFinder:
            Class = 2
        elif "3" in ClassFinder:
            Class = 3
        elif "4" in ClassFinder:
            Class = 4
        elif "5" in ClassFinder:
            Class = 5
        else:
            Class = 2 # Assume Class 2, standard

        if isExternal == False or "b" in thread.lower(): # Assume from input, default is internal
            ThreadSide = "B"
            self.isExternal = False
        else:
            ThreadSide = "A"
            self.isExternal = True

        # Check for R and J thread callouts
        if "r" in thread.lower() and ThreadSide == "A": # No UNR spec for Internal threads
            ThreadDensity = ThreadDensity.replace("UN","UNR")
        elif "j" in thread.lower() and Class >= 2:
            ThreadDensity = ThreadDensity.replace("UN","UNJ")
        elif "j" in thread.lower() and Class == 1:
            print("UNJ not compatable with Class 1 thread")

        # Thread Allowance Calc
        BasicPitchDiam = MajorDiam - 0.64952 / TPI
        BasicMajorDiam = MajorDiam

        EngagementLength = BasicMajorDiam # For tolerance calc, applicable up to 1.5 Major diams)
        Class2APitchDiamTolerance = 0.0015*BasicMajorDiam**(1/3) + 0.0015*EngagementLength**(1/2) + 0.015 * (1/TPI)**(2/3)

        MaxRootRadius = None

        if ThreadSide == "A": # External Thread (bolt)
            BasicMinorDiam = BasicMajorDiam - 3*3**(1/2)/(4*TPI)
            if Class == 1:
                MajorDiamTolerance = 0.090 * (1/TPI)**(2/3)
            elif Class == 2 or Class == 3:
                MajorDiamTolerance = 0.060 * (1/TPI)**(2/3)

            if Class == 1:
                PitchDiamTolerance = 1.5*Class2APitchDiamTolerance
                Allowance = .3 * Class2APitchDiamTolerance
            elif Class == 2:
                PitchDiamTolerance = Class2APitchDiamTolerance
                Allowance = .3 * Class2APitchDiamTolerance
            elif Class == 3:
                PitchDiamTolerance = .75*Class2APitchDiamTolerance
                Allowance = 0

            MinorDiamTolerance = PitchDiamTolerance + .21650635 * (1/TPI) #UN

            MaxMajorDiam = BasicMajorDiam - Allowance
            MinMajorDiam = MaxMajorDiam - MajorDiamTolerance
            MaxPitchDiam = BasicPitchDiam - Allowance
            MinPitchDiam = MaxPitchDiam - PitchDiamTolerance
            if "R" in ThreadDensity:
                if Class <= 2:
                    MaxMinorDiam = BasicMinorDiam - Allowance - .10825318 * (1/TPI)
                else:
                    MaxMinorDiam = BasicMinorDiam - .10825318 * (1/TPI)
                MaxRootRadius = .18042196 * (1/TPI)
                MinMinorDiam = MinPitchDiam - .64951905 * (1/TPI)
            elif "J" in ThreadDensity:
                if Class == 2:
                    MaxMinorDiam = BasicPitchDiam - Allowance - .50518 * (1/TPI)
                    MinMinorDiam = BasicPitchDiam - 1.3 * Class2APitchDiamTolerance - .5658 * (1/TPI)
                elif Class == 3:
                    MaxMinorDiam = BasicPitchDiam - .50518 * (1/TPI)
                    MinMinorDiam = BasicPitchDiam - .75 * Class2APitchDiamTolerance - .5658 * (1/TPI)
                MaxRootRadius = .15011107 * (1/TPI)
            else:
                MaxMinorDiam = BasicMinorDiam + Allowance #Note the minor diameter are slightly off from refrences
                MinMinorDiam = MaxMinorDiam - MinorDiamTolerance

            MinMinorDiamRounding1 = 4
            MinMinorDiamRounding2 = 4
            MaxMinorDiamRounding = 4

        elif ThreadSide == "B": # Internal thread (nut)
            BasicMinorDiam = MajorDiam - 1.08253175 * (1/TPI)
            Allowance = 0

            if Class == 1:
                PitchDiamTolerance = 1.95 * Class2APitchDiamTolerance
            elif Class == 2:
                PitchDiamTolerance = 1.3 * Class2APitchDiamTolerance
            elif Class == 3:
                PitchDiamTolerance = .975 * Class2APitchDiamTolerance

            MajorDiamTolerance = .14433757*(1/TPI) + PitchDiamTolerance

            if Class == 1 or Class == 2:
                if MajorDiam-.25 < .001:
                    MinorDiamTolerance = .0500*(1/TPI)**(2/3) + .03*1/(TPI * BasicMajorDiam) - .002
                    if MinorDiamTolerance > .3940*(1/TPI):
                        MinorDiamTolerance = .3940*(1/TPI)
                    elif MinorDiamTolerance < .25*(1/TPI) - .4 * (1/TPI)**2:
                        MinorDiamTolerance = .25*(1/TPI) - .4 * (1/TPI)**2
                elif TPI >= 4:
                    MinorDiamTolerance = .25*(1/TPI)-.4*(1/TPI)**2
                else:
                    MinorDiamTolerance = .15*(1/TPI)
            elif Class == 3:
                MinorDiamTolerance = .05*(1/TPI)**(2/3) + .03*1/(TPI * MajorDiam) - .002

                if MinorDiamTolerance > .394*(1/TPI):
                    MinorDiamTolerance = .394*(1/TPI)
                elif MinorDiamTolerance < .23*(1/TPI) - 1.5*(1/TPI)**2 and TPI >= 13:
                    MinorDiamTolerance = .23*(1/TPI) - 1.5*(1/TPI)**2
                elif MinorDiamTolerance < .12*(1/TPI) and TPI < 13:
                    MinorDiamTolerance = .12*(1/TPI)

            MinMajorDiam = BasicMajorDiam - Allowance
            MaxMajorDiam = MinMajorDiam + MajorDiamTolerance
            MinPitchDiam = BasicPitchDiam - Allowance
            MaxPitchDiam = MinPitchDiam + PitchDiamTolerance
            MinMinorDiam = BasicMinorDiam + Allowance #Note the minor diameter are slightly off from refrences
            MaxMinorDiam = MinMinorDiam + MinorDiamTolerance

            if "J" in ThreadDensity:
                MinMinorDiam = MinMajorDiam - .97427858 * (1/TPI)

            if MajorDiam < .1380:
                MinMinorDiamRounding1 = 4
                MinMinorDiamRounding2 = 4
                MaxMinorDiamRounding = 4
            elif Class == 1 or Class == 2:
                MinMinorDiamRounding1 = 3
                MinMinorDiamRounding2 = 3
                MaxMinorDiamRounding = 3
            elif Class == 3 and "J" in ThreadDensity:
                MinMinorDiamRounding1 = 4
                MinMinorDiamRounding2 = 4
                MaxMinorDiamRounding = 4
            else:
                MinMinorDiamRounding1 = 3
                MinMinorDiamRounding2 = 4
                MaxMinorDiamRounding = 4

        BasicMajorDiam = round(BasicMajorDiam,4)
        MaxMajorDiam = round(MaxMajorDiam,4)
        MinMajorDiam = round(MinMajorDiam,4)
        BasicPitchDiam = round(BasicPitchDiam,4)
        MaxPitchDiam = round(MaxPitchDiam,4)
        MinPitchDiam = round(MinPitchDiam,4)
        BasicMinorDiam = round(BasicMinorDiam,4)
        MaxMinorDiam = round(MaxMinorDiam, MaxMinorDiamRounding)
        MinMinorDiam = round(MinMinorDiam, MinMinorDiamRounding1)

        self.maxMajorDiameter = MaxMajorDiam
        self.nominalMajorDiameter = BasicMajorDiam
        self.minMajorDiameter = MinMajorDiam
        self.maxPitchDiameter = MaxPitchDiam
        self.nominalPitchDiameter = BasicPitchDiam
        self.minPitchDiameter = MinPitchDiam
        self.maxMinorDiameter = MaxMinorDiam
        self.nominalMinorDiameter = BasicMinorDiam
        self.minMinorDiameter = MinMinorDiam
        self.maxRootDiameter = MaxRootRadius
        self.minRootDiameter = None
        self.nominalRootDiameter = None

        if ThreadSide == "A":
            TensileStressAreaSmall = round((math.pi/4)*(MajorDiam - 0.938194*(1/TPI))**2,4)
            TensileStressAreaLarge = round(math.pi*(MinPitchDiam/2 - 0.16238/TPI)**2,4)

            self.tensileStressArea = min(TensileStressAreaSmall, TensileStressAreaLarge)
        else:
            self.tensileStressArea = None
        if DiameterPitchOverride is not None:
            threadCallout = DiameterPitchOverride
        else:
            threadCallout = str(MajorDiam) + "-" + str(TPI)
        threadCallout = threadCallout + " " + str(ThreadDensity) + "-" + str(Class) + ThreadSide
        if self.rightHand == False:
            threadCallout = threadCallout + "-" + "LH"

        self.threadCallout = threadCallout

        return

    def printInfo(self):
        print("Input Text: ", str(self.threadText))
        print("Callout Text:", str(self.threadCallout))
        print("External Thread:", str(self.isExternal))
        print("Right Handed:", str(self.rightHand))
        print("Threads Per Inch:", str(self.tpi), "1/"+self.units)
        print("Pitch:", str(self.pitch), self.units)
        print("Major Diameter:", str(self.nominalMajorDiameter), self.units)
        print("    Max:", str(self.maxMajorDiameter), self.units)
        print("    Min:", str(self.minMajorDiameter), self.units)
        print("Nominal Diameter:", str(self.nominalPitchDiameter), self.units)
        print("    Max:", str(self.maxPitchDiameter), self.units)
        print("    Min:", str(self.minPitchDiameter), self.units)
        print("Minor Diameter:", str(self.nominalMinorDiameter), self.units)
        print("    Max:", str(self.maxMinorDiameter), self.units)
        print("    Min:", str(self.minMinorDiameter), self.units)
        print("Root Diameter:", str(self.maxRootDiameter), self.units)
        print("    Max:", str(self.minRootDiameter), self.units)
        print("    Min:", str(self.nominalRootDiameter), self.units)
        print("Tensile Stress Area:", str(self.tensileStressArea), self.units+"2")

class ThreadPair:

    def __init__(self, Thread1: ThreadProfile, Thread2: ThreadProfile, EngagementLength: float, Units=None):
        if (Thread1.isExternal != Thread2.isExternal and Thread1.isExternal):
            self.externalThread = Thread1
            self.internalThread = Thread2
        elif (Thread1.isExternal != Thread2.isExternal and Thread2.isExternal):
            self.externalThread = Thread1
            self.internalThread = Thread2
        else:
            print("Internal + External thread pair not found")
            return

        self.internalShearArea = None
        self.externalShearArea = None
        self.engagementLength = EngagementLength
        if Units == None and self.internalThread.units == self.externalThread.units and self.externalThread != None:
            self.units = self.internalThread.units
        else:
            self.units = Units

        self.tensileStressArea = self.externalThread.tensileStressArea

        self.calculateShearArea()

    def calculateShearArea(self):
        if self.externalThread.units != self.internalThread.units:
            print("Warning: units are not the same")
        if self.externalThread.tpi != self.internalThread.tpi:
            print("Warning: tpi are not the same")
        tpi = (self.externalThread.tpi + self.internalThread.tpi)/2
        print("TPI", tpi)

        # Fed-STD-H28
        self.externalShearArea = math.pi * tpi * self.engagementLength * self.internalThread.maxMinorDiameter*\
                            (1/(2*tpi) + 0.57735*(self.externalThread.minPitchDiameter - self.internalThread.maxMinorDiameter))

        self.internalShearArea = math.pi * tpi * self.engagementLength * self.externalThread.minMajorDiameter* \
                                 (1/(2*tpi) + 0.57735*(self.externalThread.minMajorDiameter - self.internalThread.maxPitchDiameter))

    def printInfo(self):
        print("Internal Thread:", self.internalThread.threadCallout)
        print("    Shear Area:", self.internalShearArea, self.units+"2")
        print("External Thread:", self.externalThread.threadCallout)
        print("    Shear Area:", self.externalShearArea, self.units+"2")
        print("    Tensile Area:", self.tensileStressArea, self.units+"2")
        print("Engagement Length:", self.engagementLength, self.units)


if __name__ == "__main__":
    BoltThread1 = input("Bolt Thread1: ")
    BoltThread2 = input("Bolt Thread2: ")

    InputThread1 = ThreadProfile(BoltThread1, rightHand=True)
    InputThread2 = ThreadProfile(BoltThread2, rightHand=True)
    ThreadPair1 = ThreadPair(InputThread1,InputThread2, InputThread1.nominalPitchDiameter*2)

    ThreadPair1.printInfo()
    print("\n---External Thread---")
    ThreadPair1.externalThread.printInfo()
    print("\n---Internal Thread---")
    ThreadPair1.internalThread.printInfo()
