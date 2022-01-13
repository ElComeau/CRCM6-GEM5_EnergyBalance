#  Evaluating the surface energy balance of the Canadian Regional Climate Model 6 - Global Environmental Multiscale 5 (CRCM6-GEM5)

*La version française suit.*

This repository is for storing the code I have written for an internship started during the summer of 2021 at Université du Québec à Montréal (UQÀM) under the direction of professor Alejandro Di Luca. The internship concerns the evaluation of the Canadian Regional Climate Model 6 - Global Environmental Multiscale 5 (CRCM6-GEM5)'s surface energy balance (SEB).

The CRCM6-GEM5 model is compared with observational data collected by the AmeriFlux (AMF) network. The network is composed of a group of over a hundred weather stations that collects data pertinent to the SEB, such as the incoming and outgoing shortwave and longwave radiation, the sensible heat flux, and the latent heat flux, among many other variables, usually at 30 minute intervals. For this study, a total of 58 stations located across North America are utilized, with each station containing at least one year's worth of data beween the years 1990 and 2017.

In order to facilitate the comparison between the model and the observations, the AMF data need to be temporally averaged in order to produce 3 hour means from the original 30 minute means. Hence, the temporally averaged AMF data is of the same temporal frequency as the CRCM6-GEM5 simulations. Furthermore, each AMF station must be matched to the closest grid point in the model.

The comparison between the model and the observations is done using two approaches. In the first approach, the three-hourly and monthly quartiles for the CRCM6-GEM5 simulations and the AMF data are compared against each other for each of the previously mentioned SEB variables. In the second approach, the values of the net radiation and the latent heat flux are discretized (binned), with each combination of net radiation and latent heat flux bin producing a regime. The frequency and the mean intensity of the sensible heat flux of each regime are calculated for the AMF observations and for the CRCM6-GEM5 simulations. The frequencies and the intensities of the observational and simulated data are then compared against each other by regime.

___

# Évaluation du bilan énergétique à la surface du Modèle régional canadien du climat 6 - *Global Environmental Multiscale 5* (MRCC6-GEM5)

Ce dépôt sert à stocker le code que j'ai écrit pour un stage commencé durant l'été 2021 à l'Université du Québec à Montréal (UQÀM) sous la direction du professeur Alejandro Di Luca. Le stage concerne l'évaluation du bilan d'énergie à la surface (BES) du Modèle régional canadien du climat 6 - *Global Environmental Multiscale 5* (MRCC6-GEM5).

Le modèle MRCC6-GEM5 est conmparé avec des données d'observation collectées par le réseau AmeriFlux (AMF). Le réseau est composé d'un groupe de plus d'une centaine de stations météorologiques qui collectent des données pertinentes au BES, telles que la radiation d'ondes courtes et longues qui atteingnent et qui quittent la suface, le flux de chaleur sensible et le flux de chaleur latente, parmis de nombreuses autres variables, généralement à un intervalle de 30 minutes. Pour cette étude, un total de 58 stations situées à travers l'Amérique du Nord sont utilisées, où chaque station contient au moins l'équivalent d'un an de données entre les années 1990 et 2017.

Afin de faciliter la comparaison entre le modèle et les observations, les données d'AMF doivent être moyennées temporellement pour produire des moyennes sur 3 heures à partir des moyennes originales sur 30 minutes. Ainsi, les données temporellement moyennées d'AMF ont la même fréquence temporelle que les simulations du MRCC6-GEM5. De plus, chaque station AMF doit être jumelée avec le point de grille du modèle le plus proche.

La comparaison entre le modèle et les observations est faite en utilisant deux approches. Dans la première approche, les quartiles sur 3 heures et mensuelles des simulations du MRCC6-GEM5 et des données d'AMF sont comparés entre eux pour chacune des variables du BES mentionnées plus tôt. Dans la deuxième approche, les valeurs de la radiation nette et du flux de chaleur latente sont discrétisées (groupées par classe), où chaque combinaison de classe de radiation nette et de flux de chaleur latente produit un régime. La fréquence et l'intensité moyenne du flux de chaleur sensible associées à chaque régime sont calculées pour les observations d'AMF et pour les simulations du MRCC6-GEM5. Les fréquences et les intensités des données d'observation et de simulation sont ensuite comparées entre elles selon le régime.

___

We acknowledge the support of the Natural Sciences and Engineering Research Council of Canada (NSERC).

Nous remercions le Conseil de recherches en sciences naturelles et en génie du Canada (CRSNG) de son soutien.

![alt text](https://github.com/ElComeau/CRCM6-GEM5_EnergyBalance/blob/main/NSERC_FIP_RGB.jpg)
