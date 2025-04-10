class TimeAlreadyTakenException(Exception):
    @property
    def message(self):
        return {
                'title': 'Ошибка записи',
                'message': 'Время которые вы выбрали уже занято. Попробуйте выбрать другое время',
            }
