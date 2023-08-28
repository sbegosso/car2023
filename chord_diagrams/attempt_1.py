import pandas as pd
from pycirclize import Circos
import sys

num = int(sys.argv[1])

#means 3 sections will be feeding into 8 sections
french_names = ["Dillygence", "HIVE Electric", "Numalliance", "OSE Group", 
             "SIC Marketing", "SpooN", "SYSGO", "TRA-C Industrie"]
us_names = ["Borgwarner", "Magna", "Forvia", "Eaton", 
            "Steris", "Invacare", "LubriZol", "GoodYear"]

#3 x 8 matrix
matrix_data = [
    [1, 1, 1, 0, 1, 1, 1, 1], 
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
]

matrix_df = pd.DataFrame(matrix_data, index=us_names, columns=french_names)

#Initialize Circos from matrix for plotting Chord Diagram
circos = Circos.initialize_from_matrix(
    matrix_df,
    space = 8,
    cmap = "tab10",
    label_kws=dict(size=12),
    link_kws=dict(ec="black", lw=0.5, direction=-1),
)

circos.savefig("example0{}.png".format(num))