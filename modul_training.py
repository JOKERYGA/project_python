from __future__ import annotations
from typing import Type
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки {self.training_type}; '
                    'Длительность: {self.duration:.3f} ч.; '
                    'Дистанция: {self.distance:.3f} км; '
                    'Ср. скорость: {self.speed:.3f} км/ч; '
                    'Потрачено ккал: {self.calories:.3f}.')

    def get_message(self):
        """Выводим информацию о тренировке."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    H_TO_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_speed = self.get_distance() / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.__class__.__name__, self.duration,
                            self.get_distance(), self.get_mean_speed(),
                            self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.M_IN_KM * self.duration
                          * self.H_TO_M)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_WEIGHT_MULTIPLIER2 = 0.029
    TRN_TO_MS = round(1000 / 3600, 3)
    MTR = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_cal_walk = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                          + ((self.get_mean_speed() * self.TRN_TO_MS) ** 2)
                          / (self.height / self.MTR)
                          * (self.CALORIES_WEIGHT_MULTIPLIER2 * self.weight))
                          * (self.duration * self.H_TO_M))
        return spent_cal_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    const_cal = 1.1
    const_cal2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        spent_callories_pool = ((self.get_mean_speed() + self.const_cal)
                                * self.const_cal2 * self.weight
                                * self.duration)
        return spent_callories_pool

    def get_mean_speed(self) -> float:
        speed_pool = (self.lenght_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return speed_pool


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    activites: dict[str, Type[Training]] = {'SWM': Swimming,
                                            'RUN': Running,
                                            'WLK': SportsWalking}
    if workout_type not in activites:
        raise ValueError('Передан неверный идентификатор тренировки.')
    type_values = activites[workout_type](*data)
    return type_values


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.message)


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
