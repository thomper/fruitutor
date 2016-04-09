def reshape_1d_to_2d(seq, row_length):
    return tuple((tuple(seq[i:i + row_length] for i in
                                               range(0, len(seq), row_length))))
