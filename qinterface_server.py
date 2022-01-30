from qinterface import BB84, E91, aer_backend #,QI_backend
import os
import time
import string

quantum_request = dict(
    A_username="", B_username="", method="", A_bitstr="", A_basis="", B_basis="",
)


def execute_quantum_request(backend, quantum_request):
    """
    Takes a quantum request and execute the content,
    returns the messages for Alice and Bob.
    """

    method = quantum_request["method"]
    A_basis = quantum_request["A_basis"]
    B_basis = quantum_request["B_basis"]

    if method == "BB84":
        A_bitstr = quantum_request["A_bitstr"]
        measB = BB84(backend, A_bitstr, A_basis, B_basis)
        measA = []
        return measA, measB

    if method == "E91":
        measA, measB = E91(backend, A_basis, B_basis)
        return measA, measB

    raise


run_flag = True

while run_flag:
    file_names = os.listdir("_in")
    files = []

    # READ INPUT FILES
    for file_name in file_names:
        with open(f"./_in/{file_name}") as f:
            txtlines = f.readlines()
            for line in txtlines:
                if "METHOD" in line:
                    line = line.split(" ")
                    quantum_request["method"] = line[1].replace("\n", "")

                if "ALICE bitstring" in line:
                    line = line.split(" ")
                    quantum_request["A_bitstr"] = line[2].replace("\n", "")

                if "ALICE basis" in line:
                    line = line.split(" ")
                    quantum_request["A_basis"] = line[2].replace("\n", "")
                    quantum_request["A_username"] = file_name.replace(".txt", "")

                if "BOB basis" in line:
                    line = line.split(" ")
                    quantum_request["B_basis"] = line[2].replace("\n", "")
                    quantum_request["B_username"] = file_name.replace(".txt", "")

    print(quantum_request)

    if quantum_request["A_username"] != "" and quantum_request["A_username"] != "" :

        measA, measB = execute_quantum_request(aer_backend, quantum_request)

    with open(f'./_out/{quantum_request["A_username"]}_out.txt', "w") as f:
        f.write(str(measA))
    with open(f'./_out/{quantum_request["B_username"]}_out.txt', "w") as f:
        f.write(str(measB))

        os.remove(f"./_in/{quantum_request['A_username']}.txt")
        os.remove(f"./_in/{quantum_request['B_username']}.txt")

        quantum_request = dict(
         A_username="", B_username="", method="", A_bitstr="", A_basis="", B_basis="",
        )
        break
    time.sleep(5)