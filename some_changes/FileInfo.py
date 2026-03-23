class FileInfo:
    """Класс с информацией о файле."""
    
    __format_of_file = '.txt'
    
    def __init__(self, filename: str = ''   ) -> None:
        """Конструктор класса. 
        
        Args: 
            filename: название файла.
        """
        
        self.__filename = filename
        
    def get_filename(self) -> str:
        """Геттер названия файла.
        
        Returns:
            __filename: название файла.
        """
        
        return self.__filename
    
    def set_filename(self, filename: str = '') -> None:
        """Сеттер названия файла.
        
        Args:
            filename: название файла.
        """
        
        self.__filename = filename
        
    def get_format_of_file(self) -> str:
        """Геттер формата файла.
        
        Returns:
            __format_of_file: формат файла.
        """
        
        return self.__format_of_file
    
    def set_format_of_file(self, format_of_file: str  = '') -> None:
        """Сеттер формата файла.
        
        Args:
            format_of_file: формат файла.
        """

        self.__format_of_file = format_of_file
