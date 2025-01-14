#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os 
import camelot
import matplotlib.pyplot as plt 
from matplotlib import patches 
import numpy as np 
from collections import defaultdict 
from collections import Counter 
import sys 
from functools import partial 
from pathlib import Path  

from camelot.utils import text_in_bbox,get_table_index
from camelot.parsers import Lattice
import argparse
import json


# In[7]:


# path_to_file = sys.argv[1] # ./appl/passdatall/infersent/table_extraction/data/Apple_2019_211.pdf
# page_no = int(sys.argv[2]) 

def extracr_table(path_to_file, page_no): 
    response = {"image_path":None,"tables":[],"table_cell_coordinates":[],"table_vertical_line_coordinates":dict()}
    path_lib = Path(path_to_file) 
    base_path_dir,write_dir = path_lib.parent, path_lib.stem 
    path_to_dump = base_path_dir/write_dir 
    try:
        os.makedirs(base_path_dir/write_dir) 
    except Exception as e: 
        print(e)

    try: 
        # table_lattice = camelot.read_pdf(path file,flavor=istream.,pages=f'(page_no)') 
        tables_lattice = camelot.read_pdf(path_to_file,flavor='stream',pages=f'(page_no)')
                        #layout_kwargs = ('char_margin':0.4)  
                        # run CBL_4Q19_Earnings_02_06_20.pdf to see the difference 
    
    except IndexError: 
        return {'end_of_page':True}


# In[8]:


from IPython.display import display


# In[9]:


class Page: 
    def __init__(self, height,width,fill_value=1,scale=10): 
        '''
        create scale*height x scale*width matrix filled with fill_value
        '''
        self. scale = scale 
        self.height = self.to_scale(height) 
        self.width = self.to_scale(width) 
        self.fill_Value = fill_value 
        
        self.matrix = np.full((self.height,self.width),fill_value=fill_value,dtype=np.bool)
        
    def to_sacale(self,val): 
        return int(val*self.scale)
    
    def add_patch(self,x_bottom, y_bottom,height,width,fill=True,value=0): 
        x_bottom,y_bottom,height,width = self.to_scale(x_bottom),self.to_scale(y_bottom),self.to_scale(height),self.to_scale(width) 
        # print(x_bottosai-yb!attom,heightsuidth) 
        if fill:
            self.matrix[y_bottom:y_bottom+ height,x_bottom:x_bottom+width] = value 
        else: 
            #print(x_bottom+width,y_bottom+height) 
            
            self.matrix[y_bottom,x_bottom:x_bottom+width]=value 
            self.matrix[y_bottom:y_bottom+height,x_bottom] = value 
            self.matrix[y_b0ttom+height,x_bottom:x_bottom+width] = value 
            
    def show_page(self):
        return plt.imshow(self.matrix, origin='lower')


# In[ ]:


page = table_lattice[0]
bottom_left_x_of_chars, bottom_left_y_of_chars, upper_right_of_chars, upper_right_y_of_chars = zip(*page._text)


# In[ ]:


min_x, min_y =max(min(bottom_left_x_of_char) - 10,0), max(min(bottom_left_y_of_chars) - 10,0)
max_x, max_y =max(upper_right_x_of_chars) + 10, max(upper_right_y_of_chars) + 10


# In[ ]:


min_x,min_y,max_x,max_y


# In[ ]:


page_ds = Page(hieght=max_y,width=max_x)


# In[ ]:


for tin page._text:
    page_ds.add_patch(t[0],t[1],hieght=t[3]-t[1],width=t[2]-t[0])


# In[ ]:


page_ds.show_page()


# In[ ]:


number_of_empty_rows_in_each_column = page_ds.matrix.sum(axis=0)


# In[ ]:


number_of_full_rows_in_each_columns = page_ds.height - number_of_empty_rows_in_each_column


# In[ ]:


def get_margin(number_of_full_rows_in_each_column,gradient_threshold = 20,
               minimum_number_of_full_rows_in_a_column=30,margin='left'):
    '''
    1. gradient threshold
    2. margin = 'right' or 'left'
    '''
 
    breakpoint() 
    assert margin in ['right','Left'],"margin can only be left or right but passed{}".format(margin) 
    if margin=='right': 
        number_of_full_rows_in_each_column = number_of_full_rows_in_each_column[::-1].copy()
        
    gradient_number_of_full_rows_in_each_column = np.gradient(number_of_full_rows_in_each_column)
    
    margin_coord = np.argmax(number_of_full_rows_in_each_column > int(minimum_number_of_full_rows_in a_column)) 
    margin_coord = np.argmax(gradient_number_of_full_rows_in_each_column[margin_coord:] > int(gradient_threshold)) + margin_coord 
    
    if margin=='right': 
        margin_coord = len(number_of_full_rows_in_each_column) - margin_coord -1  
        
    return margin_coord 


# In[ ]:


threshold = 0.1 


# In[ ]:


left_margin_x = get_margin(number_of_full_rows_in_each_columns)


# In[ ]:


right_margin_x = get_margin(number_of_full_rows_in_each_column,margin='right')


# In[ ]:


left_margin_x, right_margin_x


# In[ ]:


vertical_region_under_consideration = page_ds.matrix[:,left_margin_x:right_margin_x+1].copy()


# In[ ]:


plt.matshow(page_ds.matrix, origin="lower")


# In[ ]:


plt.matshow(vertical_region_under_consideration,origin='lower')


# In[ ]:


number_of_empty_cells_in_each_rows = vertical_region_under_consideration.sum(axis=1)


# In[ ]:


### first Itft index satisfying the cond 

def first_left_index_satisfying_cond(a,cond,enumeration_start =0):
    
        '''
        Return the left most index in array a starting from enumertion_start
        Return None if no elem satisfies the cond
        '''
        

    for idx,num in enumerate(a[enumerationstart:],start=enumeration_start): 
        #print(idx,num,a) 
        if cond(num): 
            return idx 
    
    return None 


# In[ ]:


def first interval satisfying_cond(a,cond,start_index=0):
    
    '''
    returns the first interval satisfying a condition starting at index start_index 
    interval follows python slice convention where last index is exclusive
    '''

    not cond = lambda x:not(cond(x))
    
    interval_start = first_left_indexsatisfying_cond(a,cond,start_index) 
    if interval_start is None: 
        return () 
#     interval_start_not_cond = first_left_index_satisfying_cond(a,not_cond,interVal_star 
#     if interval_start_not_cond is None: 
#     return (interval_start,len(a)) 
#     interval_end = interval_start_not_cond 
    interval_end = first_left_index_satisfying_cond(a,not_cond,interval_start)   
    interval_end = interval_end if interval_end else len(a) 
    return (interval_start,interval_end) 


# In[ ]:


def interval_matching(a,cond):
    
    '''
    Return contiguous range of intervals satisfying a given cond 
    Range conform to python range convention where end is exclusive
    '''

    intervals_satisfying_cond = [] 
    current_interval = first_interval_satisfying_cond(a,cond) 
    if not current_interval: 
        return intervals_satisfying_cond 
    previous_interval_start , previous_interval_end = current_interval 
    intervals_satisfying_cond.append(current_interval)
    
    while previous_interval_end <= len(a): 
        current_interval = first_interval_satisfying_cond(a,cond,previous_interval_end) 
        if not current_interval: break 
        previous_interval_start , previous_interval_end = current_interval 
        intervals_satisfying_cond.append(current_interval)
        
    return intervals_satisfying_cond 

