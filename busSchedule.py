"""
Esse arquivo contém os horários de funcionamento dos ônibus da Unicamp e suas rotas.
"""
from timeUtils import strToDatetime

global BUS_FULL_SCHEDULE_PHOTO
BUS_FULL_SCHEDULE_PHOTO = 'https://i.pinimg.com/originals/cf/ad/04/cfad0446abaf264bf013c3f391276aac.jpg'

# Horários dos ônibus

# Dia útil
weekdayBusDepartureSchedule = [
    '06:30', '06:45', '06:50', '07:00', '07:10', '07:15', '07:20', '07:25', '07:35', '07:40', '07:45', '08:00', '08:10', '08:20',
    '08:30', '08:40', '08:50', '09:00', '09:10', '09:20', '09:30', '09:40', '09:45', '10:05', '10:15', '10:30','10:45', '11:00',
    '11:20', '11:30', '11:45', '12:00', '12:15', '12:20', '12:35', '12:45', '13:00', '13:05', '13:20', '13:30', '13:45', '14:00',
    '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:00', '17:30', '17:45',
    '18:00', '18:10','18:20', '18:25', '18:30', '18:40', '18:55', '19:00', '19:15', '19:25', '19:35', '19:50', '19:55', '20:10',
    '20:30', '20:45'
]

weekdayBusReturnSchedule = [
    '07:20', '07:40', '08:00', '08:25', '08:45', '09:00', '09:30', '09:50', '10:00', '10:15', '10:40', '11:05', '11:15', '11:30', '11:45', '11:55', '12:00',
    '12:20', '12:30', '12:45', '12:50', '13:00', '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45',
    '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:15', '17:30', '17:40', '17:45',
    '17:50', '18:00', '18:15', '18:20', '18:30', '18:40', '18:50', '19:05', '19:10', '19:25', '19:35', '19:45',
    '20:05', '20:20', '20:40', '20:50', '21:00', '21:25', '21:35', '21:55', '22:00', '22:10', '22:20', '22:30',
    '22:35', '22:45', '23:05', '23:15', '23:25', '23:35', '23:45'
]

# Dia não-útil
nonWorkingDayBusDepartureSchedule = [
    '07:10', '07:20', '07:30', '07:40', '07:50', '08:00', '08:10', '08:20', '11:00', '11:10', '11:20',
    '11:30', '11:40', '11:50', '12:00', '12:10', '12:20', '12:30', '12:40', '12:50', '13:00', '13:10', 
    '13:20', '13:30', '13:40', '13:50', '17:30', '17:40', '17:50', '18:00', '18:10', '18:20', '18:30',
    '18:40', '18:50'
]

nonWorkingDayBusReturnSchedule = [
    '07:20', '07:30', '07:40', '07:50', '08:00', '08:10', '08:20', '08:30', '11:10', '11:20', '11:30', '11:40', 
    '11:50', '12:00', '12:10', '12:20', '12:30', '12:40', '12:50', '13:00', '13:10', '13:20', '13:30', '13:40',
    '13:50', '14:00', '17:40', '17:50', '18:00', '18:10', '18:20', '18:30', '18:40', '18:50', '19:00'
]

# Conversão dos horários em datetime
weekdayBusDepartureSchedule = list(map(strToDatetime, weekdayBusDepartureSchedule))
weekdayBusReturnSchedule = list(map(strToDatetime, weekdayBusReturnSchedule))
nonWorkingDayBusDepartureSchedule = list(map(strToDatetime, nonWorkingDayBusDepartureSchedule))
nonWorkingDayBusReturnSchedule = list(map(strToDatetime, nonWorkingDayBusReturnSchedule))

dayTypes = {
    "working day": (weekdayBusDepartureSchedule, weekdayBusReturnSchedule),
    "non working day": (nonWorkingDayBusDepartureSchedule, nonWorkingDayBusReturnSchedule)
}