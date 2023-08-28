menu = [{'title': 'Главная', 'url_name': 'carwash:home'},
        {'title': 'Записаться', 'url_name': 'carwash:registration'},
        {'title': 'Услуги и цены', 'anchor': '#services_price'},
        {'title': 'Контакты и адрес', 'anchor': '#footer'},
        ]

class Common:
    title = None

    @classmethod
    def menu(cls, *args):
        user_menu = menu.copy()

        if args:
            return [user_menu[i] for i in args]
        else:
            return user_menu

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(Common, self).get_context_data(**kwargs)
    #
    #     context['menu'] = [user_menu[0]]
    #     context['title'] = self.title
    #     context['menu'] = user_menu
    #
    #     return context

