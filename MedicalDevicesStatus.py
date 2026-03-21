import pandas as pd


class MedicalDeviceStatus:
    """Класс с обработкой статусов медицинских диагностических устройств."""
    
    def __init__(self, data: pd.DataFrame = None) -> None:
        """Конструктор класса.

        Args:
            data: DataFrame, статусы которого надо обработать.
        """
        
        self.__data = data
        self.__correct_device_status = (
            'faulty',
            'maintenance_scheduled',
            'operational',
            'planned_installation',
        )

    def find_incorrect_device_status(self) -> set:
        """Нахождение неправльных статусов медицинских диагностических устройств, которые нужно нормализовать.

        Returns:
            set_with_incorrect_status: Статусы медицинских диагностических устройств, которые надо нормализовать. 
        """
        
        set_of_status = set(self.__data['status'])
        set_with_incorrect_status = {x for x in set_of_status if x not in self.__correct_device_status}

        return set_with_incorrect_status

    def get_dict_with_correct_status(self) -> dict:
        """Словарь с исправленными статусами устройств для последующей нормализации.

        Returns:
            correct_status_dict: Словарь с правильными статусами медицинских диагностических устройств.
        """
        correct_status_dict = {
            'Operational': self.__correct_device_status[2],
            'service_scheduled': self.__correct_device_status[1],
            'scheduled_install': self.__correct_device_status[3],
            'planned': self.__correct_device_status[3],
            'broken': self.__correct_device_status[0],
            'OK': self.__correct_device_status[2],
            'needs_repair': self.__correct_device_status[0],
            'to_install': self.__correct_device_status[3],
            'working': self.__correct_device_status[2],
            'maint_sched': self.__correct_device_status[1],
            'op': self.__correct_device_status[2],
            'operational ': self.__correct_device_status[2],
            'maintenance': self.__correct_device_status[1],
            'error': self.__correct_device_status[0],
            'FAULTY': self.__correct_device_status[0],
        }

        return correct_status_dict
