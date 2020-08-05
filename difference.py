#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 16:33:25 2020

@author: aii
"""
# =============================================================================
# library needed
# =============================================================================
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
#####################################################################################

# =============================================================================
# #data
# =============================================================================
V=xr.open_dataset('Data/vwnd.mon.mean.nc')
U=xr.open_dataset('Data/uwnd.mon.mean.nc')
Pr=xr.open_dataset('Data/prate.sfc.mon.mean.nc')
ndays = Pr.time.dt.days_in_month
prec=Pr*3600*24*ndays

# =============================================================================
# #IndexError()
# =============================================================================
#IMI
imi=U.uwnd.sel(level=850,lon=slice(40,80),lat=slice(15,5)).mean(axis=(1,2)) - \
    U.uwnd.sel(level=850,lon=slice(70,90),lat=slice(30,20)).mean(axis=(1,2))
#WNPMI
wnpmi=U.uwnd.sel(level=850,lon=slice(100,130),lat=slice(15,5)).mean(axis=(1,2)) - \
      U.uwnd.sel(level=850,lon=slice(110,140),lat=slice(30,20)).mean(axis=(1,2))
#AUSMI
ausmi=U.uwnd.sel(level=850,lon=slice(110,130),lat=slice(-5,-15)).mean(axis=(1,2))


# =============================================================================
# # Climatology
# =============================================================================
lev=850               #######GANTI LEVEL
# seas='JJA'            ###########GANTI SEASON
vec_scl=1          ###############GANTI VECTOR SCALE
# juduls='Rainfall and Wind '+str(lev)+' Climatology ' + seas
# prates=Pr.prate
# ndays = prates.time.dt.days_in_month
# precs=prates*3600*24*ndays
# uwnds=U.uwnd.sel(level=lev)
# vwnds=V.vwnd.sel(level=lev)
# uclim=uwnds.groupby('time.season').mean(dim='time')
# vclim=vwnds.groupby('time.season').mean(dim='time')
# prclim=precs.groupby('time.season').mean(dim='time')

# # =============================================================================
# ##AUSMI  
# # =============================================================================
# ausmi_s=ausmi.data>ausmi.data.std() ############STRONG
# precip_s=prec.prate.data[ausmi_s,:,:].mean(axis=0)
# lvl=850         ######GANTI LEVEL
# uaus_s=U.uwnd.sel(level=lvl).data[ausmi_s,:,:].mean(axis=0)
# vaus_s=V.vwnd.sel(level=lvl).data[ausmi_s,:,:].mean(axis=0)

# ausmi_w=ausmi.data<ausmi.data.std() ############WEAK
# precip_w=prec.prate.data[ausmi_w,:,:].mean(axis=0)
# uaus_w=U.uwnd.sel(level=lvl).data[ausmi_w,:,:].mean(axis=0)
# vaus_w=V.vwnd.sel(level=lvl).data[ausmi_w,:,:].mean(axis=0)

# ausmi_ss=ausmi.data[ausmi_s]

# =============================================================================
# ##IMI 
# =============================================================================
# imi_s=imi.data>imi.data.std() ############STRONG
# precip_s=prec.prate.data[imi_s,:,:].mean(axis=0)
# # lvl=850         ######GANTI LEVEL
# uimi_s=U.uwnd.sel(level=lev).data[imi_s,:,:].mean(axis=0)
# vimi_s=V.vwnd.sel(level=lev).data[imi_s,:,:].mean(axis=0)

# imi_w=imi.data<imi.data.std() ############WEAK
# precip_w=prec.prate.data[imi_w,:,:].mean(axis=0)
# uimi_w=U.uwnd.sel(level=lev).data[imi_w,:,:].mean(axis=0)
# vimi_w=V.vwnd.sel(level=lev).data[imi_w,:,:].mean(axis=0)

# =============================================================================
# WNPMI
# =============================================================================
wnpmi_s=wnpmi.data>wnpmi.data.std() ############STRONG
precip_s=prec.prate.data[wnpmi_s,:,:].mean(axis=0)
# lvl=850         ######GANTI LEVEL
uwnpmi_s=U.uwnd.sel(level=lev).data[wnpmi_s,:,:].mean(axis=0)
vwnpmi_s=V.vwnd.sel(level=lev).data[wnpmi_s,:,:].mean(axis=0)

wnpmi_w=wnpmi.data<wnpmi.data.std() ############WEAK
precip_w=prec.prate.data[wnpmi_w,:,:].mean(axis=0)
uwnpmi_w=U.uwnd.sel(level=lev).data[wnpmi_w,:,:].mean(axis=0)
vwnpmi_w=V.vwnd.sel(level=lev).data[wnpmi_w,:,:].mean(axis=0)

# # =============================================================================
# wind vector 200 hpa + prec in ausmi strong - weak
# =============================================================================
judul='Wind '+str(lev)+' hPa WNPMI weak'
#projection
mproj=ccrs.PlateCarree()
#figure dan axes 
fig = plt.figure(1, figsize=(14, 12))
ax = plt.axes(projection=mproj)
ax.set_title(judul, fontsize=23);
# currentAxis = plt.gca()
# currentAxis.add_patch(plt.Rectangle(xy=(110,-15),width=20,height=10,
#                                     linewidth= 3, edgecolor='red', fill=False))
# #contourfill magnitude
# bound=[0,100,200,300,400,500,600,700]
# cf=ax.contourf(Pr.lon.data, Pr.lat.data,precip_w,
#                bound,
#                 #cmap=plt.cm.bwr,
#                 cmap=plt.cm.jet,
#                 transform=mproj)
# cb = plt.colorbar(cf, orientation='horizontal', pad=0.03)
# cb.set_label('Rainfall Difference (milimeter)')
#quiver untuk vektor angin AUSMI strong - uv weak (200)
[xlon,ylat]=np.meshgrid(U.uwnd.lon,V.vwnd.lat)
qui=ax.quiver(xlon,ylat,uwnpmi_w,
              vwnpmi_w,
              transform=mproj,
              units='xy',
              scale=vec_scl)
# #tambahkan map feature
# title('Precip & Wind 200 hpa AUSMI strong - weak')
ax.add_feature(cfeature.LAND)
#ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_extent((30,180,-30, 60),crs=mproj)
#grid line
ax.gridlines(draw_labels=True)
plt.savefig(judul+'.png')


# =============================================================================
# Klim DJF & JJA
# =============================================================================


#projection
# mproj=ccrs.PlateCarree()
# #figure dan axis 
# fig = plt.figure(figsize=(14,12))
# ax = plt.axes(projection=mproj)
# ax.set_title(juduls, fontsize=23);
# # currentAxis = plt.gca()
# # currentAxis.add_patch(plt.Rectangle(xy=(110,-15),width=20,height=10,
# #                                     linewidth= 3, edgecolor='red', fill=False))
# #contourfill presipitasi
# bound=[0,100,200,300,400,500,600,700]
# cf=ax.contourf(precs.lon,precs.lat,prclim.sel(season=seas),
#                 bound,
#                 cmap=plt.cm.jet,
#                 transform=mproj)

# #quiver untuk vektor angin
# [xlon,ylat]=np.meshgrid(uwnds.lon,uwnds.lat)
# qui=ax.quiver(xlon,ylat,uclim.sel(season=seas),vclim.sel(season=seas),
#               transform=mproj,
#               units='xy',
#               scale=vec_scl)

# ax.set_extent((30,180,-30, 60),crs=mproj)

# #tambahkan colorbar
# cb = plt.colorbar(cf, orientation='horizontal', pad=0.03)
# cb.set_label('Rainfall (milimeter)')
# #tambahkan beberapa fitur peta
# ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
# #tambahkan grid line
# ax.gridlines(draw_labels=True)
# plt.savefig(juduls+'.png')

