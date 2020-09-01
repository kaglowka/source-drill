from .Vector_Similarity import TS_SS


def ts_ss_normalized(v1, v2):
    ts_ss = TS_SS(v1, v2)
    return 1/(1 + ts_ss)