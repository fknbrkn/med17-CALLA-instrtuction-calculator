#from dis import Instruction
from sys import byteorder
#import os


def encode_calla(address):
    # check for the 2 bytes step in adress
    if address % 2 != 0:
        raise ValueError("Address must be aligned to 2 bytes (multiple of 2).")
   
    shifted_address = address >> 1

    # offset limited to 43 bit
    if shifted_address >= (1 << 43):
        raise ValueError("Address exceeds 43-bit limit.")

    opcode = 0xED000000 #CALLA
    shifted_address += 0x800000
    
    instruction = opcode + shifted_address
    hx = instruction.to_bytes(4, byteorder='big')
    return (swapLastBytes(hx))


def swapLastBytes(hx):
    return (hx[0] << 0x18) + (hx[1] << 0x10) + (hx[3] << 8) + (hx[2])
    
    
if __name__ == "__main__":
    while True:
        try:
            # user input
            address = int(input("Enter the address (in hexadecimal without 0x8* base, e.g., 172A00): "), 16)
            hex_code = encode_calla(address)
            hex_code = " ".join(f"{(hex_code >> (8 * i)) & 0xFF:02X}" for i in reversed(range((hex_code.bit_length() + 7) // 8)))

            print(f"Instruction for CALLA to address 0x{address:X}: {hex_code}")
        except ValueError as e:
            print(f"Error: {e}")
        
        # Ожидание нажатия пробела для рестарта
        input()
  
