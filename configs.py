from jinja2 import Template

def get_model_cfg(model):
    with open('snmp_config_template.j2') as f:
        template = Template(f.read())

    rendered_template = template.render(model=model)

    return rendered_template.strip().split('\n')


if __name__ == '__main__':
   print(get_model_cfg('ruckus')) #სატესტო
