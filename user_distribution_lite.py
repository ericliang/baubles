import sys
import pygeoip
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 8))
fig.suptitle('User distribution, 2010-2011 China', fontsize='large')

####################
#
# get the ip-numbers
#
####################

f = open("ip_num.dat", "rt")
ips = []
numbers = []
ip, number = '1.1.1.1', '0'
for line in f:
    ip, number = line.split()
    ips.append(ip), numbers.append( float(number) )

#print ips, numbers


####################
#
# ip -> city-location
#
####################

gic = pygeoip.GeoIP('/home/sunny/Downloads/GeoLiteCity.dat')

cities = []
lons = []
lats = []
city_numbers = []
number_nocity = 0
number_foreign = 0
number_cn = 0
for ip,number in zip(ips, numbers):
    R = gic.record_by_addr(ip)
    try:
        country = R.get('country_code')
        if country == 'CN':
            number_cn += number
        
            city, lon, lat = R.get('city'), R.get('longitude'), R.get('latitude')
            
            try:
                i = cities.index(city)
                city_numbers[i] += number
                
            except ValueError:
                cities.append( city )
                lons.append( lon )
                lats.append( lat )
                city_numbers.append( number )
        else:
            number_foreign += number
        
    except AttributeError:
        number_nocity += number

print 'Ip in China number: ', number_cn
print 'Ip out of China number: ', number_foreign
print 'Ip unknown number: ', number_nocity

#print cities, lons, lats

####################
#
# plot the map
#
####################

# setup Lambert Conformal basemap.
map = Basemap(width=6000000,height=4500000,projection='lcc',
            resolution='c',lat_1=30, lat_2=40,lat_0=35,
            lon_0=107.)

#map.readshapefile('/home/sunny/Downloads/gadm_v1_shp/gadm1', name='countries')
map.readshapefile('/home/sunny/Downloads/CHN_adm/CHN_adm1', name='countries')
map.readshapefile('/home/sunny/Downloads/TWN_adm/TWN_adm0', name='countries')

# compute the native map projection coordinates for cities.
xs,ys = map(lons,lats)

# plot filled circles at the locations of the cities.
from pylab import * 
colors = 6*rand(len(xs))

ax = fig.add_subplot(111)
ax.scatter(xs, ys, s=[0.02*x for x in city_numbers], c=colors, alpha=0.45)
#ax.plot(xs,ys, '.', xs,ys, '-')

plt.savefig('user_distribution.png')
