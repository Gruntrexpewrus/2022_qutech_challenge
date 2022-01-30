import numpy as np
import os
from qiskit import execute, QuantumCircuit
from qiskit import QuantumCircuit, Aer
from quantuminspire.qiskit import QI


def init_QI():
    """
    Quantum inspire setup.
    """

    QI.set_authentication()
    QI.set_project_name("spiNYpizza")
    backend = QI.get_backend("Starmon-5")

    return backend


QI_backend = init_QI()
aer_backend = Aer.get_backend("aer_simulator")


def BB84(backend, input_data_string, alice_basis, bob_basis):
    """
    Taken the command string from Alice and Bob, 
    build the circuit for BB84 and run it on QuantumInspire.

    """

    assert len(input_data_string) == len(alice_basis)
    assert len(input_data_string) == len(bob_basis)

    def encode_part(qc, bit, base):
        bit = int(bit)
        base = int(base)
        if base == 0:  # Prepare qubit in Z-basis
            if bit == 0:
                pass
            else:
                qc.x(0)
        else:  # Prepare qubit in X-basis
            if bit == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()

        return qc

    def decode_part(qc, base):
        base = int(base)
        if base == 0:  # measuring in Z-basis
            qc.measure(0, 0)
        if base == 1:  # measuring in X-basis
            qc.h(0)
            qc.measure(0, 0)
        return qc

    results = ''

    for i in range(len(input_data_string)):
        qc = QuantumCircuit(1, 1)
        qc = encode_part(qc, input_data_string[i], alice_basis[i])
        qc = decode_part(qc, bob_basis[i])
        print(input_data_string[i], alice_basis[i], bob_basis[i])
        print(qc)
        _res = execute(qc, backend=backend, shots=1, memory=True).result()
        results += (str(_res.get_memory()[0]))

    return results


def E91(backend, alice_basis, bob_basis):
    """
    Taken the command string from Alice and Bob, 
    build the circuit for E91 and run it on QuantumInspire.
    """
    assert len(bob_basis) == len(alice_basis)
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(0)

    def add_basis(qc, base, index):
        base = int(base)
        if base == 1:  # measuring in X-basis
            qc.h(index)
        return qc

    measA, measB = '', ''

    for i in range(len(alice_basis)):
        q = qc.copy()
        q = add_basis(q, alice_basis[i], 0)
        q = add_basis(q, bob_basis[i], 1)
        q.measure_all()
        _res = execute(q, backend=backend, shots=1, memory=True).result()
        measA += (str(_res.get_memory()[0][0]))
        measB += (str(_res.get_memory()[0][1]))
    return measA, measB
