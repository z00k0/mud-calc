from kivy.uix.gridlayout import GridLayout
# from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from kivymd.app import MDApp
# from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem

from kivy.config import Config


Config.set('kivy', 'keyboard_mode', 'systemanddock')


class MudCalc(GridLayout):
    '''
    уравнение материального баланса для расчета плотности смеси:

    vol_mix * dens_mix = vol_1 * dens_1 + vol_2 * dens_2
    vol_mix = vol_1 + vol_2

    из этого выводится формула для вычисления количества утяжелителя:

    m_1 = dens_1 * (dens_mix - dens_2) / (dens_1 - dens_mix) * vol_2

    в данном случае:
    m_1, dens_1 - масса и плотность утяжелителя
    vol_2, dens_2 объем и плотность утяжеляемого раствора
    dens_mix - плотность смеси, т.е. необходимая плотность раствора
    '''

    dens_1 = StringProperty()

    def calculate(self):
        try:
            dens_1 = float(self.ids.dens_1.text)
        except Exception as e:
            dens_1 = 0
            print(e, 'at dens_1')

        try:
            vol_2 = float(self.ids.vol_2.text)
        except Exception as e:
            vol_2 = 0
            print(e)

        try:
            dens_2 = float(self.ids.dens_2.text)
        except Exception as e:
            dens_2 = 0
            print(e)

        try:
            dens_mix = float(self.ids.dens_mix.text)
        except Exception as e:
            dens_mix = 0
            print(e)

        try:
            m_1 = dens_1 * 1000 * (dens_mix - dens_2) / (dens_1 - dens_mix) * vol_2
        except Exception as e:
            m_1 = 0
            print(f'{e} at m_1')

        try:
            vol_mix = vol_2 + (m_1 / (dens_1 * 1000))
        except Exception as e:
            vol_mix = 0
            print(f'{e} at vol_mix')

        try:
            conc = m_1 / vol_mix
        except Exception as e:
            conc = 0
            print(f'{e} at conc')

        self.ids.m_1.text = str(round(m_1 / 1000, 3))
        self.ids.concentration.text = str(round(conc))
        self.ids.vol_mix.text = str(round(vol_mix, 1))

class ItemConfirm(OneLineIconListItem):
    divider = None
    dens_1 = StringProperty('')

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

    def set_weighting(self, text):
        dens = text.split()[0]
        MDApp.get_running_app().dens_1 = dens


class MudCalcApp(MDApp):
    dialog = None
    dens_1 = StringProperty('2.6')

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        return MudCalc()

    def choose_weighting_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title='Выберите утяжелитель',
                type='confirmation',
                items=[
                    ItemConfirm(text='2.6 г/см3 - Мел'),
                    ItemConfirm(text='4.2 г/см3 - Барит'),
                    ItemConfirm(text='5.3 г/см3 - Гематит')
                ]
            )
        self.dialog.open()

    def dialog_close(self, *args):
        self.dialog.dismiss()

    def dialog_save(self, value):
        print(f'{MDApp.get_running_app().dens_1=}')
        self.dialog.dismiss()


if __name__ == '__main__':
    MudCalcApp().run()
