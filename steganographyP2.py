import os
import sys
import binascii
import streamlit as st

selection = st.radio("Select operation: ", ["Embed a file", "Extract message from file"])

if(selection == "Embed a file"):

    p = st.file_uploader("Choose a carrier file")
    m = st.file_uploader("Choose a secret message file")
    s = st.number_input("number of bits to be skipped", min_value=0, value=1000)
    l = st.number_input("length of bits to be skipped between alteration", min_value=1, value=2)
    c = st.checkbox("Enable alternate spacing mode (c)")

    # Example run: py steganography.py carrier.jpg message.jpg 1000 2 1

    # Embeding message into carrier

    if p and m:

        carrier_bytes = bytearray(p.read())
        bini = bytearray(m.read())
        ext = m.name.split(".")


        alt = [l, l * 2, max(1, l // 2)]    
        u = 0

        if len(carrier_bytes) - s < len(bini) * l:
            st.error("Secret message too long")
        else:


            x = s
            for i in bini:
                for bit in format(i, '08b'):
                    carrier_bytes[x] = (carrier_bytes[x] & 0b11111110) | int(bit)

                    if c == 1:
                        x += alt[u]
                        u += 1
                        if u > 2:
                            u = 0
                    else:
                        x += l

            steg_fn = f"steg_{p.name}"
            st.download_button("Steganographized file: ", data = bytes(carrier_bytes), file_name = steg_fn)
            st.info("length of secret message is " +  str(len(bini)))


# Extracting the message from carrier
elif(selection == "Extract message from file"):

    p = st.file_uploader("Choose a carrier file")
    s = st.number_input("number of bits to be skipped", min_value=0, value=1000)
    l = st.number_input("length of bits to be skipped between alteration", min_value=1, value=2)
    bini = st.number_input("length of secret message")
    c = st.checkbox("Enable alternate spacing mode (c)")
    ext = st.text_input("file extension of secret message (png, jpg, mov, etc)")

    if bini and p:

        carrier_bytes = bytearray(p.read())

        alt = [l, l * 2, max(1, l // 2)]    


        new_file = []
        z = s

        u = 0
        for i in range(bini * 8):
            
            new_file.append(str(carrier_bytes[z] & 1))

            if c == 1:
                z += alt[u]
                u += 1
                if u > 2:
                    u = 0
            else:
                z += l

        nf = bytearray(int(''.join(new_file[i:i+8]), 2) for i in range(0, len(new_file), 8))

        rf = "extracted." + ext
        st.download_button("Extracted file: ", data = bytes(nf), file_name = rf)



# Someone could find M or P given only L by starting at various points of the
# steganographized text and observing every Lth bit. They would have to try it
# over and over at various points because they have to guess where the offset is.