M_IN_KM: int = 1000
H_IN_MIN: int = 60

class InfoMessage:
    """Информационное сообщение о тренировке."""
    pass

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duratuon = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

        def get_message(self) -> str:
            message =  (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
            return message

class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        dist = self.action * self.LEN_STEP / M_IN_KM   #в киломертрах
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration     # км/ч
        return mean_speed
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        ...

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_info = InfoMessage(workout_type,
                         self.duration,
                         self.get_distance(),
                         self.get_mean_speed(),
                         self.get_spent_calories()
                         )
        return training_info
    

class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / M_IN_KM * (self.duration*H_IN_MIN))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    K_1: float = 0.035
    K_2: float = 0.029
    K_KMCH_IN_MSEC: float = 3.6
    K_SM_IN_M: int = 100


    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""

        spent_calories = ((self.K_1 * self.weight +((self.get_mean_speed()/self.K_KMCH_IN_MSEC)**2) / (self.height/self.K_SM_IN_M))* self.K_2 * self.weight) * (self.duration*H_IN_MIN)
        return spent_calories

class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    K_11: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""

        mean_speed = self.length_pool * self.count_pool / M_IN_KM / self.duration     # км/ч
        return mean_speed
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""

        spent_calories = (self.get_mean_speed() + self.K_11) * 2 * self.weight * self.duration
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_type = {'SWM':Swimming, 'RUN':Running, 'WLK':SportsWalking}

    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
         return Running(*data)
    elif workout_type == 'WLK':
         return SportsWalking(*data)
    return Training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print (message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

