#-------------------------------------------------------------------------------
# Name:         informe
# Purpose:      Muestra distintos informes de acuerdo a la inyeccion y cruce realizados anteriormente
#
# Author:       Rene Ulloa
#
# Created:      09/11/2011
# Copyright:    (c) chechex 2011
# Licence:      GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys

sys.path.append("./clases")
from clsInforme import clsInforme

def main():
    i = clsInforme("informe.cfg")

if __name__ == '__main__':
    main()