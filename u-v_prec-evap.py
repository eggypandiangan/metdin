###prec-evap vs u-v wind vector


import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


#dataset 1: uwnd
fU=xr.open_dataset('Data/uwnd.mon.mean.nc')
#dataset 2: vwnd
fV=xr.open_dataset('Data/vwnd.mon.mean.nc')
#dataset 3: Precipitation
fPr=xr.open_dataset('Data/prate.sfc.mon.mean.nc')
fEp=xr.open_dataset('Data/pevpr.sfc.mon.mean.nc')
pr=fPr.prate.data
ep=fEp.pevpr.data

prate=fPr.prate
erate=fEp.pevpr
uwnd=fU.uwnd.sel(level=850)
vwnd=fV.vwnd.sel(level=850)

ndays = prate.time.dt.days_in_month
prec = prate*3600*24*ndays

ddays = erate.time.dt.days_in_month
evap = erate*ddays ####### evap/erate

#pr_ep=prec-erate
pr_ep=prec-evap


uclim=uwnd.groupby('time.month').mean(dim='time')
vclim=vwnd.groupby('time.month').mean(dim='time')
prclim=prec.groupby('time.month').mean(dim='time')
pr_epclim=pr_ep.groupby('time.month').mean(dim='time')
#pr_epclim=pr_ep.groupby('time.month').mean(dim='time')
#epclim=erate.groupby('time.month').mean(dim='time')


mproj=ccrs.PlateCarree()

#figure dan axis 
fig = plt.figure(figsize=(28,12))
ax = plt.axes(projection=mproj)

#contourfill prec-evap
cf=ax.contourf(pr_ep.lon,pr_ep.lat,pr_epclim.sel(month=1),
               cmap=plt.cm.jet,
               transform=mproj)

#quiver untuk vektor angin
[xlon,ylat]=np.meshgrid(uwnd.lon,uwnd.lat)
qui=ax.quiver(xlon,ylat,uclim.sel(month=1),vclim.sel(month=1),
              transform=mproj,
              units='xy',
              scale=2.5)

ax.set_extent((90,150, -15, 15),crs=mproj)

#tambahkan colorbar
cb = plt.colorbar(cf)

#tambahkan beberapa fitur peta
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
#tambahkan grid line
ax.gridlines(draw_labels=True)