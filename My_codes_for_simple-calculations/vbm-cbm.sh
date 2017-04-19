for i in -1.0 -0.5 +0.0 +0.5 +1.0
do
cd us$i
cd PBE_bands
cp ../../{bandgap.pl,vbm-cbm.py} .
perl bandgap.pl > abc
python vbm-cbm.py
cd ../../
done
