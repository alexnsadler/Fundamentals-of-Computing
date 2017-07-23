"""Student written code for project 4."""


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """Compute a scoring matrix that is a dictionary of dictionaries.

    Input: alphabet is a set of letters, diag_score is a score for letters with
    the same value, off_diag_score is a score for letters with different
    values, and dash_score is a score for letters matched with dashes

    Output: a dictionary of dictionaries where each key is a letter in the
    given alphabet and the values are the scores for each alignment
    """
    alphabet_copy = set(alphabet)
    alphabet_copy.add("-")

    score_dict = {}
    for first_char in alphabet_copy:
        char_dict = []
        for second_char in alphabet_copy:
            if first_char == "-" or second_char == "-":
                char_dict.append((second_char, dash_score))
            elif first_char == second_char:
                char_dict.append((second_char, diag_score))
            else:
                char_dict.append((second_char, off_diag_score))
        score_dict[first_char] = dict(char_dict)

    return score_dict


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """Compute a pairwise alignment of seq_x and seq_y.

    Input: seq_x and seq_y are strings of sequences whose elements share a
    common alphabet with scoring_matrix. scoring_matrix is a dictionary of
    dictionaries where each key is a letter in the given alphabet and the
    values are the scores for each alignment. global_flag is a Boolean flag
    to determine if a global (True) alignment should be computed

    Output: a local or global scoring matrix of pairwise alignments of
    seq_x and seq_y
    """
    scm = scoring_matrix
    seq_x_len = len(seq_x) + 1
    seq_y_len = len(seq_y) + 1

    table = [[0 for _ in range(seq_y_len)] for _ in range(seq_x_len)]

    if global_flag is True:
        for row in range(1, seq_x_len):
            table[row][0] = table[row - 1][0] + scm[seq_x[row - 1]]["-"]

        for col in range(1, seq_y_len):
            table[0][col] = table[0][col - 1] + scm["-"][seq_y[col - 1]]

        for row in range(1, seq_x_len):
            for col in range(1, seq_y_len):
                val_up = table[row - 1][col] + scm[seq_x[row - 1]]["-"]
                val_left = table[row][col - 1] + scm["-"][seq_y[col - 1]]
                val_up_left = (table[row - 1][col - 1] +
                               scm[seq_x[row - 1]][seq_y[col - 1]])
                table[row][col] = max(val_up, val_left, val_up_left)

    else:
        for row in range(1, seq_x_len):
            table[row][0] = max(table[row - 1][0] + scm[seq_x[row - 1]]["-"], 0)

        for col in range(1, seq_y_len):
            table[0][col] = max(table[0][col - 1] + scm["-"][seq_y[col - 1]], 0)

        for row in range(1, seq_x_len):
            for col in range(1, seq_y_len):
                val_up = table[row - 1][col] + scm[seq_x[row - 1]]["-"]
                val_left = table[row][col - 1] + scm["-"][seq_y[col - 1]]
                val_up_left = (table[row - 1][col - 1] +
                               scm[seq_x[row - 1]][seq_y[col - 1]])
                table[row][col] = max(val_up, val_left, val_up_left, 0)

    return table


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """Compute a global alignment of seq_x and seq_y.

    Input: seq_x and seq_y are strings are strings of sequences whose elements
    share a common alphabet with scoring_matrix. scoring_matrix is a dictionary
    of dictionaries where each key is a letter in the given alphabet and the
    values are the scores for each alignment. alignment_matrix is a global
    matrix of scores of pairwise elements of seq_x and seq_y

    Output: A tuple with a global pairwise alignment of seq_x and seq_y and its
    score in the form (score, seq_x, seq_y)
    """
    alm = alignment_matrix
    scm = scoring_matrix

    seq_x_len = len(seq_x)
    seq_y_len = len(seq_y)

    new_seq_x = ''
    new_seq_y = ''

    while seq_x_len != 0 and seq_y_len != 0:
        if alm[seq_x_len][seq_y_len] == (alm[seq_x_len - 1][seq_y_len - 1] +
                                         scm[seq_x[seq_x_len - 1]]
                                            [seq_y[seq_y_len - 1]]):
            new_seq_x = seq_x[seq_x_len - 1] + new_seq_x
            new_seq_y = seq_y[seq_y_len - 1] + new_seq_y
            seq_x_len -= 1
            seq_y_len -= 1
        else:
            if alm[seq_x_len][seq_y_len] == (alm[seq_x_len - 1][seq_y_len] +
                                             scm[seq_x[seq_x_len - 1]]['-']):
                new_seq_x = seq_x[seq_x_len - 1] + new_seq_x
                new_seq_y = '-' + new_seq_y
                seq_x_len -= 1
            else:
                new_seq_x = '-' + new_seq_x
                new_seq_y = seq_y[seq_y_len - 1] + new_seq_y
                seq_y_len -= 1
    while seq_x_len != 0:
        new_seq_x = seq_x[seq_x_len - 1] + new_seq_x
        new_seq_y = '-' + new_seq_y
        seq_x_len -= 1
    while seq_y_len != 0:
        new_seq_x = '-' + new_seq_x
        new_seq_y = seq_y[seq_y_len - 1] + new_seq_y
        seq_y_len -= 1

    score = 0
    for idx in range(len(new_seq_x)):
        score += scm[new_seq_x[idx]][new_seq_y[idx]]

    return (score, new_seq_x, new_seq_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """Compute a local alignment of seq_x and seq_y.

    Input: seq_x and seq_y are strings are strings of sequences whose elements
    share a common alphabet with scoring_matrix. scoring_matrix is a dictionary
    of dictionaries where each key is a letter in the given alphabet and the
    values are the scores for each alignment. alignment_matrix is a local
    matrix of scores of pairwise elements of seq_x and seq_y

    Output: A tuple with a local pairwise alignment of seq_x and seq_y and its
    score in the form (score, seq_x, seq_y)
    """
    score, new_seq_x, new_seq_y = 0, '', ''

    for row in range(len(alignment_matrix)):
        for col in range(len(alignment_matrix[row])):
            if alignment_matrix[row][col] >= score:
                score = alignment_matrix[row][col]
                max_row, max_col = row, col

    while max_row > 0 and max_col > 0 and alignment_matrix[max_row][max_col] > 0:
        curr_score = alignment_matrix[max_row][max_col]
        if curr_score == (alignment_matrix[max_row - 1][max_col - 1] +
                          scoring_matrix[seq_x[max_row - 1]]
                                        [seq_y[max_col - 1]]):
            new_seq_x = seq_x[max_row - 1] + new_seq_x
            new_seq_y = seq_y[max_col - 1] + new_seq_y
            max_row -= 1
            max_col -= 1
        else:
            if curr_score == (alignment_matrix[max_row - 1][max_col] +
                              scoring_matrix['-'][seq_x[max_row - 1]]):
                if curr_score > 0:
                    new_seq_x = seq_x[max_row - 1] + new_seq_x
                    new_seq_y = '-' + new_seq_y
                max_row -= 1
            else:
                if curr_score > 0:
                    new_seq_x = '-' + new_seq_x
                    new_seq_y = seq_y[max_col - 1] + new_seq_y
                max_col -= 1

    return (score, new_seq_x, new_seq_y)
