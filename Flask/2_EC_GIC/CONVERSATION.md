# GitHub Copilot conversation: 2_EC_GIC #
## Prompt: ##
On the home page of my application all products are displayed. When clicking on "Lowest price first", all products on the home page should be displayed ordered by lowest price first. But, when clicking on "Lowest price first", I am being redirected to the product page of product 2. Solve this error. 

In `home.py`:
```python
"""General page routes."""
from flask import Blueprint
from flask import current_app as app
from flask import render_template

from flask_blueprint_tutorial.api import fetch_products

# Blueprint Configuration
home_blueprint = Blueprint("home_blueprint", __name__, template_folder="templates", static_folder="static")


@home_blueprint.route("/", methods=["GET"])
def home() -> str:
    """
    Serve `Home` page template.

    :returns: str
    """
    products = fetch_products(app)
    return render_template(
        "index.jinja2",
        title="Flask Blueprint Demo",
        subtitle="Demonstration of Flask blueprints in action.",
        template="home-template",
        products=products,
    )


@home_blueprint.route("/about", methods=["GET"])
def about() -> str:
    """
    Serve `About` page template.

    :returns: str
    """
    return render_template(
        "index.jinja2",
        title="About",
        subtitle="This is an example about page.",
        template="home-template page",
    )


@home_blueprint.route("/contact", methods=["GET"])
def contact() -> str:
    """
    Serve `Contact` page template.

    :returns: str
    """
    return render_template(
        "index.jinja2",
        title="Contact",
        subtitle="This is an example contact page.",
        template="home-template page",
    )
```
In `index.jinja2`:
```
{% extends "layout.jinja2" %}

{% block pagestyles %}
  {% assets "home_style_bundle" %}
    <link href="{{ ASSET_URL }}" rel="stylesheet" type="text/css">
  {% endassets %}
{% endblock %}

{% block content %}
  {% include "navigation.jinja2" %}

  <div class="container">
    <h1>{{ title }}</h1>
    <h2>{{ subtitle }}</h2>
    <div class="resource-links">
      <p class="resource-link">Github repo <a href="https://github.com/hackersandslackers/flask-blueprint-tutorial">here.</a></p>
      <p class="resource-link">Tutorial <a href="https://hackersandslackers.com/flask-blueprints/">here.</a></p>
    </div>

      <!-- Dropdown for filtering -->
      <div class="dropdown">
          <div class="dropdown-content">
              <a href="/products/2">Lowest price first</a>
          </div>
      </div>

    <div class="products">
      {% for product in products %}
        <a href="/products/{{ loop.index - 1 }}/" class="product-preview">
          <img class="product-image" src="{{ product.image }}" alt="profile"/>
          <div class="name">{{ product.name }}</div>
          <div class="price">${{ product.salePrice }}</div>
        </a>
      {% endfor %}
    </div>
  </div>

 {% include "blueprintinfo.jinja2" %}

{% endblock %}
```
In `api.py`:
```python
"""Read placeholder data for demo purposes."""
import json

from flask import Flask


def fetch_products(app: Flask) -> dict:
    """
    Grab hardcoded product listings.

    :param Flask app: Flask application object.

    :returns: dict
    """
    product_data_filepath = app.config["PRODUCT_DATA_FILEPATH"]
    with open(product_data_filepath, encoding="utf-8") as file:
        products_data = json.load(file)
        return products_data
```

## GitHub Copilot response: ##
The issue is that the "Lowest price first" link is hardcoded to redirect to "/products/2". To fix this, you need to create a new route that sorts the products by price and then renders the home page with the sorted products.

Here's how you can do it:

1. Add a new route in `home.py` that sorts the products by price and renders the home page:

```python
@home_blueprint.route("/sort/price", methods=["GET"])
def sort_by_price() -> str:
    """
    Serve `Home` page template with products sorted by price.

    :returns: str
    """
    products = fetch_products(app)
    products.sort(key=lambda x: x['salePrice'])
    return render_template(
        "index.jinja2",
        title="Flask Blueprint Demo",
        subtitle="Demonstration of Flask blueprints in action.",
        template="home-template",
        products=products,
    )
```

2. Update the "Lowest price first" link in `index.jinja2` to point to the new route:

```html
<a href="/sort/price">Lowest price first</a>
```

This will sort the products by their 'salePrice' attribute when the "Lowest price first" link is clicked, and then render the home page with the sorted products.