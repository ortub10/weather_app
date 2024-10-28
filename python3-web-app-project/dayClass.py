class Day:

    def __init__(self, date, day_temperature, night_temperature, humidity):
        self.__date = date
        self.__day_temperature = day_temperature
        self.__night_temperature = night_temperature
        self.__humidity = humidity

    def get_date(self):
        return self.__date

    def get_day_temperature(self):
        return self.__day_temperature

    def get_night_temperature(self):
        return self.__night_temperature

    def get_humidity(self):
        return self.__humidity
