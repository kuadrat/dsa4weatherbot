from random import randint

#_Constants_____________________________________________________________________
## CLoudiness
CLOUDS_NONE = 0
CLOUDS_SOME = 1
CLOUDS_MANY = 2
CLOUDS_FULL = 3
cloud_levels = [CLOUDS_NONE, CLOUDS_SOME, CLOUDS_MANY, CLOUDS_FULL]
## Wind strength
WIND_NONE = 0
WIND_SOFTER = 1
WIND_SOFT = 2
WIND_MEDIUM = 3
WIND_STRONG = 4
WIND_STRONGER = 5
WIND_STORM = 6
wind_levels = [WIND_NONE, WIND_SOFTER, WIND_SOFT, WIND_MEDIUM, WIND_STRONG, 
               WIND_STRONGER, WIND_STORM]
## Precipitation
PRECIPITATION_NONE = 0
PRECIPITATION_LIGHT = 1
PRECIPITATION_MEDIUM = 2
PRECIPITATION_STRONG = 3
precipitation_levels = [PRECIPITATION_NONE, PRECIPITATION_LIGHT, 
                        PRECIPITATION_MEDIUM, PRECIPITATION_STRONG]
## Regions
REGION_ICE = 'Ewiges Eis'
REGION_NE_HEIGHTS = 'Ehernes Schwert'
REGION_HIGH_NORTH = 'Hoher Norden'
REGION_TUNDRA_TAIGA = 'Tundra und Taiga'
REGION_BORNLAND_THORWAL = 'Bornland, Thorwal'
REGION_QUARRELING_KINGDOMS = 'Streitende Königreiche'
REGION_CENTRAL_MIDDLEREALM = 'Zentrales Mittelreich'
REGION_NORTHERN_HORAS = 'Nördliches Horasreich, Almada, Aranien'
REGION_RASCHTUL_HEIGHTS = 'Höhen des Raschtulwalls'
REGION_SOUTHERN_HORAS = 'Südliches Horasreich, Reich der Ersten Sonne'
REGION_KHOM = 'Khom'
REGION_MERIDIANA = 'Echsensümpfe, Meridiana'
REGION_SOUTHERN_SEA = 'Altoum, Gewürzinseln, Südmeer'
REGIONS_DESERT = [REGION_KHOM]
REGIONS = [REGION_ICE, REGION_NE_HEIGHTS, REGION_HIGH_NORTH, 
           REGION_TUNDRA_TAIGA, REGION_BORNLAND_THORWAL, 
           REGION_QUARRELING_KINGDOMS, REGION_CENTRAL_MIDDLEREALM, 
           REGION_NORTHERN_HORAS, REGION_RASCHTUL_HEIGHTS, 
           REGION_SOUTHERN_HORAS, REGION_KHOM, REGION_MERIDIANA, 
           REGION_SOUTHERN_SEA] 
## Seasons
SUMMER = 'Sommer'
AUTUMN = 'Herbst'
WINTER = 'Winter'
SPRING = 'Frühling'
SEASONS = [SUMMER, AUTUMN, WINTER, SPRING]
## Change flags
CHANGE_CLOUDINESS = 0
CHANGE_WIND = 1
CHANGE_TEMPERATURE = 2
CHANGE_PRECIPITATION = 3

## Mappings
cloud_strings = {
    CLOUDS_NONE: 'völlig wolkenlos',
    CLOUDS_SOME: 'einzelne Wolken',
    CLOUDS_MANY: 'bewölkt mit Wolkenlücken',
    CLOUDS_FULL: 'geschlossene Wolkendecke'
}
wind_strings = {
    WIND_NONE: 'windstill',
    WIND_SOFTER: 'leichter Wind',
    WIND_SOFT: 'sanfte Brise',
    WIND_MEDIUM: 'frische Brise',
    WIND_STRONG: 'steife Brise',
    WIND_STRONGER: 'starker Wind',
    WIND_STORM: 'Sturm'
}
precipitation_strings = {
    PRECIPITATION_NONE: 'kein Niederschlag',
    PRECIPITATION_LIGHT: 'leichter Niederschlag',
    PRECIPITATION_MEDIUM: 'ergiebiger Niederschlag',
    PRECIPITATION_STRONG: 'heftiger Niederschlag'
}

class DSA4Weather() :
    cloud_table_normal = {
        1: CLOUDS_NONE,
        2: CLOUDS_NONE,
        3: CLOUDS_NONE,
        4: CLOUDS_NONE,
        5: CLOUDS_SOME,
        6: CLOUDS_SOME,
        7: CLOUDS_SOME,
        8: CLOUDS_SOME,
        9: CLOUDS_SOME,
       10: CLOUDS_SOME,
       11: CLOUDS_MANY,
       12: CLOUDS_MANY,
       13: CLOUDS_MANY,
       14: CLOUDS_MANY,
       15: CLOUDS_MANY,
       16: CLOUDS_MANY,
       17: CLOUDS_FULL,
       18: CLOUDS_FULL,
       19: CLOUDS_FULL,
       20: CLOUDS_FULL
    }

    cloud_table_desert = {
        1: CLOUDS_NONE,
        2: CLOUDS_NONE,
        3: CLOUDS_NONE,
        4: CLOUDS_NONE,
        5: CLOUDS_SOME,
        6: CLOUDS_SOME,
        7: CLOUDS_SOME,
        8: CLOUDS_SOME,
        9: CLOUDS_SOME,
       10: CLOUDS_SOME,
       11: CLOUDS_NONE,
       12: CLOUDS_NONE,
       13: CLOUDS_NONE,
       14: CLOUDS_NONE,
       15: CLOUDS_NONE,
       16: CLOUDS_NONE,
       17: CLOUDS_SOME,
       18: CLOUDS_SOME,
       19: CLOUDS_MANY,
       20: CLOUDS_FULL
    }
        
    wind_table_normal = {
        1: WIND_NONE,
        2: WIND_NONE,
        3: WIND_NONE,
        4: WIND_NONE,
        5: WIND_SOFTER,
        6: WIND_SOFTER,
        7: WIND_SOFTER,
        8: WIND_SOFT,
        9: WIND_SOFT,
       10: WIND_SOFT,
       11: WIND_MEDIUM,
       12: WIND_MEDIUM,
       13: WIND_MEDIUM,
       14: WIND_STRONG,
       15: WIND_STRONG,
       16: WIND_STRONG,
       17: WIND_STRONGER,
       18: WIND_STRONGER,
       19: WIND_STRONGER,
       20: WIND_STORM
    }

    wind_table_autumn = {
        1: WIND_NONE,
        2: WIND_NONE,
        3: WIND_NONE,
        4: WIND_SOFTER,
        5: WIND_SOFTER,
        6: WIND_SOFT,
        7: WIND_SOFT,
        8: WIND_MEDIUM,
        9: WIND_MEDIUM,
       10: WIND_MEDIUM,
       11: WIND_STRONG,
       12: WIND_STRONG,
       13: WIND_STRONG,
       14: WIND_STRONG,
       15: WIND_STRONGER,
       16: WIND_STRONGER,
       17: WIND_STRONGER,
       18: WIND_STRONGER,
       19: WIND_STORM,
       20: WIND_STORM
    }

    # Temperatures for Autumn are equal to thos for Spring.
    temperature_table = {
        REGION_ICE :                    {SUMMER: -20, SPRING: -30, WINTER: -40},
        REGION_NE_HEIGHTS :             {SUMMER: -10, SPRING: -20, WINTER: -30},
        REGION_HIGH_NORTH :             {SUMMER:   0, SPRING: -10, WINTER: -20},
        REGION_TUNDRA_TAIGA :           {SUMMER:   5, SPRING:   0, WINTER:  -5},
        REGION_BORNLAND_THORWAL :       {SUMMER:  10, SPRING:   3, WINTER:  -5},
        REGION_QUARRELING_KINGDOMS :    {SUMMER:  10, SPRING:   5, WINTER:   0},
        REGION_CENTRAL_MIDDLEREALM :    {SUMMER:  15, SPRING:  10, WINTER:   5},
        REGION_NORTHERN_HORAS :         {SUMMER:  20, SPRING:  15, WINTER:  10},
        REGION_RASCHTUL_HEIGHTS :       {SUMMER:   5, SPRING:   0, WINTER: -10},
        REGION_SOUTHERN_HORAS :         {SUMMER:  25, SPRING:  20, WINTER:  15},
        REGION_KHOM :                   {SUMMER:  40, SPRING:  35, WINTER:  30},
        REGION_MERIDIANA :              {SUMMER:  30, SPRING:  25, WINTER:  20},
        REGION_SOUTHERN_SEA :           {SUMMER:  35, SPRING:  30, WINTER:  25}
    }

    # Temperature mod for night is this mod times -1
    temperature_mod_cloudiness = {
        CLOUDS_NONE : 10,
        CLOUDS_SOME : 5,
        CLOUDS_MANY : 0,
        CLOUDS_FULL : -5
    }

    temperature_mod_wind = {
        WIND_NONE : 4,
        WIND_SOFTER : 2,
        WIND_SOFT : 0,
        WIND_MEDIUM : 0,
        WIND_STRONG : -2,
        WIND_STRONGER : -4,
        WIND_STORM : -6
    }

    # For a 1d20 below this value (including), we get precipitation
    precipitation_probability = {
        CLOUDS_NONE : 0,
        CLOUDS_SOME : 1,
        CLOUDS_MANY : 4,
        CLOUDS_FULL : 10
    }

    # Give upper ends of intervals (including) for the three types of 
    # precipitation:
    # LIGHT, MEDIUM, STRONG
    precipitation_type_table = {
        WIND_NONE : [12, 19, 20],
        WIND_SOFTER : [9, 18, 20],
        WIND_SOFT : [7, 17, 20],
        WIND_MEDIUM : [5, 16, 20],
        WIND_STRONG : [3, 15, 20],
        WIND_STRONGER : [2, 13, 20],
        WIND_STORM : [1, 10, 20]
    }

    change_table_summer_winter = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
       10: [CHANGE_WIND],
       11: [CHANGE_TEMPERATURE],
       12: [CHANGE_PRECIPITATION],
       13: [CHANGE_CLOUDINESS, CHANGE_PRECIPITATION],
       14: [CHANGE_WIND, CHANGE_TEMPERATURE],
       15: [CHANGE_WIND, CHANGE_PRECIPITATION],
       16: [CHANGE_PRECIPITATION, CHANGE_TEMPERATURE],
       17: [CHANGE_WIND, CHANGE_TEMPERATURE, CHANGE_PRECIPITATION],
       18: [CHANGE_CLOUDINESS, CHANGE_TEMPERATURE, CHANGE_PRECIPITATION],
       19: [CHANGE_CLOUDINESS, CHANGE_WIND, CHANGE_PRECIPITATION],
       20: [CHANGE_CLOUDINESS, CHANGE_WIND, CHANGE_TEMPERATURE, CHANGE_PRECIPITATION]
    }

    change_table_autumn_spring = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [CHANGE_WIND],
        6: [CHANGE_TEMPERATURE],
        7: [CHANGE_PRECIPITATION],
        8: [CHANGE_CLOUDINESS, CHANGE_PRECIPITATION],
        9: [CHANGE_CLOUDINESS, CHANGE_PRECIPITATION],
       10: [CHANGE_WIND, CHANGE_TEMPERATURE],
       11: [CHANGE_WIND, CHANGE_TEMPERATURE],
       12: [CHANGE_WIND, CHANGE_PRECIPITATION],
       13: [CHANGE_WIND, CHANGE_PRECIPITATION],
       14: [CHANGE_PRECIPITATION, CHANGE_TEMPERATURE],
       15: [CHANGE_PRECIPITATION, CHANGE_TEMPERATURE],
       16: [CHANGE_WIND, CHANGE_TEMPERATURE, CHANGE_PRECIPITATION],
       17: [CHANGE_CLOUDINESS, CHANGE_TEMPERATURE, CHANGE_PRECIPITATION],
       18: [CHANGE_CLOUDINESS, CHANGE_WIND, CHANGE_PRECIPITATION],
       19: [CHANGE_CLOUDINESS, CHANGE_WIND, CHANGE_TEMPERATURE, CHANGE_PRECIPITATION],
       20: [CHANGE_CLOUDINESS, CHANGE_WIND, CHANGE_TEMPERATURE, CHANGE_PRECIPITATION]
    }

    use_original_night_temperature = False

    def __init__(self, season=SUMMER, region=REGION_CENTRAL_MIDDLEREALM, 
                 daytime=True) :
        # Skip the `setter` methods in order to prevent execution of 
        # `roll_new_weather`.
        self.season = season
        self.region = region
        self.daytime = daytime
        # Initialize a weather
        self.roll_new_weather()

    def d20(self) :
        """ Return the result of a 1d20. """
        return randint(1, 20)

    def set_season(self, season):
        self.season = season
        self.roll_new_weather()

    def set_region(self, region):
        self.region = region
        self.roll_new_weather()

    def roll_new_weather(self) :
        """ Create a completely new weather, independent of the possibly 
        existing current weather conditions, only based on region and season.

        Requires `region`, `season`
        Sets `cloudiness`, `wind`, `temperature`, `precipitation`
        """
        ## Step 1: determine cloudiness
        self.roll_cloudiness()
        ## Step 2: determine wind
        self.roll_wind()
        ## Step 3: determine temperature
        self.determine_temperature()
        ## Step 4: check for precipitation (yes/no) and #Step 5 decide on the 
        ## precipitation type.
        self.roll_precipitation()

    def roll_next_weather(self) :
        """ Create a weather pattern for the next day, based on the current 
        weather pattern, region and season.

        Requires `cloudiness`, `wind`, `temperature`, `precipitation`
        Sets `cloudiness`, `wind`, `temperature`, `precipitation`
        """
        ## Determine what needs to be changed
        if self.season in [SUMMER, WINTER] :
            change_table = self.change_table_summer_winter
        elif self.season in [AUTUMN, SPRING] :
            change_table = self.change_table_autumn_spring
        changes = change_table[self.d20()]

        ## Change what needs changing
        for change in changes :
            if change == CHANGE_CLOUDINESS :
                self.roll_cloudiness()
            elif change == CHANGE_WIND :
                self.roll_wind()
            elif change == CHANGE_TEMPERATURE :
                self.determine_temperature()
            elif change == CHANGE_PRECIPITATION :
                self.roll_precipitation()

    def roll_cloudiness(self) :
        """ Determine the cloudiness depending on the region.

        Requires `region`
        Sets `cloudiness`
        """
        if self.region in REGIONS_DESERT :
            cloud_table = self.cloud_table_desert
        else :
            cloud_table = self.cloud_table_normal
        self.cloudiness = cloud_table[self.d20()]

    def roll_wind(self) :
        """ Determine the strength of winds depending of the season.

        Requires `season`
        Sets `wind`
        """
        if self.season == AUTUMN :
            wind_table = self.wind_table_autumn
        else :
            wind_table = self.wind_table_normal
        self.wind = wind_table[self.d20()]

    def determine_temperature(self) :
        """ Determine the temperature that follows from the region, wind and 
        cloudiness. 

        Requires `region`, `wind`, `cloudiness`
        Sets `temperature`
        """
        ## Step 3.1: Base temperature based on region and season
        if self.season == AUTUMN :
            season = SPRING
        else :
            season = self.season
        self.temperature = self.temperature_table[self.region][season]
        if not self.use_original_night_temperature:
            self.temperature += 5
        print("*** ***")
        print(f"Day 0: {self.temperature}")
        # :NOTE: The original formulation for night temperatures just seems 
        # way off.
        # Use a milder version instead.
        if self.use_original_night_temperature:
            self.night_temperature = self.temperature - (self.d20() + 5) 
        else:
            self.night_temperature = self.temperature - (self.d20()//4 + 2) 
        print(f"Night 0: {self.night_temperature}")

        ## Step 3.2: add temperature modifiers
        print(f"[D]Cloudiness: {self.cloudiness}")
        cloud_mod = self.temperature_mod_cloudiness[self.cloudiness]
        if not self.use_original_night_temperature:
            cloud_mod //= 2
        print(f"[D]Cloud mod: {cloud_mod}")
        self.temperature += cloud_mod
        print(f"Day cloud: {self.temperature}")
        self.night_temperature -= cloud_mod
        # Min temperature must not grow larger than max temperature
        if self.night_temperature >= self.temperature - 1:
            self.night_temperature = self.temperature - 1
        print(f"Night cloud: {self.night_temperature}")

        wind_mod = self.temperature_mod_wind[self.wind]
        self.temperature += wind_mod
        print(f"[D]Wind: {self.wind}")
        print(f"Day wind: {self.temperature}")
        self.night_temperature += wind_mod
        print(f"Night wind: {self.night_temperature}")

        # Random modifier
#        self.temperature += randint(-2, 2)

    def roll_precipitation(self) :
        """ Determine type of precipitation depending on wind strength. 

        Requires `wind`
        Sets `precipitation`
        """
        precipitates = \
                self.d20() <= self.precipitation_probability[self.cloudiness]

        if not precipitates :
            self.precipitation = PRECIPITATION_NONE
            return
        precipitation_list = self.precipitation_type_table[self.wind]
        rand = self.d20()
        if rand <= precipitation_list[0] :
            self.precipitation = PRECIPITATION_LIGHT
        elif rand > precipitation_list[0] and rand <= precipitation_list[1] :
            self.precipitation = PRECIPITATION_MEDIUM
        elif rand > precipitation_list[1] :
            self.precipitation = PRECIPITATION_STRONG

    def print_weather(self) :
        print(f"Daily average T: {self.temperature} C")
        print(f"Nightly minimum T: {self.night_temperature} C")
        print(wind_strings[self.wind])
        print(cloud_strings[self.cloudiness])
        print(precipitation_strings[self.precipitation])

    def get_weather_string(self) :
        """ Get the current weather in a human-readable format. """
        res = f'Today\' weather in {self.region} in {self.season}\n\n'
        res += f'{self.temperature}°C\n'
        res += f'{cloud_strings[self.cloudiness]}\n'
        res += f'{wind_strings[self.wind]}\n'
        res += f'{precipitation_strings[self.precipitation]}\n'
        return res

if __name__ == "__main__" :
    W = DSA4Weather(region=REGION_BORNLAND_THORWAL, season=AUTUMN)
#    W = DSA4Weather(region=REGION_KHOM, season=AUTUMN)
    print(W.region, W.season)
    data = []
    for i in range(30) :
        W.roll_next_weather()
        print(80*"=")
        W.print_weather()
        data.append([W.temperature, W.night_temperature, W.cloudiness, 
                     W.wind, W.precipitation])

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.gridspec import GridSpec

    data = np.array(data)
    x = np.arange(len(data))
    temp = data[:,0]
    night_temp = data[:,1]

    fig = plt.figure(layout="constrained")
    gs = GridSpec(nrows=2, ncols=2, figure=fig)

    ax_temp = fig.add_subplot(gs[0,0])
    ax_temp.plot(x, temp, 'r-', label='Temp')
    ax_temp.plot(x, night_temp, 'r--', label='Night Temp')
    ax_temp.fill_between(x, temp, night_temp, color="red", alpha=0.5)

    ax_clouds = fig.add_subplot(gs[1, 0])
    ax_clouds.plot(data[:,2], 'k--', label='Clouds')

    ax_wind = fig.add_subplot(gs[0, 1])
    ax_wind.plot(data[:,3], 'g-', label='Wind')

    ax_pp = fig.add_subplot(gs[1, 1])
    ax_pp.plot(data[:,4], 'b-', label='Precipitation')

#    plt.legend()
    plt.show()
