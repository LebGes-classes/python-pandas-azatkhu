from ExcelParser import ExcelParser
from MedicalDevicesStatus import MedicalDeviceStatus

import pandas as pd


class AnalyzeMedicalDiagnosticDevices:
    """Класс, анализирующий медицинские диагностические устройства и клиники."""
    
    def __init__(self, filename: str = '') -> None:
        """Конструктор класса.
        
        Args: 
            filename: Наименование файла.
        """
    
        self.__data = ExcelParser(filename)
        self.__time_now = pd.Timestamp.now()

    def get_dataframe(self) -> pd.DataFrame:
        """Геттер DataFrame. 
        
        Returns:
            __dataframe_medical_devices: DataFrame с медицинскими диагностическими устройствами и клиниками.
        """
        
        return self.__dataframe_medical_devices

    def get_dataframe_from_file(self) -> None:
        """Получение DataFrame из файла."""

        self.__dataframe_medical_devices = self.__data.open_file()
        self.__medical_devices_status = MedicalDeviceStatus(self.__dataframe_medical_devices)
    
    def dataframe_to_excel(self, new_data: pd.DataFrame = None, filename: str = '') -> None:
        """Запись DataFrame в Excel файл.
        
        Args:
            new_data: DataFrame, который нужно записать в Excel файл.
            filename: Наименования файла.
        """
        
        self.__data.create_file(new_data, f'{filename}.xlsx')

    def dataframes_to_excel(self, dataframes: list = [pd.DataFrame], filenames: list = [str]) -> None:
        """Запись нескольких DataFrame в один Excel файл с несколькими листами (страницами).
        
        Args:
            dataframes: Список с несколькими DataFrame.
            filenames: Список с наименованиями страниц для соответствующих DataFrame в создаваемом Excel файле.
        """
        
        self.__data.create_file_with_some_sheets(dataframes, filenames)            
    
    def filter_out_date(self, column: str = '') -> None:
        """Фильтрация дат в DataFrame.

        Args:
            column: Строка, которая показывает, какой столбец нужно фильтровать.
        """
        
        date_index = pd.to_datetime(self.__dataframe_medical_devices[column], format = 'mixed')
        self.__dataframe_medical_devices[column] = date_index

    def filtering_warranty_dates(self, filtering_type: int = 0) -> pd.DataFrame:
        """Фильтрация таблицы по дате окончания гарантии.

        Args:
            filtering_type: Целое число, показывающее, как надо фильтровать таблицу по датам окончания гарантии.

        Returns:
            df: Отфильтрованный DataFrame по указанному типу фильтрации. 
        """
        
        match filtering_type:
            case 1:
                df = self.__dataframe_medical_devices[
                    self.__dataframe_medical_devices['warranty_until'] > self.__time_now
                ]
            case 2:
                df = self.__dataframe_medical_devices[
                    self.__dataframe_medical_devices['warranty_until'] < self.__time_now
                ]
            case 3:
                df = self.__dataframe_medical_devices[
                    self.__dataframe_medical_devices['warranty_until'] == self.__time_now
                ]
            case 4:
                df = self.__dataframe_medical_devices.sort_values(by = 'warranty_until', ascending = False)
            case 5:
                df = self.__dataframe_medical_devices.sort_values(by = 'warranty_until')
            case _:
                print('Нет такого варианта.')

        return df
    
    def normalize_status_of_device(self) -> None:
        """Нормализация статуса медицинских устройств."""
        
        correct_status_dict = MedicalDeviceStatus(self.__dataframe_medical_devices).get_dict_with_correct_status()
        self.__dataframe_medical_devices['status'] = self.__dataframe_medical_devices['status'].replace(correct_status_dict)
        
    def sort_issues_reported(self) -> pd.DataFrame:
        """Сортировка по наибольшему числу зарегистрированных проблем в клиниках.

        Returns:
            __clinics_devices_problems: DataFrame, отсортированный по числу зарегистрированных проблем.
        """
        
        self.__clinics_devices_problems = self.__dataframe_medical_devices.groupby(by = ['clinic_name']).agg({'issues_reported_12mo': 'sum'})
        self.__clinics_devices_problems = self.__clinics_devices_problems.sort_values('issues_reported_12mo', ascending = False)
        
        return self.__clinics_devices_problems

    def show_clinics_with_problems(self, count_of_clinics: int = 0) -> pd.DataFrame:
        """Создание DataFrame, отсортированного по количеству проблем, который содержит число клиник, заданных пользователем.

        Args:
            count_of_clinics: Количество первых сверху клиник, которые должен содержать DataFrame. 

        Returns:
            clinics_with_problems: DataFrame, содержащий клиники и количество их проблем.
        """
        
        result = self.sort_issues_reported()
        result = result.reset_index()
        clinics_with_problems = result.head(count_of_clinics)
        
        return clinics_with_problems
    
    def last_calibration_future(self) -> pd.DataFrame:
        """Создание DataFrame с информацией об устройствах клиник, дата последней калибровки которых еще не наступила.

        Returns:
            __filter_data: DataFrame с информацией об устройствах клиник, дата последней калибровки которых еще не наступила.
        """
        
        self.__filter_data = self.__dataframe_medical_devices[
            (self.__dataframe_medical_devices['last_calibration_date'] > self.__time_now) &
            (self.__dataframe_medical_devices['last_calibration_date'] > self.__dataframe_medical_devices['install_date'])
        ]

        return self.__filter_data

    def last_calibration_past(self) -> pd.DataFrame:
        """Создание DataFrame с информацией об устройствах клиник, дата последней калибровки которых прошла.

        Returns:
            __filter_data: DataFrame с информацией об устройствах клиник, дата последней калибровки которых в прошлом.
        """
        
        self.__filter_data = self.__dataframe_medical_devices[
            (self.__dataframe_medical_devices['last_calibration_date'] < self.__time_now) &
            (self.__dataframe_medical_devices['last_calibration_date'] > self.__dataframe_medical_devices['install_date'])
        ]

        return self.__filter_data

    def last_calibration_incorrect(self) -> pd.DataFrame:
        """Создание DataFrame с информацией об устройствах клиник, дата последней калибровки которых ошибочна (до установки).

        Returns:
            __filter_data: DataFrame с информацией об устройствах клиник, дата последней калибровки которых еще ошибочна.
        """
        
        self.__filter_data = self.__dataframe_medical_devices[
            (self.__dataframe_medical_devices['last_calibration_date'] < self.__dataframe_medical_devices['install_date'])
        ]

        return self.__filter_data

    def create_pivot_table_with__device_issues(self) -> pd.DataFrame:
        """Создание сводной таблицы с зарегестрированными проблемами устройств в клиниках.

        Returns:
            issues_table: Сводная таблица с зарегестрированными проблемами устройств в клиниках. 
        """
        
        issues_data = self.sort_issues_reported()
        issues_table = issues_data.pivot_table(index = 'clinic_name', values = 'issues_reported_12mo', aggfunc = 'sum')
        
        return issues_table

    def create_pivot_table_with_calibration_dates(self) -> pd.DataFrame:
        """Создание сводной таблицы с датами послених калибровок устройств в клиниках.

        Returns:
            calibration_table: Сводная таблица с датами последних калибровокк устройств в клиниках.
        """
        
        calibration_data = self.last_calibration_future()
        calibration_table = calibration_data.pivot_table(index = 'clinic_name', values = 'last_calibration_date')
        
        return calibration_table
