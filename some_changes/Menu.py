from AnalyzeMedicalDiagnosticDevices import AnalyzeMedicalDiagnosticDevices
from ExcelParser import ExcelParser


class Menu:
    """Класс Меню."""
    
    def __init__(self) -> None:
        """Конструктор класса."""
        
        self.__analysing_devices = AnalyzeMedicalDiagnosticDevices('medical_diagnostic_devices_10000')
    
    def choose_filter_warranty_option(self) -> None:
        """Вывод вариантов для выбора типа фильтрации даты последней гарантии медицинских устройств."""
        
        print('Как нужно отфильтровать дату гарантии?')
        print('1 - гарантия не истекла.')
        print('2 - гарантия истекла.')
        print('3 - сегодня последний гарантийный день.')
        print('4 - сортировка гарантии по возрастанию.')
        print('5 - сортировка гарантии по убыванию.')
        
    def choose_calibration_time(self) -> None:
        """Вывод вариантов для выбора временного отрезка последней калибровки медицинского устройства."""
        
        print('Какие даты калибровки хотите увидеть?')
        print('1 - дата калибровки еще не настала.')
        print('2 - дата последней калибровки была в прошлом.')
        print('3 - дата калибровки ошибочная (до даты установки оборудования).')
        
    def process_of_analysing(self) -> None:
        """Процесс анализа, включающий все функции класса анализа медицинских устройств."""
        
        self.__analysing_devices.get_dataframe_from_file()
        input('Файл прочитан.')

        self.__analysing_devices.filter_out_date('warranty_until')
        self.__analysing_devices.filter_out_date('install_date')
        self.__analysing_devices.filter_out_date('last_calibration_date')
        self.__analysing_devices.filter_out_date('last_service_date')   
        input('Даты приведены к одному виду.')
        
        self.__analysing_devices.normalize_status_of_device()
        input('Нормализованы статусы устройств.')
        
        self.choose_filter_warranty_option()
        choice_warranty_until_filter = int(input())
        df1 = self.__analysing_devices.filtering_warranty_dates(choice_warranty_until_filter)
        input('Даты окончания гарантии отфильтрованы, создан файл xlsx.')
        
        self.__analysing_devices.sort_issues_reported()
        input('Отсортированы проблемы устройств по клиникам.')
        count_of_clinics = int(input('Введите количество клиник, для которых хотите увидеть количество проблем.'))
        df2 = self.__analysing_devices.show_clinics_with_problems(count_of_clinics)
        input('Создан новый файл.')
        
        self.choose_calibration_time()
        choose_last_calibration_time = int(input())
        match choose_last_calibration_time:
            case 1:
                data_calibration_date_in_future = self.__analysing_devices.last_calibration_future()
                df3 = data_calibration_date_in_future
            case 2:
                data_calibration_date_in_past = self.__analysing_devices.last_calibration_past()
                df3 = data_calibration_date_in_past
            case 3:
                data_calibration_date_is_incorrect = self.__analysing_devices.last_calibration_incorrect()
                df3 = data_calibration_date_is_incorrect
            case _:
                print('Такого варианта нет.')
                
        print('Сделана страница с датами калибровок.')
        df4 = self.__analysing_devices.create_pivot_table()

        self.__analysing_devices.dataframes_to_excel([df1, df2, df3, df4], ['filtered_warranty', 'sorted_devices_issues', 'calibration_dates', 'table'])

        