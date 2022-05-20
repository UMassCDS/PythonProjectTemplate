"""An example of a script you can run. It tokenizes an folder of input documents and
writes the corpus counts to a user-specified CSV file
"""
import argparse
import logging
from pathlib import Path

# Import the code from this project needed for this script
from cdstemplate import sample_module, utils

logger = logging.getLogger(__name__)


def main(csv_out, documents, case_insensitive=False):
    cc = sample_module.CorpusCounter(case_insensitive=case_insensitive)
    for i, doc in enumerate(documents):
        if i % 2 == 0:
            logger.info("Tokenizing document number %s: %s", i, doc)
            cc.add_doc(Path(doc).read_text())

    cc.save_token_counts(csv_out)


# The argument parser gives nice ways to include help message and specify which arguments
# are required or optional, see https://docs.python.org/3/library/argparse.html#prog for usage instructions
parser = argparse.ArgumentParser(
    description="A script to generate counts of tokens in a corpus"
)

parser.add_argument(
    "csv", help="Path to the output CSV storing token counts. Required."
)

parser.add_argument(
    "documents",
    nargs="+",
    help="Paths to at least one raw text document that make up the corpus. Required.",
)
parser.add_argument(
    "--case-insensitive",
    "-c",
    action="store_true",
    help="Default is to have case sensitive tokenization. Use this flag to make the token counting case insensitive. Optional.",
)


# The entry point of your script - if a user runs it from the commane line, this is what will be run.
if __name__ == "__main__":
    args = parser.parse_args()
    utils.configure_logging()
    logger.info("Command line arguments: %s", args)
    main(args.csv, args.documents, args.case_insensitive)

