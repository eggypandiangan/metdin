#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 19:59:32 2020

@author: aii
"""

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

##############IMPORT DATA
V=xr.open_dataset('Data/vwnd.mon.mean.nc')
U=xr.open_dataset('Data/uwnd.mon.mean.nc')
Pr=xr.open_dataset('Data/prate.sfc.mon.mean.nc')
ndays = Pr.time.dt.days_in_month
prec=Pr*3600*24*ndays

ausmi=U.uwnd.sel(level=850,lon=slice(110,130),lat=slice(-5,-15)).mean(axis=(1,2))


prec1=prec.prate.groupby('time.month').mean(dim='time')
prec_jan=prec1.sel(month=1)
prec_feb=prec1.sel(month=2)
prec_mar=prec1.sel(month=3)
pr_djf=((prec_jan+prec_feb+prec_mar)*1/3)
                              
pr_djf_k=pr_djf.sel(lon=slice(120,150),lat=slice(-7.5,-17.5)).mean(axis=(1,2))    

prec_bln=np.append(pr_djf[7:12],pr_djf[0:7])

aus_djf=ausmi.groupby('time.season').mean(dim='time')
aus_djfs=aus_djf.sel(season=seas)                                          
std_au=ausmi.std()

aus_bln=ausmi.groupby("time.month").mean(dim='time')

aus_bln1=np.append(aus_bln[7:12],aus_bln[0:7])



judul='Mean AUSMI & Rainfall monthly'
# x=['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agt','Sep','Okt','Nov','Des']
x=['Agt','Sep','Okt','Nov','Des','Jan','Feb','Mar','Apr','Mei','Jun','Jul']
##############PLOT GRAFIK AUSMI
fig=plt.figure(figsize=(14,7))
ax1=fig.add_subplot()
ax2=ax1.twinx()
ax1.plot(x,aus_bln1, 'r')
ax2.bar(x,prec_bln, alpha=0.4)
plt.grid()
xs = np.array(np.arange(0,12,1),dtype=np.float32)
ys = np.array(aus_bln1.data)
# for x,y in zip(xs,ys):
#     label = "{:.2f}".format(y)
#     plt.annotate(label, # this is the text
#                  (x,y), # this is the point to label
#                  textcoords="offset points", # how to position the text
#                  xytext=(0,10), # distance from text to points (x,y)
#                  ha='center') # horizontal alignment can be left, right or center
plt.title(judul)
ax1.set_ylabel('AUSMI')
ax2.set_ylabel('Rainfall (mm)')
plt.xlabel('Bulan')
plt.axhline(y=161.5, color='black')
plt.savefig(judul+'.png')
######################################


#####HITUNG CORRELATION
from scipy.stats import pearsonr
# aa=pearsonr(ausmi,prec.prate)

lon=prec.lon
lat=prec.lat
data = np.random.rand(192, 94)
cor = np.zeros((len(lat),len(lon)))

for i in range(len(lat)):
    for j in range(len(lon)):
        cor[i,j], pvalue=pearsonr(ausmi,prec.prate.data[:,i,j])

ds=xr.DataArray(cor, dims=('lat','lon'), coords={'lat':lat, 'lon':lon},)        
############################################################################################

judul='Correlation AUSMI to precip'
#projection
mproj=ccrs.PlateCarree()
#figure dan axis 
fig = plt.figure(figsize=(14,12))
ax = plt.axes(projection=mproj)
ax.set_title(judul, fontsize=23);
currentAxis = plt.gca()
currentAxis.add_patch(plt.Rectangle(xy=(110,-15),width=20,height=10,
                                    linewidth= 3, edgecolor='blue', fill=False))
currentAxis.add_patch(plt.Rectangle(xy=(120,-17.5),width=30,height=10,
                                    linewidth= 3, edgecolor='black', fill=False))

#contourfill presipitasi
cf=ax.contourf(ds.lon,ds.lat,ds,
               cmap=plt.cm.jet,
               transform=mproj)
ax.set_extent((30,180,-30, 60),crs=mproj)
#tambahkan colorbar
cb = plt.colorbar(cf, orientation='horizontal', pad=0.03, extend='both')
cb.set_label('Coeficient Correlation')
#tambahkan beberapa fitur peta
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
#tambahkan grid line
ax.gridlines(draw_labels=True)
plt.savefig(judul+'.png')
##########################################################################

