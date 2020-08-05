#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 09:52:32 2020

@author: aii
"""
######NMME

import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
from cartopy import crs, feature

hcst=xr.open_dataarray('Data/CanCM4/CMC2-CanCM4_Precip_Climatology.nc',decode_times=False)*30

fnames=['Data/CanCM4/pr_daily_cancm4.20200501_E1_20200501-20210430.nc',
       'Data/CanCM4/pr_daily_cancm4.20200501_E2_20200501-20210430.nc',
       'Data/CanCM4/pr_daily_cancm4.20200501_E3_20200501-20210430.nc',
       'Data/CanCM4/pr_daily_cancm4.20200501_E4_20200501-20210430.nc',
       'Data/CanCM4/pr_daily_cancm4.20200501_E5_20200501-20210430.nc']

fcst = xr.open_mfdataset(fnames,concat_dim="ens")

#hitung akumulasi bulanan
dpr=fcst.pr*3600*24
mpr=dpr.groupby('time.month').sum(dim='time')

#Plume
def tsplume(df,dh,ilon,ilat,t1):
    #fcst
    tsf=df.sel(lon=ilon,lat=ilat,method='nearest')
    ts1=tsf.sel(month=slice(1,t1-1))
    ts2=tsf.sel(month=slice(t1,12))
    TSf=xr.concat((ts2,ts1),'month')
    it=TSf.month.values;
    #hcst
    tsh=dh.sel(X=ilon,Y=ilat,method='nearest')
    tsh1=tsh.sel(S=slice(0,t1-2),L=0.5) #0.5
    tsh2=tsh.sel(S=slice(t1-1,11),L=0.5) # 0.5
    TSh=xr.concat((tsh2,tsh1),'S')
    
    #
    fig,ax=plt.subplots(nrows=2,ncols=1,figsize=(14,7))
    ax[0].set_title(lokasi, fontsize=23)
    ax[0].plot(TSf.transpose())
    ax[0].plot(TSh,'--k',linewidth=2)
    ax[0].set_xticks(np.linspace(0,11,12))
    ax[0].set_xticklabels(it)
    ax[0].legend(np.linspace(1,5,5)).set_title('Ens')
    #
    #
    ax[1].boxplot(TSf.transpose())
    ax[1].set_xticklabels(it)
    plt.savefig(lokasi+'.png')
    
# d2=hcst.sel(X=slice(extent[0],extent[1]),Y=slice(extent[2],extent[3]),S=t1-1,L=0.5)    
#Contoh Bandung 107.609918, -6.890670 
#-6.243052, 106.780077 keb lama
#aceh 4.605637, 97.101413
ilon=106.780077
ilat=-6.243052
lokasi='Keb. Lama Jaksel '+ str(ilon) +', '+ str(ilat)
tsplume(mpr,hcst,ilon,ilat,5)

def probmap(mpr,hcst,extent,t1):
    lon=mpr.lon.sel(lon=slice(extent[0],extent[1])) 
    lat=mpr.lat.sel(lat=slice(extent[3],extent[2]))
    #fcst
    # d1=mpr.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[3],extent[2]),month=t1)
    d1=mpr.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[3],extent[2]),
               month=[t1,t1+1,t1+2]).sum(axis=1) # J A S
    #hist
    # d2=hcst.sel(X=slice(extent[0],extent[1]),Y=slice(extent[2],extent[3]),S=t1-1,L=0.5)
    d2=hcst.sel(X=slice(extent[0],extent[1]),
                Y=slice(extent[2],extent[3]),S=t1-1,L=[2.5,3.5,4.5]).sum(axis=0) ######J A S
    #mean + 15% mean
    tholdAN=np.flipud(d2.values+0.15*d2.values)
    #mean - 15% mean
    tholdBN=np.flipud(d2.values-0.15*d2.values)
    #Probabilitas
    ch=d1.values
    nmem,ny,nx=ch.shape
    #Atas normal
    probAN=np.sum(ch>tholdAN,axis=0)/nmem
    #Bawah normal
    probBN=np.sum(ch<tholdBN,axis=0)/nmem
    
    #
    cmap=crs.PlateCarree()
    fig=plt.figure(figsize=(14,6))
    ax=plt.axes(projection=cmap)
    pc=ax.pcolor(lon,lat,probAN, cmap='RdYlBu_r')
    # pc=ax.pcolormesh(lon,lat,probAN, cmap='RdYlBu_r')
    # pc=ax.contourf(lon,lat,probAN,cmap='RdYlBu_r')
    ax.add_feature(feature.COASTLINE.with_scale('50m'))
    plt.colorbar(pc, orientation='horizontal', pad=0.05, fraction=0.069).set_label('Persen')
    ax.gridlines(draw_labels=True)
    plt.title('Peluang Atas Normal JAS')
    plt.savefig('Peluang Atas Normal JAS.png')
    #
    fig=plt.figure(figsize=(14,6))
    ax=plt.axes(projection=cmap)
    pc=ax.pcolor(lon,lat,probBN,cmap='RdYlBu_r')
    # pc=ax.contourf(lon,lat,probAN,cmap='RdYlBu')
    ax.add_feature(feature.COASTLINE.with_scale('50m'))
    plt.colorbar(pc,orientation='horizontal', pad=0.05, fraction=0.069).set_label('Persen')
    ax.gridlines(draw_labels=True)
    plt.title('Peluang Bawah Normal JAS')
    plt.savefig('Peluang Bawah Normal JAS.png')
    
t1=7

extent=[94,141,-15,15]
probmap(mpr,hcst,extent,t1)
