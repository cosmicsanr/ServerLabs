from datetime import date

from fastapi import (
    APIRouter,
    Request,
    Response,
    Depends,
    responses,
    status
)

from fastapi_chameleon import template

from services import student_service
from common.common import (
    is_valid_name,
    is_valid_email,
    is_valid_iso_date,
    is_valid_password,
)

from common.viewmodel import ViewModel
from common.fastapi_utils import form_field_as_str
from common.auth import (
    get_current_user,
    requires_unauthentication,
    requires_authentication,
    set_auth_cookie,
    delete_auth_cookie,
)

MIN_DATE = date.fromisoformat('1920-01-01')

router = APIRouter()


@router.get(
    '/account/register',
    dependencies=[Depends(requires_unauthentication),]
)
@template()
async def register():
    return register_viewmodel()


def register_viewmodel():
    return ViewModel(
        name='',
        email='',
        password='',
        birth_date='',
        min_date=MIN_DATE,
        max_date=date.today(),
        checked=False,
    )


@router.post(
    '/account/register',
    dependencies=[Depends(requires_unauthentication),]
)
@template(template_file='account/register.pt')
async def post_register(request: Request):
    vm = await post_register_viewmodel(request)

    if vm.error:
        return vm

    # TODO: fazer um login (ie, memorizar que o utilizador fez login) com cookies
    return exec_login(vm.new_student_id)


async def post_register_viewmodel(request: Request):
    def is_valid_birth_date(birth_date: str) -> bool:
        return (is_valid_iso_date(birth_date)
                and date.fromisoformat(birth_date) >= MIN_DATE)

    form_data = await request.form()
    vm = ViewModel(
        name=form_field_as_str(form_data, 'name'),
        email=form_field_as_str(form_data, 'email'),
        password=form_field_as_str(form_data, 'password'),
        birth_date=form_field_as_str(form_data, 'birth_date'),
        new_student_id=None,
        min_date=MIN_DATE,
        max_date=date.today(),
        checked=False,
    )
    print(vm)

    if not is_valid_name(vm.name):
        vm.error, vm.error_msg = True, 'Nome inválido!'
    elif not is_valid_email(vm.email):
        vm.error, vm.error_msg = True, 'Email inválido!'
    elif not is_valid_password(vm.password):
        vm.error, vm.error_msg = True, 'Senha inválida!'
    elif not is_valid_birth_date(vm.birth_date):
        vm.error, vm.error_msg = True, 'Data nascimento inválida!'

    # TODO: verificar se o estudante já exuste (email)
    elif student_service.get_student_by_email(vm.email):
        vm.error, vm.error_msg = True, f'Endereço de email {vm.email} já existe!'
    else:
        vm.error, vm.error_msg = False, ''

    # TODO: criar a conta se nao existir erro (obtendo o id do estudante)
    if not vm.error:
        student = student_service.create_account(
            vm.name,
            vm.email,
            vm.password,
            date.fromisoformat(vm.birth_date),
        )
        vm.new_student_id = student.id

    return vm


@router.get(
    '/account/login',
    dependencies=[Depends(requires_unauthentication),]
)
@template()
async def login():
    return login_viewmodel()


def login_viewmodel():
    return ViewModel(
        email='',
        password='',
    )


@router.post(
    '/account/login',
    dependencies=[Depends(requires_unauthentication),]
)
@template(template_file='account/login.pt')
async def post_login(request: Request):
    vm = await post_login_viewmodel(request)

    if vm.error:
        return vm

    return exec_login(vm.student_id)


async def post_login_viewmodel(request: Request) -> ViewModel:
    form_data = await request.form()
    vm = ViewModel(
        email=form_field_as_str(form_data, 'email'),
        password=form_field_as_str(form_data, 'password'),
        student_id=None,
    )
    if not is_valid_email(vm.email):
        vm.error_msg = 'Endereço de email inválido!'

    elif not is_valid_password(vm.password):
        vm.error_msg = 'Senha inválida!'

    elif not (student :=
              student_service.authenticate_student_by_email(vm.email, vm.password)):
        vm.error_msg = 'Utilizador ou senha inválida!'

    else:
        vm.error_msg = ''
        vm.student_id = student.id

    vm.error = bool(vm.error_msg)
    return vm


def exec_login(user_id: int) -> Response:
    response = responses.RedirectResponse(
        url='/', status_code=status.HTTP_302_FOUND)
    set_auth_cookie(response, user_id)
    return response


@router.get(
    '/account/logout',
    dependencies=[Depends(requires_authentication),]
)
async def logout():
    response = responses.RedirectResponse(
        url='/', status_code=status.HTTP_302_FOUND)
    delete_auth_cookie(response)
    return response


@router.get(
    '/account',
    dependencies=[Depends(requires_authentication),]
)
@template()
async def account():
    return account_viewmodel()


def account_viewmodel() -> ViewModel:
    student = get_current_user()
    # Current user must exist because we're in an authenticated
    # view context.
    assert student is not None

    return ViewModel(
        name=student.name,
        email=student.email,
    )


@router.post(
    '/account',
    dependencies=[Depends(requires_authentication),]
)
@template(template_file='account/account.pt')
async def update_account(request: Request):
    vm = await update_account_viewmodel(request)

    if vm.error:
        return vm

    return responses.RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)


async def update_account_viewmodel(request: Request):
    form_data = await request.form()
    student = get_current_user()
    assert student is not None

    vm = ViewModel()
    vm.error_msg = ''
    vm.name = student.name
    vm.email = form_field_as_str(form_data, 'email').strip()
    new_email = None if vm.email == student.email else vm.email
    current_password = form_field_as_str(form_data, 'current_password').strip()
    new_password = form_field_as_str(form_data, 'new_password').strip()

    if not student_service.password_matches(student, current_password):
        vm.error_msg = 'Senha inválida!'
    #:
    elif new_email:
        if not is_valid_email(new_email):
            vm.error_msg = f'Endereço de email {new_email} inválido!'
        elif student_service.get_student_by_email(new_email):
            vm.error_msg = f'Endereço de email {new_email} já existe!'
    #:
    elif student_service.password_matches(student, new_password):
        vm.error_msg = 'Nova senha é igual à anterior!'
    #:
    elif not is_valid_password(new_password):
        vm.error_msg = 'Senha inválida!'
    #:

    vm.error = bool(vm.error_msg)
    if not vm.error:
        student_service.update_account(
            student.id,
            current_password,
            new_email,
            new_password,
        )

    return vm
