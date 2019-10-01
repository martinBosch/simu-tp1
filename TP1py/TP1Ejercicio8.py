#75.26 Simulación - TP1
#Grupo 5
#79979 – González, Juan Manuel (juanmg0511@gmail.com)<br />
#92028 – Tusca, Bautista (bautista.tusca@gmail.com)<br />
#93272 – Zapico, Rodrigo (rodri.zapico@gmail.com)<br />
#96749 – Bosch, Martín (martinbosch17@gmail.com)

#Ejercicio 8

from matplotlib import pyplot as plt
import scipy.stats as stats


class GCL:
    """Generador Lineal Congruente

    atributos:
     m: el modulo
     a: el multiplicador
     c: el incremento
     xn: ultimo valor generado
    """

    def __init__(self, m, a, c, x0):
        self.m = m
        self.a = a
        self.c = c
        self.xn = x0

    def generar_numero_aleatorio(self):
        self.xn = (self.a * self.xn + self.c) % self.m
        return self.xn

    def generar_numero_aleatorio_uniforme(self):
        return self.generar_numero_aleatorio()/m


m = 2**32
a = 1013904223
c = 1664525

padrones = [93272, 92028, 79979, 96749]
x0 = int(sum(padrones)/len(padrones))


def generar_secuencia(secuencia_largo):
    gcl = GCL(m, a, c, x0)
    secuencia = []
    for i in range(secuencia_largo):
        secuencia.append(gcl.generar_numero_aleatorio_uniforme())

    return secuencia


tam_muestra = 100000
muestras = generar_secuencia(tam_muestra)


alfa, beta = 0.3, 0.6

#calculo las probabilidades, corto cuando ya no distingo diferencia
esperados = [beta - alfa]
termino = False
i = 1
while not termino:
    nuevaProb = esperados[0] * ((1 - esperados[0]) ** i)

    if nuevaProb == esperados[i - 1]:
        termino = True
    else:
        esperados.append(nuevaProb)
        i += 1

# calculo cantidad de veces que cai 0 afuera, 1 afuera, 2 afuera...
primero = True
contador_veces_cae_afuera = 0
veces_cae_afuera = {}
for x in muestras:
    if (x >= alfa and x <= beta) and primero:
        primero = False
    if (x >= alfa and x <= beta) and not primero:
        veces = veces_cae_afuera.get(contador_veces_cae_afuera, 0)
        veces_cae_afuera[contador_veces_cae_afuera] = veces + 1
        contador_veces_cae_afuera = 0
    if (x < alfa or x > beta) and not primero:
        contador_veces_cae_afuera += 1

# ajusto para que sean frecuencias
total = sum(veces_cae_afuera.values())
for k in veces_cae_afuera.keys():
    veces_cae_afuera[k] /= total

# lo paso a lista y relleno con 0 donde no tuve apariciones
observados = []
for i in range(len(esperados)):
    observados.append(veces_cae_afuera.get(i, 0))

Dsquared, p = stats.chisquare(observados, esperados)
print('D^2:', Dsquared)
print('p:', p)
