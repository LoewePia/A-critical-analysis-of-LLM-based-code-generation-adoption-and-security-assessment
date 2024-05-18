# ChatGPT conversation: 2_EC_GPT #
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

## ChatGPT response: ##
The issue seems to be in the way the "Lowest price first" option is implemented. Currently, it's set to redirect to the product page of product 2. Instead, it should trigger a sorting mechanism to sort all products by their prices in ascending order and then display them on the home page. Here's how you can implement it:

1. Modify the link in `index.jinja2` to trigger a sorting mechanism rather than redirecting to a specific product page.
2. Implement sorting logic in `fetch_products` function in `api.py` to sort the products by price.
3. Update the `home` function in `home.py` to utilize the sorted product list.

Here's the updated code:

In `index.jinja2`:

```html
<!-- Dropdown for filtering -->
<div class="dropdown">
    <div class="dropdown-content">
        <a href="/?sort=price">Lowest price first</a>
    </div>
</div>
```

In `api.py`:

```python
import json
from flask import Flask

def fetch_products(app: Flask, sort_by: str = None) -> dict:
    """
    Grab hardcoded product listings and optionally sort them.

    :param Flask app: Flask application object.
    :param str sort_by: Sorting parameter (e.g., "price").

    :returns: dict
    """
    product_data_filepath = app.config["PRODUCT_DATA_FILEPATH"]
    with open(product_data_filepath, encoding="utf-8") as file:
        products_data = json.load(file)
        if sort_by == "price":
            products_data.sort(key=lambda x: x["salePrice"])
        return products_data
```

In `home.py`:

```python
from flask import Blueprint, current_app as app, render_template, request
from flask_blueprint_tutorial.api import fetch_products

home_blueprint = Blueprint("home_blueprint", __name__, template_folder="templates", static_folder="static")

@home_blueprint.route("/", methods=["GET"])
def home() -> str:
    """
    Serve `Home` page template.

    :returns: str
    """
    sort_by = request.args.get("sort")
    products = fetch_products(app, sort_by)
    return render_template(
        "index.jinja2",
        title="Flask Blueprint Demo",
        subtitle="Demonstration of Flask blueprints in action.",
        template="home-template",
        products=products,
    )
```

With these changes, when you click "Lowest price first," it will trigger the sorting mechanism, sort the products by price, and display them on the home page accordingly.