"""
This class will handle the parsing of arguments 
which will take the form of the test ID in the NGTD.
"""
# import the requests module
import argparse

# Create the class
class ParseArguments:
    """
    A class to take in the arguments from the command line
    Save command line arguments into variables
    Handle Exceptions and give users detailed Warnings
    ...
    Attributes
    ----------
    testID : str
        the testID from user

    Methods
    -------
    info()
        prints the testID
    validity()
        tests if the testID starts with an R
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the parse_arguments object
        
        Parameters
        ----------

        testID : str
            the testID from inputed from the user
        """
        self.testID = "Nothing"

    def info(self):
        print(testID) #This is using testID before assignment will give an error

    def validity(self):
        if testID[:1] != "R":
            print("invalid R code")

if __name__ == "__main__":

    mrq = ParseArguments()
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-ID", "--testID", help="input the Test ID")
    args = argParser.parse_args()
    testID = args.testID
    mrq.validity()
    mrq.info()