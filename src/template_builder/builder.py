import os
import shutil
import typing
from pathlib import Path

import jinja2
import pydantic
import black


cd = Path(os.path.dirname(__file__))
project_root = cd.parent.parent


class CloudComponentDescription(pydantic.BaseModel):
    type: typing.Literal["S3Bucket", "EC2Instance", "LambdaFunction"]
    args: dict


class StackDescription(pydantic.BaseModel):
    lang: typing.Literal["TypeScript", "Python"]
    provider: typing.Literal["AWS", "GCP", "Azure"]
    summary: str | None = None
    components: list[CloudComponentDescription]


def generate_python(desc: StackDescription) -> str:
    template_directory = (cd / 'templates' / 'python').absolute()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_directory))
    template = env.get_template('stack.py.j2')

    code = template.render(
        stack_name='AppStack',
        s3_buckets=list(filter(lambda c: c.type == 'S3Bucket', desc.components)),
        ec2_instances=list(filter(lambda c: c.type == 'EC2Instance', desc.components)),
        lambda_functions=list(filter(lambda c: c.type == 'LambdaFunction', desc.components)),
    )
    return black.format_str(code, mode=black.FileMode())


def build(desc: str | dict):
    if isinstance(desc, str):
        desc = StackDescription.model_validate_json(desc)
    else:
        desc = StackDescription.model_validate(desc)

    if desc.lang.lower() == 'python':
        code = generate_python(desc)
    else:
        raise NotImplementedError

    formation_folder = project_root / 'app'

    if formation_folder.is_dir():
        shutil.rmtree(formation_folder)

    formation_folder.mkdir()
    os.chdir(formation_folder)
    os.system('cdk init -l python')

    with (formation_folder / 'app' / 'app_stack.py').open('w') as f:
        f.write(code)

    shutil.copy(cd / 'assets' / 'app.py', formation_folder / 'app.py')
    os.makedirs(formation_folder / 'lambda_handlers', exist_ok=True)
    shutil.copy(cd / 'assets' / 'handler.py', formation_folder / 'lambda_handlers' / 'handler.py')
