import matplotlib 
import pandas as pd
import matplotlib.pyplot as plt

def format_model_m_and_us(linker):
  model  = linker.save_settings_to_json()
  m_and_us = []
  for variable in model['comparisons']:
    for level in variable['comparison_levels']:
      if 'm_probability' in level:
        m_and_us.append({'variable':variable['output_column_name'],'sql_condition':level['label_for_charts'],'m_probability':level['m_probability']}) 
      if 'u_probability' in level:
        m_and_us[-1]['u_probability'] = level['u_probability']
  m_and_us = pd.DataFrame(m_and_us)
  m_and_us = m_and_us[['variable','sql_condition','m_probability','u_probability']]
  m_and_us['1-u'] = 1-m_and_us['u_probability']
  return m_and_us


def plot_m_and_u(df,ax,marker=''):
  groups = df.groupby('variable')
  i=0
  for variable, group in groups:
    ax.scatter(group['1-u'], group.m_probability, edgecolors = list(matplotlib.colors.TABLEAU_COLORS.keys())[i], c = 'none',label=variable,marker=marker)
    ax.set_xlabel('1 - u-probability')
    ax.set_ylabel('m-probability')
    i+=1  

