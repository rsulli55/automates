from automates.program_analysis.for2py.format import *
from automates.program_analysis.for2py.arrays import *

def main():
    A = Array([(1,5)])

    for i in range(1,5+1):
        A.set_(i, i*i)

    fmt_obj = Format(['5(I5)'])

    sys.stdout.write(fmt_obj.write_line([A.get_(1), A.get_(2), A.get_(3), A.get_(4), A.get_(5)]))

    A_subs = [2,3,4]
    A.set_elems(A_subs, 17)

    sys.stdout.write(fmt_obj.write_line([A.get_(1), A.get_(2), A.get_(3), A.get_(4), A.get_(5)]))


main()
