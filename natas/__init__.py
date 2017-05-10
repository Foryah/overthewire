import sys, os

sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))
        ), 
        'lib'
    )
)

print(sys.path)
