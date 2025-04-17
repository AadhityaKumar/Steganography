import os
import sys
import binascii
import streamlit as st

p = st.file_uploader("Choose a carrier file")
m = st.file_uploader("Choose a secret message file")
s = st.text_input("number of bits to be skipped", "")
l = st.text_input("length of bits to be skipped between alteration", "")
c = st.text_input("Alteration mode? (1 if yes)", "")

# Example run: py steganography.py carrier.jpg message.jpg 1000 2 1

# Embeding message into carrier


if p and m:

    bytes = bytearray(p.read())
    bini = bytearray(m.read())
    ext = m.name.split(".")[-1]


    alt = [l, l*2, max(1, int(l/2))]
    u = 0

    if( len(bytes) - s < len(bini) * l):
        print("Secret message too long")
    else:


        x = s
        for i in bini:
            for bit in format(i, '08b'):
                bytes[x] = (bytes[x] & 0b11111110) | int(bit)

                if c == 1:
                    x += alt[u]
                    u += 1
                    if u > 2:
                        u = 0
                else:
                    x += l

        steg_fn = f"steg_{p.name}"
        st.download_button("Steganographized file: ", data = bytes, file_name = steg_fn)


    # Extracting the message from carrier

    new_file = []
    z = s

    u = 0
    for i in range(len(bini) * 8):
        
        new_file.append(str(bytes[z] & 1))

        if c == 1:
            z += alt[u]
            u += 1
            if u > 2:
                u = 0
        else:
            z += l

    nf = bytearray(int(''.join(new_file[i:i+8]), 2) for i in range(0, len(new_file), 8))

    rf = "extracted." + ext[1]
    st.download_button("Extracted file: ", data = nf, file_name = rf)



# Someone could find M or P given only L by starting at various points of the
# steganographized text and observing every Lth bit. They would have to try it
# over and over at various points because they have to guess where the offset is.