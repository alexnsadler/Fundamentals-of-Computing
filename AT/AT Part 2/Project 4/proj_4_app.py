"""Provide code, solution, and student written code for Application 4."""

import math
import random
import urllib2
import matplotlib.pyplot as plt
import proj_4_des as student


# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


###############################################
# provided code


def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)

    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


###############################################
# student written code

# Sequences constants
PAM_SCORE_MATRIX = read_scoring_matrix(PAM50_URL)
HUMAN_PROTEIN_SEQ = read_protein(HUMAN_EYELESS_URL)
FLY_PROTEIN_SEQ = read_protein(FRUITFLY_EYELESS_URL)
PAX_SEQ = read_protein(CONSENSUS_PAX_URL)
WORD_LIST = read_words(WORD_LIST_URL)


def question_one():
    """
    Compute the local alignment between human and fly sequences for q1.

    Output: a tuple with the local alignment score, the human local alignment,
    and then fly's local alignment
    """
    pam_alm_matrix = student.compute_alignment_matrix(HUMAN_PROTEIN_SEQ,
                                                      FLY_PROTEIN_SEQ,
                                                      PAM_SCORE_MATRIX, False)

    q1_answer = student.compute_local_alignment(HUMAN_PROTEIN_SEQ,
                                                FLY_PROTEIN_SEQ,
                                                PAM_SCORE_MATRIX,
                                                pam_alm_matrix)

    return q1_answer


def question_two():
    """
    Compute the percentage of elements in sequences that agree.

    Output: tuple of the form (hum_perc, fly_perc) where hum_perc is the
    percentage of elements in the local human sequence that agree with the
    elements in the pax sequence. fly_perc is the percentage of elements in the
    local fly sequence that agree with the elements in the pax sequence
    """
    orig_hum_seq, orig_fly_seq = question_one()[1], question_one()[2]
    dashless_hum, dashless_fly = "", ""

    for char in orig_hum_seq:
        if char != '-':
            dashless_hum += char

    for char in orig_fly_seq:
        if char != '-':
            dashless_fly += char

    # Alignment matrices for the human/ PAX seq and the fly/ PAX seq
    pax_hum_alm_matrix = student.compute_alignment_matrix(dashless_hum,
                                                          PAX_SEQ,
                                                          PAM_SCORE_MATRIX,
                                                          True)

    pax_fly_alm_matrix = student.compute_alignment_matrix(dashless_fly,
                                                          PAX_SEQ,
                                                          PAM_SCORE_MATRIX,
                                                          True)

    # Global alignments for local human/ pax and local fly/ pax
    hum_pax_seq = student.compute_global_alignment(dashless_hum, PAX_SEQ,
                                                   PAM_SCORE_MATRIX,
                                                   pax_hum_alm_matrix)

    fly_pax_seq = student.compute_global_alignment(dashless_fly, PAX_SEQ,
                                                   PAM_SCORE_MATRIX,
                                                   pax_fly_alm_matrix)

    # Percentage calculations of elements in alignments that agree
    fly_score = 0.0
    for idx in range(len(fly_pax_seq[1])):
        if fly_pax_seq[1][idx] == fly_pax_seq[2][idx]:
            fly_score += 1
    fly_perc = fly_score / len(fly_pax_seq[1])

    hum_score = 0.0
    for idx in range(len(hum_pax_seq[1])):
        if hum_pax_seq[1][idx] == hum_pax_seq[2][idx]:
            hum_score += 1
    hum_perc = hum_score / len(hum_pax_seq[1])

    return (hum_perc, fly_perc)


# Function for question four
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Generate a null distribution represented by a dictionary of a scoring dist.

    Input: seq_x and seq_y are strings of sequences whose elements share a
    common alphabet with scoring_matrix. scoring_matrix is a dictionary of
    dictionaries where each key is a letter in the given alphabet and the
    values are the scores for each alignment. num_trials is the number of
    desired scores to have in the distriubtion

    Output: a dictionary that represents an un-normalized distribution
    generated by performing num_trials trials
    """
    score_list = []
    for idx in range(num_trials):
        rand_y = ''.join(random.sample(seq_y, len(seq_y)))
        xy_alm = student.compute_alignment_matrix(seq_x, rand_y,
                                                  scoring_matrix, False)
        score = student.compute_local_alignment(seq_x, rand_y,
                                                scoring_matrix, xy_alm)[0]
        score_list.append(score)

    scoring_dist = []
    for idx in range(max(score_list) + 1):
        scoring_dist.append((idx, score_list.count(idx)))

    return dict(scoring_dist)


def question_four():
    """
    Generate a normalized distriubtion graph.

    Output: a normalized graph with data from generate_null_distribution
    for 1000 trials.
    """
    null_dist = generate_null_distribution(HUMAN_PROTEIN_SEQ, FLY_PROTEIN_SEQ, AM_SCORE_MATRIX, num_trials)

    x_vals = null_dist.keys()
    for idx in null_dist:
        null_dist[idx] /= 1000.0
    y_vals = null_dist.values()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    plt.title('Normalized Distribution for Hypothesis Testing with 1000 Trials')
    plt.xlabel('Scores')
    plt.ylabel('Percentage of trials')

    ax1.bar(x_vals, y_vals)
    plt.show()


def question_five():
    """Return statistical computations.

    Output: the mean and standard deviation of the null distriubtion from
    generate_null_distribution and the z-score for the human and fly alignment
    score
    """
    null_dist = generate_null_distribution(HUMAN_PROTEIN_SEQ, FLY_PROTEIN_SEQ, AM_SCORE_MATRIX, num_trials)

    mean = 0
    for idx in null_dist:
        mean += null_dist[idx] * idx
    mean /= 1000

    variance = 0
    for key in null_dist:
        for idx in range(null_dist[key]):
            variance += ((key - mean) ** 2)
    stdev = math.sqrt((1 / 1000.0) * variance)

    # z-score for the human and fly protein local alignment
    hum_fly_score = question_one()[0]
    z_score = (hum_fly_score - mean) / stdev
    return (mean, stdev, z_score)


def question_seven():
    """
    Return the diag_score, off_diag_score, and dash_score.

    Output: a tuple with diag_score, off_diag_score, and dash_score such that
    the score from the resulting global alignment yields the edit distance when
    substituted into the edit distance formula
    """
    diag_score = 2
    off_diag_score = 1
    dash_score = 0

    return (diag_score, off_diag_score, dash_score)


# Function for question 8
def check_spelling(checked_word, dist, word_list):
    """
    Return a list of words within a specified dist of a word.

    Input: checked_word is the word to be checked against the other words in
    the dictionary. dist is the the edit distance for how similar the
    checked_word is compared to the words in word_list. word_list is the list
    of words for checked_word to be checked against

    Output: a list of words that are within the edit distance of dist to words
    in word_list
    """
    scm = student.build_scoring_matrix('abcdefghijklmnopqrstuvwxyz', 2, 1, 0)

    words = []
    for word in word_list:
        alm = student.compute_alignment_matrix(checked_word, word, scm, True)
        glbl_alm = student.compute_global_alignment(checked_word, word,
                                                    scm, alm)
        if len(checked_word) + len(word) - glbl_alm[0] <= dist:
            words.append(glbl_alm[2])

    return words


def question_eight():
    """Return a list of words similar to "humble" and "firely"."""
    humble_words = check_spelling("humble", 1, WORD_LIST)
    firefly_words = check_spelling("firefly", 2, WORD_LIST)

    return humble_words, firefly_words
