from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.datatables import MDDataTable
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.boxofficemojo.com/year/world/2022')
soup = BeautifulSoup(page.content, 'html.parser')

class MyLayout(FloatLayout):

	table_exists = False

	def show_table(self):
		selected = []
		try:
			if self.table_exists == True:
				self.remove_widget(self.data_table)
			self.ids.error.text = ""
			table = soup.find(id='table')
			inds = self.ids.list_inds.text.split('-')
			n1, n2 = int(inds[0]), int(inds[1])
			movies = table.find_all('td', class_="a-text-left")
			revenues = table.find_all('td', class_="a-text-right")
			for i in range(n1-1,n2):
				selected.append((str(i+1), movies[i].text, revenues[6*i+1].text))

			self.data_table = MDDataTable(
				size_hint=(0.8,0.75),
				pos_hint={'center_x': 0.5, 'center_y': 0.45},
    	        use_pagination=True,
				column_data = [
					("Rank", dp(45)),
					("Movie Name", dp(45)),
					("Revenue", dp(45)),
				],
				row_data = selected,
			)
			self.add_widget(self.data_table)
			self.table_exists = True

		except Exception:
			self.ids.error.text = "Error!"


class MainApp(MDApp):
	def build(self):
		return MyLayout()

app = MainApp()
app.run()
