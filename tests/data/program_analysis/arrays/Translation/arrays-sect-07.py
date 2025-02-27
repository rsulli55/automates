from automates.program_analysis.for2py.format import *
from automates.program_analysis.for2py.arrays import *

def main():
    A = Array([(1,5)])
    B = Array([(1,3)])

    # B = (/2,3,4/)
    B.set_elems(array_subscripts(B), [2,3,4])

    for i in range(1,5+1):
        A.set_(i, 0)

    fmt_obj = Format(['5(I5)'])

    sys.stdout.write(fmt_obj.write_line([A.get_(1), A.get_(2), A.get_(3), A.get_(4), A.get_(5)]))

    A.set_elems(array_values(B), 17)

    sys.stdout.write(fmt_obj.write_line([A.get_(1), A.get_(2), A.get_(3), A.get_(4), A.get_(5)]))


main()
