#! /usr/bin/env python3

import sys
import pprint
import pygame
from   pygame.locals import *
import math
import csv
import random
from   enum import Enum
import time
pp = pprint.PrettyPrinter(indent = 4)

card_size_x = 120
card_size_y = 160
t_mergin    = 20
l_mergin    = 20
x_mergin    = 10
y_mergin    = 10
x_full_size = 6
y_full_size = 5
textsize    = 15

class card_face(Enum):
	flont    = 0
	back     = 1
	invalid  = 2

Parlwhite = (253, 245, 230)
Brown     = (139,  69,  19)
Green     = (143, 188, 143)
Yellow    = (195, 216,  37)
Red       = (200,  85,  84)

card_face_color_dict                    = {}
card_face_color_dict[card_face.flont]   = Parlwhite
card_face_color_dict[card_face.back]    = Brown
card_face_color_dict[card_face.invalid] = Green

player_points = 0

shokubaiflag = False
hitflag      = False
nukiuchiflag = False


class card_propaty:
	def __init__(self, screen, x_pos_index, y_pos_index, size_x, size_y, face = card_face.back, element = None, cost = None, isSelected = False, element_name_str = None):
		self.screen      = screen
		self.x_pos_index = x_pos_index
		self.y_pos_index = y_pos_index
		self.size_x      = size_x
		self.size_y      = size_y
		self.face        = face
		self.element     = element
		self.cost        = cost
		self.isSelected  = isSelected
		self.element_name_str = element_name_str
		self.used        = False

	def draw_card(self):
		if self.face == card_face.invalid:
			return 0
		tmp_card_position = card_position(self.x_pos_index, self.y_pos_index)
		if   self.face == card_face.back:
			pygame.draw.rect(self.screen, card_face_color_dict[card_face.back], tmp_card_position)
		elif self.face == card_face.flont:
			if self.isSelected == True:
				pygame.draw.rect(self.screen, Yellow,                                tmp_card_position)
			else:
				pygame.draw.rect(self.screen, card_face_color_dict[card_face.flont], tmp_card_position)
			if self.element != None:
				self.screen.blit(self.element, tmp_card_position)
		elif self.face == card_face.invalid:
			pygame.draw.rect(self.screen, card_face_color_dict[card_face.invalid], tmp_card_position)


	def print_all_propaties(self):
		pp.pprint(self.__dict__.items())

class event_card_propaty:
	def __init__(self, screen, x_pos_index, y_pos_index, size_x, size_y, face = card_face.flont, element = None, cost = None, isSelected = False, element_name_str = None):
		self.screen      = screen
		self.x_pos_index = x_pos_index
		self.y_pos_index = y_pos_index
		self.size_x      = size_x
		self.size_y      = size_y
		self.face        = face
		self.element     = element
		self.cost        = cost
		self.isSelected  = isSelected
		self.element_name_str = element_name_str
		self.used        = False

	def draw_card(self):
		if self.face == card_face.invalid:
			return 0
		tmp_card_position = card_position(self.x_pos_index, self.y_pos_index)
		if   self.face == card_face.back:
			pygame.draw.rect(self.screen, card_face_color_dict[card_face.back], tmp_card_position)
		elif self.face == card_face.flont:
			if self.isSelected == True:
				pygame.draw.rect(self.screen, Yellow,                                tmp_card_position)
			else:
				pygame.draw.rect(self.screen, card_face_color_dict[card_face.flont], tmp_card_position)
			if self.element != None:
				self.screen.blit(self.element, tmp_card_position)
		elif self.face == card_face.invalid:
			pygame.draw.rect(self.screen, card_face_color_dict[card_face.invalid], tmp_card_position)



	def print_all_propaties(self):
		pp.pprint(self.__dict__.items())

class deck:
	def __init__(self, screen, x_pos_index, y_pos_index, size_x, size_y, rest = -1):
		self.screen      = screen
		self.x_pos_index = x_pos_index
		self.y_pos_index = y_pos_index
		self.size_x      = size_x
		self.size_y      = size_y
		self.rest        = rest

	def draw_card_with_rest(self):
		if self.rest != 0:
			pygame.draw.rect(self.screen, card_face_color_dict[card_face.back], card_position(self.x_pos_index, self.y_pos_index))
		reststring = pygame.font.SysFont("ヒラキノ角コシックw4ttc", 60).render(str(self.rest), True, (0,0,0))
		self.screen.blit(reststring, card_position(self.x_pos_index, self.y_pos_index, 20, 50))

class fusion_button:
	def __init__(self, screen, x_axis, y_axis, x_width, y_height, fusion_dict, textsize = 30, button_on = False, selected_cards = None):
		self.screen = screen
		self.x_axis = x_axis
		self.y_axis = y_axis
		self.x_width  = x_width
		self.y_height = y_height
		self.fusion_dict = fusion_dict
		self.button_on      = button_on
		self.selected_cards = selected_cards
		self.font    = pygame.font.SysFont("ヒラキノ角コシックw4ttc", textsize)
		self.message = self.font.render("合成", True, (0,0,0))
		self.image   = pygame.image.load("./image/合成ロゴ.gif")
	def draw(self):
		if self.button_on:
			pygame.draw.rect(self.screen, (Red),       (self.x_axis, self.y_axis, self.x_width, self.y_height / 2 - y_mergin))
			self.screen.blit(self.image,   (self.x_axis, self.y_axis))
		else:
			pygame.draw.rect(self.screen, (Parlwhite), (self.x_axis, self.y_axis, self.x_width, self.y_height / 2 - y_mergin))
			self.screen.blit(self.image,   (self.x_axis, self.y_axis))
	def is_pushed(self, x, y):
		if x > self.x_axis and y > self.y_axis and x < self.x_axis + self.x_width and y < self.y_axis + self.y_height:
			self.button_on = True
		else:
			self.button_on = False
	def fusion(self):
		global nukiuchiflag
		element_names  = list(map(lambda x:x.element_name_str, self.selected_cards))
		element_prices = list(map(lambda x:x.cost,             self.selected_cards))
		element_names_clean  = sorted([e for e in element_names  if e is not None])
		element_prices_clean = sorted([e for e in element_prices if e is not None])
		for itr in self.fusion_dict.keys():
			tmp_element_name_array = sorted(self.fusion_dict[itr])
			if tmp_element_name_array == element_names_clean:
				if type(element_prices_clean) is list:
					rewards = sum(element_prices_clean) + 2 * len(element_prices_clean) - 1
				else:
					rewards = element_prices_clean + 1
				global player_points
				global shokubaiflag
				global hitflag
				if shokubaiflag:
					rewards += 1
				if hitflag:
					rewards *= 2
				player_points += rewards
				pygame.draw.rect(self.screen, (Parlwhite), (self.x_axis, self.y_axis + card_size_y / 2, self.x_width, self.y_height / 2))
				message_draw(self.screen, "%sから%sを合成！"%("と".join(element_names_clean), itr), 15, self.x_axis, self.y_axis + card_size_y / 2 + y_mergin)
				message_draw(self.screen, "獲得：%3dポイント"%(rewards),                            15, self.x_axis, self.y_axis + card_size_y / 2 + y_mergin + 15)
				message_draw(self.screen, "合計：%3dポイント"%(player_points),                      15, self.x_axis, self.y_axis + card_size_y / 2 + y_mergin + 30)

				for card in self.selected_cards:
					card.isSelected = False
					card.face = card_face.back
					card.used = True

class turnend_button:
	def __init__(self, screen, x_axis, y_axis, x_width, y_height, button_on = False):
		self.screen    = screen
		self.x_axis    = x_axis
		self.y_axis    = y_axis
		self.x_width   = x_width
		self.y_height  = y_height
		self.button_on = button_on
		self.image     = pygame.image.load("./image/ターンエンド.gif")
		self.image_alt = pygame.image.load("./image/ターンエンド_薄.gif")
	def is_pushed(self, x, y):
		if x > self.x_axis and y > self.y_axis and x < self.x_axis + self.x_width and y < self.y_axis + self.y_height:
			self.button_on = True
		else:
			self.button_on = False
	def draw(self, flag):
		if flag:
			self.screen.blit(self.image, (self.x_axis, self.y_axis))
		else:
			self.screen.blit(self.image_alt, (self.x_axis, self.y_axis))

class swap_button:
	def __init__(self, screen, x_axis, y_axis, x_width, y_height, button_on = False):
		self.screen    = screen
		self.x_axis    = x_axis
		self.y_axis    = y_axis
		self.x_width   = x_width
		self.y_height  = y_height
		self.button_on = button_on
		self.image     = pygame.image.load("./image/回転.gif")
	def is_pushed(self, x, y):
		if x > self.x_axis and y > self.y_axis and x < self.x_axis + self.x_width and y < self.y_axis + self.y_height:
			self.button_on = True
		else:
			self.button_on = False
	def draw(self):
		self.screen.blit(self.image, (self.x_axis, self.y_axis))

def message_draw(screen, sentence, textsize, x_pos, y_pos, width = None, height = None):
	showpoint = pygame.font.SysFont("ヒラキノ角コシックw4ttc", textsize).render(sentence, True, (0, 0, 0))
	pygame.draw.rect(screen, (Parlwhite), (x_pos, y_pos, textsize * len(sentence), textsize + 1))
	if width is not None and height is not None:
		screen.blit(showpoint, (x_pos, y_pos, x_pos + width, y_pos + height))
	else:
		screen.blit(showpoint, (x_pos, y_pos))



def hand_out_cards(card_propaties, deck_array, card_render_dict):
	for itr in card_propaties:
		if itr.used:
			tmp_receiver = deck_array.pop()
			element_name, element_cost = tmp_receiver
			itr.element          = card_render_dict[element_name][1]
			itr.cost             = element_cost
			itr.isSelected       = False
			itr.element_name_str = element_name
			itr.used             = False

def card_position(x_index, y_index, x_offset = 0 , y_offset = 0):
	return ( \
		x_offset + l_mergin + (card_size_x + x_mergin) * x_index, \
		y_offset + t_mergin + (card_size_y + y_mergin) * y_index, \
		card_size_x, \
		card_size_y)

def mouse_pos_2_index(mouse_x, mouse_y):
	x_tmp = mouse_x - l_mergin
	y_tmp = mouse_y - t_mergin
	x_cnt = 0
	y_cnt = 0
	while x_tmp > card_size_x + x_mergin:
		x_tmp -= (card_size_x + x_mergin)
		x_cnt += 1
	while y_tmp > card_size_y + y_mergin:
		y_tmp -= (card_size_y + y_mergin)
		y_cnt += 1
	if x_tmp < card_size_x and \
	   y_tmp < card_size_y and \
	   x_cnt < x_full_size and \
	   y_cnt < y_full_size:
		return (x_cnt, y_cnt)
	else:
		return (-1, -1)
	#x_q, x_mod = divmod(mouse_x - l_mergin, card_size_x + x_mergin)
	#y_q, y_mod = divmod(mouse_y - t_mergin, card_size_y + y_mergin)
	#if x_mod < card_size_x and y_mod < card_size_y and x_mod < x_full_size and y_mod < y_full_size:
		#return (x_q, y_q)
	#else:
		#return (x_mod, y_mod)

def opponent_action():
	return True



def main():
	global player_points
	global shokubaiflag
	global hitflag
	global nukiuchiflag
	pygame.init()
	font4card_name   = pygame.font.SysFont("ヒラキノ角コシックw4ttc", textsize)
	card_render_dict = {}
	deck_rawdict     = {}
	with open('見やすい枚数表.txt') as f:
		reader = csv.reader(f, delimiter = '\t')
		header = next(reader)
		for row in reader:
			tmp_element_name  = str(row[0]).strip()
			tmp_element_cost  = int(row[1])
			tmp_element_count = int(row[2])
			card_render_dict[tmp_element_name] = [tmp_element_name, font4card_name.render(tmp_element_name, True, (0,0,0))]
			deck_rawdict[tmp_element_name]     = [tmp_element_cost, tmp_element_count]

	deck_array       = [] * 100
	extra_deck_array = [] * 100
	for elem in deck_rawdict.keys():
		for i in range(int(deck_rawdict[elem][1])):
			if int(deck_rawdict[elem][0]) > 0:
				deck_array.append((elem, deck_rawdict[elem][0]))#(str元素名, int コスト)
			else:
				extra_deck_array.append((elem, deck_rawdict[elem][0]))
	random.shuffle(deck_array)
	random.shuffle(extra_deck_array)

	fusion_dict = {}
	with open("合成一覧.txt") as f:
		reader = csv.reader(f, delimiter = ',')
		header = next(reader)
		for row in reader:
			fusion_material   = str(row[0]).strip()
			required_elements = str(row[1]).split('.')
			fusion_dict[fusion_material] = [x.strip() for x in required_elements]
	

	screen = pygame.display.set_mode((2 * l_mergin + (card_size_x + x_mergin) * x_full_size, 2 * t_mergin + (card_size_y + y_mergin) * y_full_size))
	pygame.display.set_caption("ALCHEMIST")
	screen.fill(Green)

	mycard = []
	opponent_card = []
	for i in range(6):
		mycard.append(deck_array.pop())
		opponent_card.append(deck_array.pop())



	onstage_cards = []
	for x in range(3):
		x = x + 1
		for y in range(5):
			if y == 0:
				element_name, element_cost = opponent_card.pop()
				tmp = card_propaty(screen, x, y, card_size_x, card_size_y, element = card_render_dict[element_name][1], cost = element_cost, element_name_str = card_render_dict[element_name][0])
			elif y == 1:
				element_name, element_cost = opponent_card.pop()
				tmp = card_propaty(screen, x, y, card_size_x, card_size_y, element = card_render_dict[element_name][1], cost = element_cost, face = card_face.flont, element_name_str = card_render_dict[element_name][0])
			elif y == 2:
				tmp = card_propaty(screen, x, y, card_size_x, card_size_y, face = card_face.invalid)
			elif y >  2:
				element_name, element_cost = mycard.pop()
				tmp = card_propaty(screen, x, y, card_size_x, card_size_y, element = card_render_dict[element_name][1], cost = element_cost, face = card_face.flont, element_name_str = card_render_dict[element_name][0])
			onstage_cards.append(tmp)

	my_event_cards = []
	for i in range(2):
		card_name, card_cost = extra_deck_array.pop()
		tmp = event_card_propaty(screen, 0, 3 + i, card_size_x, card_size_y, element = card_render_dict[card_name][1], cost = card_cost, face = card_face.flont, element_name_str = card_render_dict[card_name][0])
		my_event_cards.append(tmp)

	my_fusion_button  = fusion_button(screen, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin), 3 * card_size_x + 2 * x_mergin, card_size_y, fusion_dict)
	my_turnend_button = turnend_button(screen, l_mergin + 4 * (card_size_x + x_mergin), t_mergin + 3 * (card_size_y + y_mergin), 160, 120)
	my_swap_button    = swap_button(screen, l_mergin + 4 * (card_size_x + x_mergin), t_mergin + 4 * (card_size_y + y_mergin), 160, 120)
	common_deck = deck(screen, 4, 2, card_size_x, card_size_y, rest = len(deck_array))
	extra_deck  = deck(screen, 5, 2, card_size_x, card_size_y, rest = len(extra_deck_array))

	#pp.pprint(fusion_dict)
	#pp.pprint(mycard)
	#pp.pprint(opponent_card)
	#pp.pprint(deck_array)

	player_turn = True
	shokubaicounter = 0
	while(True):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			common_deck.draw_card_with_rest()
			extra_deck.draw_card_with_rest()
			my_turnend_button.draw(player_turn)
			my_swap_button.draw()
			if player_turn:
				my_fusion_button.draw()
				for unused in filter(lambda l: not l.used and l.y_pos_index in [1, 3, 4], onstage_cards):
					unused.face = card_face.flont
				currently_selected_cards = [x for x in onstage_cards if x.isSelected]

				if event.type == MOUSEBUTTONDOWN:
					x, y = event.pos
					x_index, y_index = mouse_pos_2_index(x, y)

					if x_index != -1 and y_index in [1, 3, 4]:

						for selected_card in filter(lambda l: l.x_pos_index == x_index and l.y_pos_index == y_index and l.face == card_face.flont, onstage_cards):
							selected_card.isSelected = not selected_card.isSelected

					if x_index ==  0 and y_index in [3, 4]:
						for selected_card in filter(lambda l: l.x_pos_index == x_index and l.y_pos_index == y_index and l.face == card_face.flont, my_event_cards):
							selected_card.face = card_face.back
							if selected_card.element_name_str == "在庫処分":
								player_points += selected_card.cost
								message_draw(screen, "%s：コスト%d"%(selected_card.element_name_str, selected_card.cost), 15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 25)
								message_draw(screen, "合計：%3dポイント"%(player_points),       15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 40)
								for i in [3, 8, 13, 14, 9, 4]:
									if onstage_cards[i].isSelected and not onstage_cards[i].used:
										tmp_tuple = (onstage_cards[i].element_name_str, onstage_cards[i].cost)
										deck_array.append(tmp_tuple)
										random.shuffle(deck_array)
										tmp_receiver = deck_array.pop()
										name = tmp_receiver[0]
										cost = tmp_receiver[1]
										onstage_cards[i].element          = card_render_dict[name][1]
										onstage_cards[i].cost             = cost
										onstage_cards[i].element_name_str = card_render_dict[name][0]
								for card in onstage_cards:
									card.isSelected = False

							elif selected_card.element_name_str == "ヒット化！":
								hitflag = True
								message_draw(screen, "%s：コスト%d"%(selected_card.element_name_str, selected_card.cost), 15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 25)
								message_draw(screen, "合計：%3dポイント"%(player_points),       15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 40)

							elif selected_card.element_name_str == "抜き打ち検査":
								message_draw(screen, "%s：コスト%d"%(selected_card.element_name_str, selected_card.cost), 15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 25)
								message_draw(screen, "合計：%3dポイント"%(player_points),       15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 40)

								nukiuchiflag = True
							elif selected_card.element_name_str == "触媒":
								shokubaiflag = True
								shokubaicounter = 3
								message_draw(screen, "触媒中", 15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 55)
								selected_card.face = card_face.back
							selected_card.used = True

					my_fusion_button.is_pushed(x, y)
					if my_fusion_button.button_on:
						my_fusion_button.selected_cards = list(filter(lambda card: card.isSelected, onstage_cards))
						my_fusion_button.fusion()

					my_turnend_button.is_pushed(x, y)
					if my_turnend_button.button_on:
						player_turn = False
						hitflag     = False
						shokubaicounter -= 1
						if shokubaiflag:
							message_draw(screen, "触媒中", 15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 55)
						if shokubaicounter < 1:
							shokubaiflag = False
							message_draw(screen, "             ", 15, l_mergin + (card_size_x + x_mergin), t_mergin + 2 * (card_size_y + y_mergin) + card_size_y / 2 + 55)


						hand_out_cards(onstage_cards, deck_array, card_render_dict)
						hand_out_cards(my_event_cards, extra_deck_array, card_render_dict)

						common_deck.rest = len(deck_array)
						extra_deck.rest  = len(extra_deck_array)
						for card in onstage_cards:
							card.isSelected = False
							if card.y_pos_index > 2:
								card.used = False
								card.face = card_face.flont
						for card in my_event_cards:
							card.isSelected = False
							card.used = False
							card.face = card_face.flont


					my_swap_button.is_pushed(x, y)
					if my_swap_button.button_on:
						tmp_x = onstage_cards[3].x_pos_index
						tmp_y = onstage_cards[3].y_pos_index
						onstage_cards[ 3].x_pos_index = onstage_cards[ 4].x_pos_index
						onstage_cards[ 3].y_pos_index = onstage_cards[ 4].y_pos_index
						onstage_cards[ 4].x_pos_index = onstage_cards[ 9].x_pos_index
						onstage_cards[ 4].y_pos_index = onstage_cards[ 9].y_pos_index
						onstage_cards[ 9].x_pos_index = onstage_cards[14].x_pos_index
						onstage_cards[ 9].y_pos_index = onstage_cards[14].y_pos_index
						onstage_cards[14].x_pos_index = onstage_cards[13].x_pos_index
						onstage_cards[14].y_pos_index = onstage_cards[13].y_pos_index
						onstage_cards[13].x_pos_index = onstage_cards[ 8].x_pos_index
						onstage_cards[13].y_pos_index = onstage_cards[ 8].y_pos_index
						onstage_cards[ 8].x_pos_index = tmp_x
						onstage_cards[ 8].y_pos_index = tmp_y

			else:#not player_turn
				player_turn = opponent_action()

			for card in onstage_cards:
				card.draw_card()
			for card in my_event_cards:
				card.draw_card()

			pygame.display.update()


if __name__ == "__main__":
	main()
