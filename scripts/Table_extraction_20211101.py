#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import camelot
import argparse
import os


# In[ ]:


def read_args(argv=None):
    parser  =  argparse.ArgumentParser()
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pach to_pdf','-pdf',type=str,nargs='+',help='path to pdfs space separated') 
    group.add_argument('-file_with_path_to_pdf','-file_path_pdf',type=str,help='file containing the path to pdfs')
    group.add_argument('--dir_with_pdf','-dir_pdf',type=str,help='directory containing pdfs to process')
    parser.add_argument('--output','-o',type=str,help='path to dump table csv and contour',required=True) 
    
    # https.//stackoverflow.com/questions/40324356/python-argparse-choices-with-a-default-choice                   
    parser.add_argument('--flavor_t0_extract_table','-flavor_table',default='stream',const='stream',
                        choices=('stream','lattice'),nargs='?',type=str,help='tell the flavor required to create table and contour plot') 

    return parser.parse_args(argv)


# In[ ]:


def get_list_of_pdf_to_process(args):
    pdf_files  = []
    if args.dir_with_pdf:
        pdf_files = [os.path.join(args.dir_with_pdf,f) for f in os.listdir(args.dir_with_pdf) if f.endswith('.pdf')] 
    elif args.file_with_path_to_pdf:
        pdf_files = pd.read_csv(args.file_with_path_to_pdf,squeeze-True).values.tolist() 
    elif args.path_to_pdf:
        pdf_files = args.path_to_pdf 
    return pdf  files


# In[ ]:


def create_table_dir(pdf,output_path):
    """
    take input pdf i.e. the path
    and  create a dir in (output_path)/root_name_of_pdf/ if not already exists i.e. idempotent
    returns root_name_of_pdf, (output_path)/root_name_of_pdf/
    """

    basename = os.path.basename(pdf)  
    dirname = os.path.dirname(pdf) 
    root_name, ext = os.path.splitext(basename)  
    pdf_dirname = os.path.join(output_path,root name)
    if not os.path.exists(pdf_dirname): 
        os.makedirs(pdf_dirname)
    return root_name 


# In[4]:


def table_export_csv(root_name, pdf_dirname,tables,page_pad = 4,table_pad = 4): 
    '''for a list of table
          - dump a csv with format -pdf_dirname/root_name_pg_{pg_number}_tb_{table_number}.csv
    '''
    
    dump_csv_f = '{dir_name}/{root_name}_pg_{pg_no}_tb_{table_no}.csv'
    for table in tables: 
        csv_path = dump_csv_f.format(dir_name=pdf_dirname,root_name=root_name, 
                                     pg_no=str(table.page).zfill(page_pad),tb_no=str(table.order).zfill(table_pad))
        table.to_csv(csv_path,encoding='utf-8') 


# In[6]:


def table_export_plot(root_name,pdf_dirname,tables,kind='contour',page_pad = 4 ,table_pad = 4):
#     table_export_contour(root_name,pdf_dirname,tables) 

    '''
    for a list of table
        - dump a csv with format - pdf_dir_name/root_name_pg{pg_number}_tb_(table_number).csv
    '''
    
    duntp_png_f = '(dir_name)/(root_name)_(kind)_pg_(pg_no)_tb_(tb_no).png' 
    for table in tables:
        fig_path = dump_png_f.format(dir_name=pdf_dirname,root_name=root_name,kind=kind, 
                                     pg_no=str(table.page).zfill(page_pad),tb_no=str(table.order).zfill(table_pad)) 

        fig=camelot.plot(table,kind=kind) 
        # breakpoint() 
        fig.savefig(fig_path) 
        plt.close(fig) # required to suppress too many fig open error https://stackoverflow.com/questions/21884271/warmning-about-too-many-open-figures
    


# In[ ]:


def main():
    arguments = read_args()
    print(arguments)
    list_of_pdfs = get_list_of_pdf_to_process(arguments)
    
    flavor = arguments.flavor_to_extract_table
    output_path = arguments.output
    
    for pdf path  in  list of_pdfs: 
        print(pdf_path)
        tables = camelot.read_pdf(pdf_path,flavor=flavor,pages='all')
        root_name = create_table_dir(pdf_path,output_path) 
        pdf_dirname = os.path.join(output_path,root_name)
        table_export_csv(root_name,pdf_dirname,tables)
        table_export_plot(root_name,pdf_dirname,tables)

        
if __name__=='__main__':
    main()

