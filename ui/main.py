# %%
import os
from argparse import ArgumentParser

import pandas as pd
import streamlit as st
from app import app
from managers.session_manager import SessionManager
from constants import SESSION_KEYS
from views.sidebar_cohort_nav import render_sidebar_cohort_subjects


def parse_args(args=None):
    parser = ArgumentParser("QC-Studio")

    parser.add_argument(
        "--dataset_dir",
        dest="dataset_dir",
        help=("Path to dataset dir"),
        required=True,
    )
    parser.add_argument(
        "--participant_list",
        dest="participant_list",
        help=("List of participants to QC"),
        required=True,
    )
    parser.add_argument(
        "--session_list",
        dest="session_list",
        help=("List of sessions to QC"),
        default="Baseline",
        required=False,
    )
    parser.add_argument(
        "--qc_pipeline",
        help=("Pipeline output to QC"),
        dest="qc_pipeline",
        required=True,
    )
    parser.add_argument(
        "--qc_task",
        help=("Specific workflow output to QC"),
        dest="qc_task",
        required=True,
    )
    parser.add_argument(
        "--output_dir",
        dest="out_dir",
        help="Directory to save session state and QC results",
        required=True,
    )
    parser.add_argument(
        "--qc_json",
        dest="qc_json",
        help=("Path to a JSON containing a list of image file paths to be displayed."),
        required=True,
    )

    return parser.parse_args(args)


def get_cli_run_context():
    """Paths and counts from CLI args.

    Used by ``main()`` and by multipage ``pages/*.py`` entrypoints so sidebar
    navigation matches the same run configuration.
    """
    args = parse_args()
    ui_dir = os.path.dirname(os.path.abspath(__file__))
    qc_config_path = os.path.join(ui_dir, args.qc_json)
    participants_df = pd.read_csv(args.participant_list, delimiter="\t")
    stored_ids = SessionManager.get_participant_ids()
    participant_ids = stored_ids if stored_ids else participants_df["participant_id"].tolist()
    total_participants = len(participant_ids)
    return {
        "dataset_dir": args.dataset_dir,
        "participant_list": args.participant_list,
        "qc_pipeline": args.qc_pipeline,
        "qc_task": args.qc_task,
        "qc_config_path": qc_config_path,
        "out_dir": args.out_dir,
        "total_participants": total_participants,
        "drop_duplicates": True,
        "participant_ids": participant_ids,
    }


def main():
    """Main entry point for the Streamlit app."""
    ctx = get_cli_run_context()
    dataset_dir = ctx["dataset_dir"]
    participant_list = ctx["participant_list"]
    qc_pipeline = ctx["qc_pipeline"]
    qc_task = ctx["qc_task"]
    qc_config_path = ctx["qc_config_path"]
    out_dir = ctx["out_dir"]
    total_participants = ctx["total_participants"]
    drop_duplicates = ctx["drop_duplicates"]

    participants_df = pd.read_csv(participant_list, delimiter="\t")
    stored_ids = SessionManager.get_participant_ids()
    participant_ids = stored_ids if stored_ids else participants_df["participant_id"].tolist()

    # Initialize session state
    SessionManager.init_session_state()
    SessionManager.compact_duplicate_qc_records_if_needed()

    session_id = "ses-01"
    render_sidebar_cohort_subjects(
        participant_ids=participant_ids,
        total_participants=total_participants,
        qc_task=qc_task,
        session_id=session_id,
        entrypoint_rel_path=None,
    )

    current_page = st.session_state.get(SESSION_KEYS['current_page'], 1)
    if current_page < 1:
        st.session_state[SESSION_KEYS['current_page']] = 1
        current_page = 1

    if current_page > total_participants:
        participant_id = None
    else:
        participant_id = participant_ids[current_page - 1]
        # Ensure participant_id has "sub-" prefix
        if participant_id and not participant_id.startswith("sub-"):
            participant_id = f"sub-{participant_id}"

    app(
        dataset_dir=dataset_dir,       
        participant_id=participant_id,
        session_id=session_id,
        qc_pipeline=qc_pipeline,
        qc_task=qc_task,
        qc_config_path=qc_config_path,
        out_dir=out_dir,
        total_participants=total_participants,
        drop_duplicates=drop_duplicates,
        participant_list=participant_list,
        participant_ids=participant_ids,
    )


if __name__ == "__main__":
    main()




# %%
