import kivy
from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.config import Config

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')

class MudCalc(FloatLayout):
    '''
    уравнение материального баланса для расчета плотности смеси:

    vol_sm * dens_sm = vol_1 * dens_1 + vol_2 * dens_2
    vol_sm = vol_1 + vol_2

    из этого выводится формула для вычисления количества утяжелителя:

    m_1 = dens_1 * (dens_sm - dens_2) / (dens_1 - dens_sm) * vol_2

    в данном случае:
    m_1, dens_1 - масса и плотность утяжелителя
    vol_2, dens_2 объем и плотность утяжеляемого раствора
    dens_sm - плотность смеси, т.е. необходимая плотность раствора
    '''
    
    def calculate(self):
        dens_1 = float(self.ids.dens_1.text)
        vol_2 = float(self.ids.vol_2.text)
        dens_2 = float(self.ids.dens_2.text)
        dens_sm = float(self.ids.dens_sm.text)

        try:
            m_1 = dens_1 * 1000 * (dens_sm - dens_2) / (dens_1 - dens_sm) * vol_2
        except Exception as e:
            m_1 = 0
            print(e)
        
        try:
            vol_sm = vol_2 + (m_1 / (dens_1 * 1000))
        except Exception as e:
            vol_sm = 0
            print(e)

        try:
            conc = m_1 / vol_sm
        except Exception as e:
            conc = 0
            print(e)

        self.ids.m_1.text = str(round(m_1))
        self.ids.concentration.text = str(round(conc))
        self.ids.vol_sm.text = str(round(vol_sm, 1))
        


class MudCalcApp(App):
    
    def build(self):
        return MudCalc()

if __name__ == '__main__':
    MudCalcApp().run()