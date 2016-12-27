Vizualizace využití spektra na základě dat volně poskytovaných ČTU ke dni
07.02.2016.

    - http://spektrum.ctu.cz/kmitocty
    - http://spektrum.ctu.cz/export/csv-zip
    - http://data.ctu.cz/dataset/vyuziti-radioveho-spektra-spektrum

Výstup ze scriptu show.py je ve formátu SNG

    - http://www.catb.org/~esr/writings/taoup/html/ch06s01.html#id2910193
    - http://sng.sourceforge.net/

Převeden na PNG:

    ./show.py > out.sng; sng out.sng

Script počítá mezi data frekvence otagované následujícími tagy, i když některé z nich nemusí být zrovna data:

    - 2G
    - 3G
    - 4G
    - 700 MHz
    - 800 MHz
    - 900 MHz
    - Bluetooth
    - bod-bod
    - bod-více bodů
    - CDMA
    - Datové spoje
    - E-GSM
    - FWA
    - Galileo
    - GLONASS
    - GPS
    - GSM
    - GSM-R
    - IMT-A
    - LTE
    - LTE-A
    - Mobil
    - mobil
    - Mobilní sítě
    - mobilní sítě
    - Mobilní síť
    - Mobily
    - P-P
    - Pevné spoje
    - pevný bezdrátový přístup
    - pásmo 1800 MHz
    - pásmo 800 MHz
    - pásmo 900 MHz
    - Přenos dat
    - Přenos dat na společných kmitočtech
    - Radio LAN
    - RLAN
    - terminály pro komunikaci pomocí družic
    - UMTS
    - UMTS FDD
    - UMTS TDD
    - WiFi
    - Širokopásmový přenos dat
