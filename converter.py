import numpy as np
import warnings
warnings.filterwarnings('ignore')

class TwoPortConverter:
    def __init__(self):
        self.parameters = {'Z': None, 'Y': None, 'H': None, 'ABCD': None, 'G': None}
    
    def validate_matrix(self, matrix):
        if matrix.shape != (2, 2):
            raise ValueError("Matrix must be 2x2")
        return True
    
    def set_parameters(self, param_type, matrix):
        matrix = np.array(matrix, dtype=complex)
        self.validate_matrix(matrix)
        
        if param_type == 'Z':
            self.parameters['Z'] = matrix
            self.z_to_all()
        elif param_type == 'Y':
            self.parameters['Y'] = matrix
            self.y_to_all()
        elif param_type == 'H':
            self.parameters['H'] = matrix
            self.h_to_all()
        elif param_type == 'ABCD':
            self.parameters['ABCD'] = matrix
            self.abcd_to_all()
        elif param_type == 'G':
            self.parameters['G'] = matrix
            self.g_to_all()
    
    def z_to_all(self):
        Z = self.parameters['Z']
        Z11, Z12, Z21, Z22 = Z[0,0], Z[0,1], Z[1,0], Z[1,1]
        delta_Z = Z11 * Z22 - Z12 * Z21
        
        # Z to Y
        if abs(delta_Z) > 1e-12:
            self.parameters['Y'] = np.array([[Z22/delta_Z, -Z12/delta_Z],
                                             [-Z21/delta_Z, Z11/delta_Z]])
        
        # Z to H
        if abs(Z22) > 1e-12:
            self.parameters['H'] = np.array([[delta_Z/Z22, Z12/Z22],
                                             [-Z21/Z22, 1/Z22]])
        
        # Z to ABCD
        if abs(Z21) > 1e-12:
            self.parameters['ABCD'] = np.array([[Z11/Z21, delta_Z/Z21],
                                                [1/Z21, Z22/Z21]])
        
        # Z to G
        if abs(Z11) > 1e-12:
            self.parameters['G'] = np.array([[1/Z11, -Z12/Z11],
                                             [Z21/Z11, delta_Z/Z11]])
    
    def y_to_all(self):
        Y = self.parameters['Y']
        Y11, Y12, Y21, Y22 = Y[0,0], Y[0,1], Y[1,0], Y[1,1]
        delta_Y = Y11 * Y22 - Y12 * Y21
        
        # Y to Z
        if abs(delta_Y) > 1e-12:
            self.parameters['Z'] = np.array([[Y22/delta_Y, -Y12/delta_Y],
                                             [-Y21/delta_Y, Y11/delta_Y]])
        
        # Y to H
        if abs(Y22) > 1e-12:
            self.parameters['H'] = np.array([[1/Y22, -Y12/Y22],
                                             [Y21/Y22, delta_Y/Y22]])
        
        # Y to ABCD
        if abs(Y21) > 1e-12:
            self.parameters['ABCD'] = np.array([[-Y22/Y21, -1/Y21],
                                                [-delta_Y/Y21, -Y11/Y21]])
        
        # Y to G
        if abs(Y11) > 1e-12:
            self.parameters['G'] = np.array([[delta_Y/Y11, Y12/Y11],
                                             [-Y21/Y11, 1/Y11]])
    
    def h_to_all(self):
        H = self.parameters['H']
        H11, H12, H21, H22 = H[0,0], H[0,1], H[1,0], H[1,1]
        delta_H = H11 * H22 - H12 * H21
        
        # H to Z
        if abs(H22) > 1e-12:
            self.parameters['Z'] = np.array([[delta_H/H22, H12/H22],
                                             [-H21/H22, 1/H22]])
        
        # H to Y
        if abs(H11) > 1e-12:
            self.parameters['Y'] = np.array([[1/H11, -H12/H11],
                                             [H21/H11, delta_H/H11]])
        
        # H to ABCD
        if abs(H21) > 1e-12:
            self.parameters['ABCD'] = np.array([[-delta_H/H21, -H11/H21],
                                                [-H22/H21, -1/H21]])
        
        # H to G
        if abs(H12) > 1e-12:
            self.parameters['G'] = np.array([[H22/H12, -delta_H/H12],
                                             [-1/H12, H11/H12]])
    
    def abcd_to_all(self):
        ABCD = self.parameters['ABCD']
        A, B, C, D = ABCD[0,0], ABCD[0,1], ABCD[1,0], ABCD[1,1]
        delta_T = A * D - B * C
        
        # ABCD to Z
        if abs(C) > 1e-12:
            self.parameters['Z'] = np.array([[A/C, delta_T/C],
                                             [1/C, D/C]])
        
        # ABCD to Y
        if abs(B) > 1e-12:
            self.parameters['Y'] = np.array([[D/B, -delta_T/B],
                                             [-1/B, A/B]])
        
        # ABCD to H
        if abs(B) > 1e-12:
            self.parameters['H'] = np.array([[delta_T/D, B/D],
                                             [-1/D, 1/D]])
        
        # ABCD to G
        if abs(C) > 1e-12:
            self.parameters['G'] = np.array([[1/A, -B/A],
                                             [C/A, delta_T/A]])
    
    def g_to_all(self):
        G = self.parameters['G']
        G11, G12, G21, G22 = G[0,0], G[0,1], G[1,0], G[1,1]
        delta_G = G11 * G22 - G12 * G21
        
        # G to Z
        if abs(G22) > 1e-12:
            self.parameters['Z'] = np.array([[1/G22, -G12/G22],
                                             [G21/G22, delta_G/G22]])
        
        # G to Y
        if abs(G11) > 1e-12:
            self.parameters['Y'] = np.array([[delta_G/G11, G12/G11],
                                             [-G21/G11, 1/G11]])
        
        # G to H
        if abs(G12) > 1e-12:
            self.parameters['H'] = np.array([[G22/G12, -delta_G/G12],
                                             [-1/G12, G11/G12]])
        
        # G to ABCD
        if abs(G21) > 1e-12:
            self.parameters['ABCD'] = np.array([[1/G21, G22/G21],
                                                [G11/G21, delta_G/G21]])
    
    def get_formatted_results(self):
        results = []
        for param_type, matrix in self.parameters.items():
            if matrix is not None:
                results.append(f"\n{param_type}-Parameters:")
                for i in range(2):
                    for j in range(2):
                        num = matrix[i, j]
                        if np.isnan(num) or np.isinf(num):
                            val = "Undefined"
                        else:
                            real = np.real(num)
                            imag = np.imag(num)
                            if abs(imag) < 1e-10:
                                val = f"{real:.6f}"
                            elif abs(real) < 1e-10:
                                val = f"j{imag:.6f}"
                            else:
                                sign = '+' if imag >= 0 else '-'
                                val = f"{real:.6f} {sign} j{abs(imag):.6f}"
                        results.append(f"{param_type}{i+1}{j+1} = {val}")
        return "\n".join(results)