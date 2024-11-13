import plotly.express as px
import plotly.graph_objects as go

# Example 1: Scatter Plot
def scatter_plot():
    df = px.data.iris()  # Load example dataset
    fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species',
                     title='Scatter plot of Sepal Width vs Sepal Length')
    fig.show()

# Example 2: Line Chart
def line_chart():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x='year', y='gdpPercap', title='GDP per Capita in Canada')
    fig.show()

# Example 3: Bar Chart
def bar_chart():
    df = px.data.tips()
    fig = px.bar(df, x='day', y='total_bill', color='sex', barmode='group',
                 title='Total Bill by Day and Gender')
    fig.show()

# Example 4: Pie Chart
def pie_chart():
    df = px.data.tips()
    fig = px.pie(df, values='total_bill', names='day', title='Total Bill Distribution by Day')
    fig.show()

# Example 5: 3D Scatter Plot
def scatter_3d():
    df = px.data.iris()
    fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                        color='species', title='3D Scatter plot of Iris dataset')
    fig.show()

if __name__ == "__main__":
    scatter_plot()
    line_chart()
    bar_chart()
    pie_chart()
    scatter_3d()
