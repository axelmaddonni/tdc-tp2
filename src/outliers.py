from math import sqrt

fallo_importar_stats = False
try:
    from scipy import stats
except:
    print 'Te olvidaste de instalar las dependencias! No te va a decir si ' \
        'es una ruta submarina.'
    print 'Corre'
    print '    make install-deps'
    print ''
    fallo_importar_stats = True



ALPHA = 0.05

def thompson_tau(n):
    t_a2 = stats.t.ppf(1 - ALPHA / 2.0, n - 2)
    return t_a2 * (n - 1) / (sqrt(n) * sqrt(n-2 + t_a2**2))

