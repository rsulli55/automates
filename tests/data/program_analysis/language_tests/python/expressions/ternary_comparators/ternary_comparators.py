import sys


def main(x1, x2, x3, x4):
    a = x1 < x2 < x3
    b = x4 >= x3 >= x2
    return a, b


print(
    main(
        int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    )
)