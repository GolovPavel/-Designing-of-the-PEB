import utils

def write_header(file, header):
  file.write("======================\n")
  file.write(header + "\n")
  file.write("----------------------\n")
  
def first_circuit_params_calculation(data):
  file = open("heat_paramsOutput.txt", "w")
  write_header(file, "1st circuit parameters")
  
  Gr = data["Wsr"] * data["roH2O"] * data["Stn"] / data["kG"] * data["Ntvs"]
  Gtn = Gr * data["kG"] / data["Ntvs"]
  deltaTr = data["Qr"] / (data["Cp"] * Gr)
  tVhR = data["tVihR"] - deltaTr
  
  file.write("Gr: %.3f\nGtn: %.3f\ndeltaTr: %.3f\ntVhR: %.3f\n" % (Gr, Gtn, deltaTr, tVhR))
  file.close()
  
data = {}
utils.fill_dict_from_file(data, "heat_paramsInput.txt")
first_circuit_params_calculation(data)
