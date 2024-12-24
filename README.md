# RSA and Shor's Algorithm Demonstration

This repository provides a simple implementation of RSA encryption/decryption along with Shor's Algorithm for quantum factorization. It includes Python scripts to explore RSA cryptography and how quantum computing can be used to break it.

---

## How RSA and Shor's Algorithm Work

### RSA:
1. **Key Generation:**
   - Two large prime numbers, `p` and `q`, are chosen.
   - The product `n = p * q` forms the modulus.
   - Euler's totient function, `\( \phi(n) = (p-1)(q-1) \)` is calculated.
   - A public exponent `e` is chosen such that `1 < e < \phi(n)` and `\gcd(e, \phi(n)) = 1`.
   - The private key exponent `d` is computed as the modular inverse of `e` mod `\phi(n)`.

2. **Encryption:**
   - A plaintext message is converted to numeric form and encrypted as:
     \[ c = m^e \mod n \]

3. **Decryption:**
   - The ciphertext is decrypted using the private key:
     \[ m = c^d \mod n \]

### Shor's Algorithm:
- Shor's algorithm efficiently factorizes the modulus `n` (used in RSA) into its prime factors `p` and `q` using a quantum computer.
- Once the factors are found, the private key can be reconstructed, breaking the encryption.

---

## How to Run the Project

### Using Docker:
1. **Build the Docker Image:**
   ```bash
   docker build -t rsa-shor-demo .
   ```

2. **Run the Docker Container:**
   ```bash
   docker run -p 8888:8888 rsa-shor-demo
   ```

3. **Access Jupyter Notebook:**
   - Open your browser and navigate to `http://localhost:8888`.
   - Use the token provided in the terminal to log in.
   - Open `Shor_demo.ipynb` to explore RSA and Shor's algorithm interactively.

### Running Locally:
1. **Install Dependencies:**
   Ensure Python 3.9 or later is installed. Then, run:
   ```bash
   pip install numpy sympy qiskit qiskit-aer pycryptodome notebook
   ```

2. **Run Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

3. **Access Jupyter Notebook:**
   - Open your browser and navigate to `http://localhost:8888`.
   - Open `Shor_demo.ipynb` to interact with the scripts.

4. **Run Scripts Directly:**
   - To run the RSA script:
     ```bash
     python simple_rsa.py
     ```
   - To use Shor's Algorithm for factorization:
     ```bash
     python shor.py
     ```

---

## Repository Contents

- `simple_rsa.py`: A Python implementation of RSA encryption and decryption.
- `shor.py`: A Python script implementing Shor's algorithm using Qiskit.
- `Shor_demo.ipynb`: A Jupyter Notebook to demonstrate RSA and Shor's algorithm interactively.
- `Dockerfile`: Configuration for building a Docker image to run the project.

---

## Prerequisites

- **Python Version:** 3.9 or later
- **Quantum Computing Framework:** Qiskit
- **Docker (Optional):** Required for running the project in a containerized environment

---

## License
This project is licensed under the MIT License. Feel free to use, modify, and share it.

---

## Acknowledgements
- RSA Algorithm: Rivest, Shamir, and Adleman (1977)
- Shor's Algorithm: Peter Shor (1994)
- Qiskit: Open-source quantum computing software from IBM


