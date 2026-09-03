import streamlit as st


def upload_product_images():
    """
    Allows the user to upload multiple images
    of the same packaged commodity.
    """

    uploaded_images = st.file_uploader(
        "Upload images of the product package",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload front, back, side, top or bottom views of the package."
    )

    return uploaded_images