import matplotlib 
import pandas as pd
import matplotlib.pyplot as plt
from splink.datasets import splink_datasets

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

subset_a = splink_datasets.historical_50k.sample(40000)
subset_b = splink_datasets.historical_50k.sample(10000)

merged_df = pd.merge(splink_datasets.historical_50k, subset_b, how='outer', indicator=True)

# Filter out rows that are only in the subset DataFrame
subset_df = merged_df[merged_df['_merge'] == 'right_only'].drop('_merge', axis=1)

# Filter out rows that are in the subset DataFrame from the original DataFrame
df = merged_df[merged_df['_merge'] == 'left_only'].drop('_merge', axis=1)

subset_c = df.sample(10000)