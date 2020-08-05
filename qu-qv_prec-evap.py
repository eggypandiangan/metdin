#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 20:53:14 2020

@author: aii
"""
#####prec-evap vs moist transport u-v vector

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy import integrate


fQ=xr.open_dataset('Data/shum.mon.mean.nc')
fPr=xr.open_dataset('Data/prate.sfc.mon.mean.nc')
fEp=xr.open_dataset('Data/pevpr.sfc.mon.mean.nc')
pr=fPr.prate.data
ep=fEp.pevpr.data
prate=fPr.prate
erate=fEp.pevpr
pr_ep=prec-erate
ndays = prate.time.dt.days_in_month
prec = prate*3600*24*ndays

pr_epclim=pr_ep.groupby('time.month').mean(dim='time')

g=9.8;
Qu=fQ.shum/1000*fU.uwnd.sel(level=slice(1000,300)) ##level bawah 1000 sd 300 pakai operator slice. SLice bisa dipakai di lon lat 
Qv=fQ.shum/1000*fV.vwnd.sel(level=slice(1000,300))

#trapezoid
BQu=-1*100./g*integrate.trapz(Qu,x=Qu.level,axis=1)  #   yg trapezoid int dari 300 ke 1000 maka dikali -1
BQv=-1*100./g*integrate.trapz(Qv,x=Qv.level,axis=1)

#combine ke DataArray Qu dan Qv
Qu['BQu']=(('time','lat','lon'),BQu)  ###insert data array kita BQu ke data lama Qu
Qv['BQv']=(('time','lat','lon'),BQv)

BQu_clim=Qu.BQu.groupby('time.month').mean(dim='time')  ###grup berdasarkan time dgn informasi waktu season
BQv_clim=Qv.BQv.groupby('time.month').mean(dim='time')



#projection
mproj=ccrs.PlateCarree()
#figure dan axes 
fig = plt.figure(1, figsize=(14, 12))
ax = plt.axes(projection=mproj)

#contourfill magnitude
lvl=np.linspace(100,500,10)
cf=ax.contourf(pr_ep.lon,pr_ep.lat,pr_epclim.sel(month=1),
               cmap=plt.cm.jet,
               transform=mproj)
               #levels=lvl)
               #zorder=2,
               #alpha=0.65,)
#cb = plt.colorbar(cf, orientation='vertical', aspect=50)#, pad=0, aspect=50)
cb = plt.colorbar(cf, orientation='horizontal', aspect=50)#, pad=0, aspect=50)

#vector
qui=ax.quiver(xlon,ylat,BQu_clim[0,:,:],BQv_clim[0,:,:],transform=mproj)

#tambahkan map feature
ax.add_feature(cfeature.LAND)
#ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_extent((90,150, -20, 20),crs=mproj)
#grid line
ax.gridlines(draw_labels=True)

