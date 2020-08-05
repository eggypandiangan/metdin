#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 03:52:29 2020

@author: aii
"""

import numpy as np
import xarray as xr

#dataset 1: uwnd
U=xr.open_dataset('Data/uwnd.mon.mean.nc')
#dataset 2: vwnd
V=xr.open_dataset('Data/vwnd.mon.mean.nc')
#dataset 3: Precipitation
Pr=xr.open_dataset('Data/prate.sfc.mon.mean.nc')


seas='DJF'
lev=850
judul='Rainfall and Wind '+str(lev)+' Climatology ' + seas
prate=Pr.prate
uwnds=U.uwnd.sel(level=lev)
vwnds=V.vwnd.sel(level=lev)

#Hitung akumulasi curah hujan bulanan
ndays = prate.time.dt.days_in_month
prec=prate*3600*24*ndays

#klimatologi
uclim=uwnds.groupby('time.season').mean(dim='time')
vclim=vwnds.groupby('time.season').mean(dim='time')
prclim=prec.groupby('time.season').mean(dim='time')


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
#projection
mproj=ccrs.PlateCarree()

#figure dan axis 
fig = plt.figure(figsize=(14,12))
ax = plt.axes(projection=mproj)
ax.set_title(judul, fontsize=23);
currentAxis = plt.gca()
currentAxis.add_patch(plt.Rectangle(xy=(110,-15),width=20,height=10,
                                    linewidth= 3, edgecolor='red', fill=False))
#contourfill presipitasi
bound=[0,100,200,300,400,500,600,700]
cf=ax.contourf(prec.lon,prec.lat,prclim.sel(season=seas),
               bound,
               cmap=plt.cm.jet,
               transform=mproj)

#quiver untuk vektor angin
[xlon,ylat]=np.meshgrid(uwnds.lon,uwnds.lat)
qui=ax.quiver(xlon,ylat,uclim.sel(season=seas),vclim.sel(season=seas),
              transform=mproj,
              units='xy',
              scale=1.5)

ax.set_extent((30,180,-30, 60),crs=mproj)

#tambahkan colorbar
cb = plt.colorbar(cf, orientation='horizontal', pad=0.03, extend='both')
cb.set_label('Rainfall (milimeter)')
#tambahkan beberapa fitur peta
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
#tambahkan grid line
ax.gridlines(draw_labels=True)
plt.savefig(judul+'.png')