# define variables
polindrom = str(input())
rev_pol = polindrom[::-1]
# condition
if polindrom == rev_pol:
    print(polindrom+" is polindrom")
else:
    print(polindrom+" is not polindrom")