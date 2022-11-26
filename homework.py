from dataclasses import dataclass
from typing import Type
from typing import Dict


@dataclass
class InfoMessage:
    """
    Информационное сообщение о тренировке.
    Содержит: training_type - имя класса тренировки;
              duration - длительность тренировки в часах;
              distance - дистанция в км, которую преодалел
                         пользователь за время тренировки;
              speed    - средняя скорость, с которой двигался пользователь;
              calories - количество килокалорий, которое израсходовал
                         пользователь за время тренировки.
    """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вернуть результат тренировки"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """
        Атрибуты:
        action   - количество совершённых действий
                (число шагов при ходьбе и беге либо гребков — при плавании);
        duration - длительность тренировки в часах
        weight   - вес спортсмена в кг;
        """
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = self.__class__.__name__

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        """
        Атрибуты:
        action   - количество совершённых действий
                (число шагов при ходьбе и беге либо гребков — при плавании);
        duration - длительность тренировки в ч;
        weight   - вес спортсмена в кг;
        """
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """
        Атрибуты:
        action   - количество совершённых действий
                   (число шагов при ходьбе и беге либо гребков — при плавании);
        duration - длительность тренировки в ч;
        weight   - вес спортсмена в кг;
        height   - рост спротсмена в см.
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM: float = 1.1
    SWIM2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        """
        Атрибуты:
        action   - количество совершённых действий
                   (число шагов при ходьбе и беге либо гребков — при плавании);
        duration - длительность тренировки в ч;
        weight   - вес спортсмена в кг;
        height   - рост спротсмена в см;
        length_pool - длина бассейна в м;
        count_pool - сколько раз пользователь
                     переплыл бассейн.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.SWIM)
                * self.SWIM2
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_training: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking}
    if workout_type not in type_of_training:
        raise TypeError(f'UnknownTypeOfWorkout: {workout_type}, '
                        'an unknown type of training was '
                        'transferred to the dictionary.')
    return type_of_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
