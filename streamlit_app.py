import streamlit as st
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
import tempfile

st.set_page_config(page_title="Protein Sequence Alignment Tool", layout="wide")
st.title("🔬 Protein Sequence Alignment Tool (BLAST)")

sequence_input = st.text_area("Paste your protein sequence (FASTA format preferred):", height=200)

database = st.selectbox("Choose BLAST database:", ["nr", "swissprot"])
program = "blastp"

if st.button("Run BLAST"):
    if not sequence_input.strip():
        st.warning("Please enter a protein sequence.")
    else:
        with st.spinner("Running BLAST... this may take a while."):
            try:
                result_handle = NCBIWWW.qblast(program=program, database=database, sequence=sequence_input)
                blast_records = NCBIXML.read(result_handle)

                st.success("BLAST search complete. Top alignments:")

                for alignment in blast_records.alignments[:5]:
                    for hsp in alignment.hsps:
                        st.markdown(f"**Alignment Title:** {alignment.title}")
                        st.markdown(f"**Length:** {alignment.length}")
                        st.markdown(f"**Score:** {hsp.score}")
                        st.markdown(f"**E-value:** {hsp.expect}")
                        st.code(hsp.sbjct)
                        st.markdown("---")
            except Exception as e:
                st.error(f"An error occurred: {e}")
