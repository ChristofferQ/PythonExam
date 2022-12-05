def add_labels(x,y):
    """
    Add labels to barplot.
    """
    import matplotlib.pyplot as plt
    
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def make_autopct(values):
    """
    This is a helper function to display values in a pie chart.
    """
    import matplotlib.pyplot as plt
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct