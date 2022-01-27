from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout

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

    def calculate(self):
        try:
            dens_1 = float(self.ids.dens_1.text)
        except Exception as e:
            dens_1 = 0
            print(e)

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
            print(e)

        try:
            vol_mix = vol_2 + (m_1 / (dens_1 * 1000))
        except Exception as e:
            vol_mix = 0
            print(e)

        try:
            conc = m_1 / vol_mix
        except Exception as e:
            conc = 0
            print(e)

        self.ids.m_1.text = str(round(m_1))
        self.ids.concentration.text = str(round(conc))
        self.ids.vol_mix.text = str(round(vol_mix, 1))


class MudCalcApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        return MudCalc()

if __name__ == '__main__':
    MudCalcApp().run()
