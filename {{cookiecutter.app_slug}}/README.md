# {{ cookiecutter.app_name }}

{{ cookiecutter.app_description }}

Do you have Docker? Then Run

```bash
docker build --tag <your_tag> .
```

You don't have Docker? Then Run:

```
pip install invoke
```

And then:

```
invoke buildAndServe
```
