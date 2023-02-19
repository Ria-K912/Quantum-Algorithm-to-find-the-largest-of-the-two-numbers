#!/usr/bin/env python
# coding: utf-8

# In[22]:


import math
from qiskit import QuantumCircuit, Aer, execute

def qft_dagger(n):
    """n-qubit QFTdagger the first n qubits in circ."""
    qc = QuantumCircuit(n)
    # Not to forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-math.pi/float(2**(j-m)), m, j)
        qc.h(j)
    return qc

def encode_integer(qc, qr, number):
    """Encode an integer into a quantum register"""
    for i in range(len(number)):
        if number[i] == '1':
            qc.x(qr[len(number)-i-1])
    return qc

def find_the_largest_number(number_1, number_2):
    # Determining the number of qubits required to represent the numbers
    n = max(len(bin(abs(number_1))), len(bin(abs(number_2)))) - 2
    qr = QuantumRegister(3*n)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)

    # encoding the integers as quantum states
    qc = encode_integer(qc, qr[:n], format(number_1, 'b').zfill(n))
    qc = encode_integer(qc, qr[n:2*n], format(number_2, 'b').zfill(n))

    # applying phase oracle to compare the integers
    for i in range(n):
        qc.cswap(qr[i], qr[n+i], qr[2*n+i])
        qc.x(qr[i])
        qc.x(qr[n+i])
        qc.cswap(qr[i], qr[n+i], qr[2*n+i])
        qc.x(qr[i])
        qc.x(qr[n+i])
        qc.h(qr[i])
        qc.h(qr[n+i])

    # applying inverse QFT to measure the largest number
    qc.append(qft_dagger(n), qr[:n])
    qc.measure(qr[:n], cr)

    # running the circuit and getting the measurement results
    backend = Aer.get_backend('qasm_simulator')
    shots = 1024
    results = execute(qc, backend=backend, shots=shots).result()
    counts = results.get_counts()
    max_number = int(max(counts.keys(), key=lambda x: counts[x]), 2)

    return max_number


result = find_the_largest_number(5, -6)
print(result)


# In[ ]:


If we have an infinite number of qubits, then we can represent any integer as an infinite binary string. For example, the integer 5 can be represented as the binary string 101. If we have an infinite number of qubits, we can encode this binary string into the state of the qubits as follows:
|101⟩ = |1⟩ ⊗ |0⟩ ⊗ |1⟩ ⊗ |0⟩ ⊗ |1⟩ ⊗ |0⟩ ⊗......... .Each qubit represents a binary digit in the string, and we use the value of the qubit to encode whether that digit is a 0 or a 1. We can do the same for any integer, no matter how large it is, as long as we have an infinite number of qubits available.

With this representation, we can compare any two integers using the phase oracle and QFT methods we discussed earlier, and we can find the larger number with a probability of 1.


# In[ ]:




