import fractions
import math
import random
import numpy as np
import sympy
from typing import Callable, Iterable, List, Optional, Sequence, Union
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram

def shor_factorization(n):
    # Set Base
    for _ in range(100):
        # Choose a random number between 2 and n - 1.
        x = random.randint(2, n - 1)
        
        # Most likely x and n will be relatively prime.
        c = math.gcd(x, n)
        
        # If x and n are not relatively prime, return factor
        if 1 < c < n:
            return c
        # Using Shor
        r = shor_order(x, n)
        
        # If the order finder failed, try again.
        if r is None:
            continue
        
        # If the order r is even, try again.
        if r % 2 != 0:
            continue
        
        # Compute the non-trivial factor.
        y = x**(r // 2) % n
        assert 1 < y < n
        c = math.gcd(y - 1, n)
        if 1 < c < n:
            return c

def shor_order(x, n):
    # Set Bit length of the integer N
    L = n.bit_length()
    base = x
    
    qreg_t = QuantumRegister(L)
    qreg_e = QuantumRegister(2*L + 3)

    mod_circuit = QuantumCircuit(qreg_t, qreg_e, name='ModExp')

    # Modular exponentiation logic
    for i, control_qubit in enumerate(qreg_e):
        # Compute base^(2^i) % n
        exp_base = pow(base, 2**i, n)
        # Apply controlled modular multiplication
        for j in range(len(qreg_t)):
            if (exp_base >> j) & 1:  # Check if the j-th bit of exp_base is set
                mod_circuit.cx(control_qubit, qreg_t[j])
    
    creg = ClassicalRegister(2*L + 3)
    qc = QuantumCircuit(qreg_t,qreg_e, creg)
    
    
    qc.x(qreg_t[L-1])
    qc.h(qreg_e)
    qc.barrier()
    qc.append(mod_circuit.to_instruction(), qc.qubits)
    qc.barrier()
    qc.append(QFT(num_qubits=len(qreg_e), do_swaps=True).inverse().decompose(), qreg_e[:])
    qc.barrier()
    qc.measure(qreg_e,creg)
    
    qc = qc.decompose().decompose()
    backend = AerSimulator()
    job = backend.run(qc, shots = 33)
    job.status()
    result = job.result()

    # Extract counts from the result
    counts = result.get_counts()
    
    # Get the bitstring with the highest count (most likely measurement)
    bitstring = max(counts, key=counts.get)
    exponent_as_integer = int(bitstring, 2)

    # Determine the number of bits in the exponent register
    num_exponent_bits = len(bitstring)

    # Compute the eigenphase
    eigenphase = exponent_as_integer / (2**num_exponent_bits)

    # Run the continued fractions algorithm to find f = s / r
    f = fractions.Fraction.from_float(eigenphase).limit_denominator(n)

    # If the numerator is zero, the order finder failed
    if f.numerator == 0:
        return None

    # Get the candidate order r
    r = f.denominator

    # Validate r: x^r mod n must equal 1
    if pow(x, r, n) != 1:
        return None

    return r
