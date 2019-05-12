import time

def msgs(n, length=1000, delay=None):
    """Generate n messages of length ending with new line char
    """

    msg = bytearray(b'00000' + (length-6) * b'a' + b'\n')

    for i in range(1, n+1):
        if delay is not None:
            time.sleep(delay)
        msg[:5] = b'%5.5d' % i
        yield msg

def report(n_sent, n_rcvd):
    """Print report on sent/received msgs
    """

    delta = len(n_sent) - len(n_rcvd)
    if delta > 0:
        n_rcvd.extend([0 for i in range(delta)])
    elif delta < 0:
        n_sent.extend([0 for i in range(-delta)])
    print(' n   sent  rcvd')
    print('---------------')
    for e in enumerate(zip(n_sent, n_rcvd)):
        print(e)
    print('total', (sum(n_sent), sum(n_rcvd)))

