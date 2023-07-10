import os
import json
import numpy as np
import matplotlib.pyplot as plt

# if you need to access a file next to the source code, use the variable ROOT
# for example:
#    torch.load(os.path.join(ROOT, 'weights.pth'))
ROOT = os.path.dirname(os.path.realpath(__file__))

FOLDER = "GaitData"
CODE_LIST = [filename.replace("_lf.txt", "") for filename in os.listdir(FOLDER) if filename.endswith("_lf.txt")]
#COLUMN_NAMES = {'PacketCounter': 0, 'Acc_X': 1, 'Acc_Y': 2, 'Acc_Z': 3, 'FreeAcc_X': 4, 'FreeAcc_Y': 5, 'FreeAcc_Z': 6,
#                'Gyr_X': 7, 'Gyr_Y': 8, 'Gyr_Z': 9, 'Mag_X': 10, 'Mag_Y': 11, 'Mag_Z': 12}
COLUMN_NAMES = {'TAX': 0, 'TAY': 1, 'TOX': 2, 'RAV': 3, 'RAZ': 4, 'RRY': 5, 'LAV': 6, 'LAZ': 7, 'LRY': 8}


def load_metadata(subject, trial):
    """Return the metadata dict for the given subject-trial.

    Arguments:
        subject {int} -- Subject number
        trial {int} -- Trial number

    Returns
    -------
    dict
        Metadata
    """

    code = str(subject) + "-" + str(trial)
    fname = os.path.join(FOLDER, code)
    with open(fname + ".json") as metadata_file:
        metadata_dict = json.load(metadata_file)
    return metadata_dict


def load_signal(subject, trial):
    """Return the signal associated with the subject-trial pair.

    Parameters
    ----------
    subject : int
        Subject number
    trial : int
        Trial number

    Returns
    -------
    numpy array
        Signal

    """
    code = str(subject) + "-" + str(trial)
    fname = os.path.join(FOLDER, code)
    signal_lb = np.loadtxt(fname+"_lb.txt", skiprows=1)
    signal_lf = np.loadtxt(fname+"_lf.txt", skiprows=1)
    signal_rf = np.loadtxt(fname+"_rf.txt", skiprows=1)
    return signal


def print_trial_info(metadata_dict):
    """Dump the trial information in a text file (trial_info.txt)

    Parameters
    ----------
    metadata_dict : dict
        Metadata of the trial.
    signal : numpy array
        Time series of the trial.

    """
    display_dict = {'Subject': "Subject: {Subject}".format(**metadata_dict),
                    'Trial': "Trial: {Trial}".format(**metadata_dict),
                    'Age': "Age (year): {Age}".format(**metadata_dict),
                    'Gender': "Gender: {Gender}".format(**metadata_dict),
                    'Height': "Height (m): {Height}".format(**metadata_dict),
                    'Weight': "Weight (kg): {Weight}".format(**metadata_dict),
                    'WalkingSpeed': "WalkingSpeed (m/s): {WalkingSpeed}".format(2000/(metadata_dict['TrialBoundaries'][1]-metadata_dict['TrialBoundaries'][0])),
                    'UTurnDuration': "U-Turn Duration (s): {}".format((metadata_dict['UTurnBoundaries'][1]-metadata_dict['UTurnBoundaries'][0])/100),
                    'LeftGaitCycles': '    - Left foot: {}'.format(len(metadata_dict['LeftFootActivity'])),
                    'RightGaitCycles': '    - Right foot: {}'.format(len(metadata_dict['RightFootActivity']))
                    }
    info_msg = """
    {Subject:^30}|{Trial:^30}
    ------------------------------+------------------------------
    {Age:<30}| {WalkingSpeed:<30}
    {Height:<30}| Number of footsteps:
    {Weight:<30}| {LeftGaitCycles:<30}
    {UTurnDuration:<30} | {RightGaitCycles:<30}
    """
    # Dump information
    with open("trial_info.txt", "w") as f:
        print(info_msg.format(**display_dict), file=f)


def dump_plot(signal, metadata_dict, to_plot=["RAV", "RAZ", "RRY"]):

    n_samples, _ = signal.shape
    tt = np.arange(n_samples) / 100

    # get limits
    acc = np.take(signal, indices=[COLUMN_NAMES[dim_name]
                                   for dim_name in to_plot if dim_name[1] == "A"], axis=1)
    if acc.size > 0:
        acc_ylim = [acc.min()-0.1, acc.max()+0.1]
    rot = np.take(signal, indices=[COLUMN_NAMES[dim_name]
                                   for dim_name in to_plot if dim_name[1] == "R"], axis=1)
    if rot.size > 0:
        rot_ylim = [rot.min()-20, rot.max()+20]

    for dim_name in to_plot:
        fig, ax = plt.subplots(figsize=(10, 4))
        # xlim
        ax.set_xlim(0, n_samples/100)
        # plot
        dim = COLUMN_NAMES[dim_name]
        ax.plot(tt, signal[:, dim])
        # ylim
        if dim_name[1] == "A":
            ax.set_ylim(acc_ylim)
        elif dim_name[1] == "R":
            ax.set_ylim(rot_ylim)
        # number of yticks
        plt.locator_params(axis='y', nbins=6)
        # ylabel
        ylabel = "m/s²" if dim_name[1] == "A" else "deg/s"
        ax.set_ylabel(ylabel, fontdict={"size": 20})
        for z in ax.get_yticklabels() + ax.get_xticklabels():
            z.set_fontsize(15)
        # step annotations
        if dim_name[0] == "R":
            steps = metadata_dict["RightFootActivity"]
        elif dim_name[0] == "L":
            steps = metadata_dict["LeftFootActivity"]

        ymin, ymax = ax.get_ylim()
        for start, end in steps:
            ax.vlines([start/100, end/100], ymin, ymax, linestyles="--", lw=1)
            ax.fill_between([start/100, end/100], ymin, ymax,
                            facecolor="green", alpha=0.3)
        fig.tight_layout()
        plt.savefig(dim_name + ".svg", dpi=300,
                    transparent=True, bbox_inches='tight')


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description='Display information and time series for a given trial.')
    parser.add_argument('--subject', metavar='subject', type=int,
                        help='The subject identifier')
    parser.add_argument('--trial', metavar='trial', type=int,
                        help='The trial identifier')
    args = parser.parse_args()

    subject, trial = args.subject, args.trial
    to_plot = ["TAX", "TAY", "TOX", "RAV", "RAZ", "RRY", "LAV", "LAZ", "LRY"]

    # check if the code exists.
    code = str(subject) + "-" + str(trial)
    assert code in CODE_LIST, "The following code does not exist: {}".format(
        code)

    # Check if the signal to display follow the naming convention.
    assert all(
        dim_name in COLUMN_NAMES for dim_name in to_plot), "Check the names of the dimensions to plot."

    # load metadata and signal
    metadata = load_metadata(subject, trial)
    signal = load_signal(subject, trial)
    # dump trial info
    print_trial_info(metadata)
    # dump plots
    dump_plot(signal, metadata, to_plot=to_plot)
