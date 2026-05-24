import matplotlib.pyplot as plt
import numpy as np

# Настройка шрифта
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

tasks = ['Задача 1', 'Задача 2']

# Время (в часах)
time_tdd = [6.0, 7.0]          # TDD Only
time_tdd_llm = [3.25, 3.5]     # TDD + LLM  
time_llm = [0.5, 1.0]          # LLM Only

# Данные по токенам из логов
# Токены: Задача 1
t1_tdd_llm_input = 13165
t1_tdd_llm_output = 7184
t1_llm_input = 1115
t1_llm_output = 4358
t1_llm_cached = 512

# Токены: Задача 2
t2_tdd_llm_input = 78046
t2_tdd_llm_output = 23338
t2_llm_input = 89703
t2_llm_output = 40691
t2_llm_cached = 65764


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Левая гистограмма: Время
x = np.arange(len(tasks))
width = 0.22

bars1 = ax1.bar(x - width, time_tdd, width, label='TDD Only', color='#4472C4')
bars2 = ax1.bar(x, time_tdd_llm, width, label='TDD + LLM', color='#ED7D31')
bars3 = ax1.bar(x + width, time_llm, width, label='LLM Only', color='#A5A5A5')

ax1.set_ylabel('Время (часы)', fontsize=12)
ax1.set_title('Время разработки', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(tasks, fontsize=12)
ax1.legend(fontsize=10)

# Подписи значений
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1, str(height),
             ha='center', va='bottom', fontsize=9)
for bar in bars2:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1, str(height),
             ha='center', va='bottom', fontsize=9)
for bar in bars3:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1, str(height),
             ha='center', va='bottom', fontsize=9)


# Правая гистограмма: Токены
x_tokens = np.arange(4)
width_t = 0.22

# Данные: [Задача1 TDD+LLM, Задача1 LLM Only, Задача2 TDD+LLM, Задача2 LLM Only]
input_data = [t1_tdd_llm_input, t1_llm_input, t2_tdd_llm_input, t2_llm_input]
output_data = [t1_tdd_llm_output, t1_llm_output, t2_tdd_llm_output, t2_llm_output]
cached_data = [0, t1_llm_cached, 0, t2_llm_cached]

bars4 = ax2.bar(x_tokens - width_t, input_data, width_t, label='Входные', color='#4472C4')
bars5 = ax2.bar(x_tokens, output_data, width_t, label='Выходные', color='#ED7D31')
bars6 = ax2.bar(x_tokens + width_t, cached_data, width_t, label='Кэшированные', color='#70AD47')

ax2.set_ylabel('Количество токенов', fontsize=12)
ax2.set_title('Использование токенов', fontsize=12)
ax2.set_xticks(x_tokens)
ax2.set_xticklabels(['Задача 1\nTDD+LLM', 'Задача 1\nLLM Only', 'Задача 2\nTDD+LLM', 'Задача 2\nLLM Only'], fontsize=10)
ax2.legend(fontsize=10)

# Подписи значений
for bar in bars4:
    height = bar.get_height()
    if height > 0:
        ax2.text(bar.get_x() + bar.get_width()/2., height + 500,
                 f'{int(height):,}', ha='center', va='bottom', fontsize=8)
for bar in bars5:
    height = bar.get_height()
    if height > 0:
        ax2.text(bar.get_x() + bar.get_width()/2., height + 500,
                 f'{int(height):,}', ha='center', va='bottom', fontsize=8)
for bar in bars6:
    height = bar.get_height()
    if height > 0:
        ax2.text(bar.get_x() + bar.get_width()/2., height + 500,
                 f'{int(height):,}', ha='center', va='bottom', fontsize=8)


plt.tight_layout()
fig.savefig('histograms.png', dpi=200, bbox_inches='tight')
print("Гистограмма сохранена: histograms.png")