from flask import Flask, send_from_directory
from flask_graphql import GraphQLView
from schema import schema


app = Flask(__name__)

# Create a GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)


# Serve static files
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
