import streamlit as st
from io import BytesIO

st.title("Steganography Encoder/Decoder")

# Upload files
carrier_file = st.file_uploader("Choose a carrier file (e.g., image/video)", type=["jpg", "png", "bmp", "mp4", "mov"])
secret_file = st.file_uploader("Choose a secret message file (any format)")

# User inputs
s = st.number_input("Bits to skip at start (s)", min_value=0, value=1000)
l = st.number_input("Bit spacing between changes (l)", min_value=1, value=2)
c = st.checkbox("Enable alternate spacing mode (c)")

if carrier_file and secret_file:
    carrier_bytes = bytearray(carrier_file.read())
    message_bytes = bytearray(secret_file.read())
    message_ext = secret_file.name.split(".")[-1]

    alt = [l, l * 2, max(1, l // 2)]
    u = 0

    if len(carrier_bytes) - s < len(message_bytes) * 8 * l:
        st.error("Secret message too large for selected carrier and settings.")
    else:
        x = s
        for byte in message_bytes:
            for bit in format(byte, '08b'):
                carrier_bytes[x] = (carrier_bytes[x] & 0b11111110) | int(bit)
                if c:
                    x += alt[u]
                    u = (u + 1) % 3
                else:
                    x += l

        stego_filename = f"stego_{carrier_file.name}"
        st.success("Message embedded successfully!")
        st.download_button("Download Stego File", data=carrier_bytes, file_name=stego_filename)

        # Extract the message
        z = s
        u = 0
        extracted_bits = []
        for _ in range(len(message_bytes) * 8):
            extracted_bits.append(str(carrier_bytes[z] & 1))
            if c:
                z += alt[u]
                u = (u + 1) % 3
            else:
                z += l

        extracted_bytes = bytearray(
            int("".join(extracted_bits[i:i + 8]), 2) for i in range(0, len(extracted_bits), 8)
        )

        extracted_filename = f"extracted.{message_ext}"
        st.download_button("Download Extracted Message", data=extracted_bytes, file_name=extracted_filename)
