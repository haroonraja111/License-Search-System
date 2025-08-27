from django.shortcuts import render, redirect
from django.db.models import Q, DateField, DateTimeField
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .models_license import License, Endorsenumber, Licenseupdation, Licensevehicle, Updationtype, Vehicletype
from .models_old import OldLicense, Endo
import logging
from django.contrib.auth import logout, authenticate, login

logger = logging.getLogger(__name__)

# ---------------------------- Helper Functions ---------------------------- #

def get_field_names_and_fields(model):
    concrete_fields = list(model._meta.fields)
    field_names = [f.name for f in concrete_fields]
    fields_by_name = {f.name: f for f in concrete_fields}
    return field_names, fields_by_name

def filter_by_licenseno(q, search_params, field_names):
    if search_params.get('licenseno'):
        if 'licenseno' in field_names:
            q &= Q(licenseno__icontains=search_params['licenseno'])
        elif 'number' in field_names:
            q &= Q(number__icontains=search_params['licenseno'])
    return q

def filter_by_cnic(q, search_params, field_names):
    if search_params.get('cnic') and 'cnic' in field_names:
        q &= Q(cnic__icontains=search_params['cnic'])
    return q

def filter_by_name(q, search_params, field_names):
    if search_params.get('name') and 'name' in field_names:
        q &= Q(name__icontains=search_params['name'])
    return q

def filter_by_fathername(q, search_params, field_names):
    if search_params.get('fathername') and 'fathername' in field_names:
        q &= Q(fathername__icontains=search_params['fathername'])
    return q

def filter_by_dob(q, search_params, field_names, fields_by_name):
    if search_params.get('dob') and 'dob' in field_names:
        dob_field = fields_by_name.get('dob')
        dob_value = search_params['dob']
        if isinstance(dob_field, (DateField, DateTimeField)):
            from datetime import datetime
            try:
                parsed_date = datetime.strptime(dob_value, '%Y-%m-%d').date()
                if isinstance(dob_field, DateTimeField):
                    q &= Q(dob__date=parsed_date)
                else:
                    q &= Q(dob=parsed_date)
            except Exception:
                pass
        else:
            q &= Q(dob__icontains=dob_value)
    return q

def filter_by_address(q, search_params, field_names):
    if search_params.get('address') and 'address' in field_names:
        q &= Q(address__icontains=search_params['address'])
    return q

def build_search_query(model, search_params):
    q = Q()
    field_names, fields_by_name = get_field_names_and_fields(model)
    q = filter_by_licenseno(q, search_params, field_names)
    q = filter_by_cnic(q, search_params, field_names)
    q = filter_by_name(q, search_params, field_names)
    q = filter_by_fathername(q, search_params, field_names)
    q = filter_by_dob(q, search_params, field_names, fields_by_name)
    q = filter_by_address(q, search_params, field_names)
    return q

def get_primary_key(obj, model_name):
    if hasattr(obj, 'serialno'):
        return obj.serialno
    elif hasattr(obj, 'id'):
        return obj.id
    else:
        try:
            return obj.pk
        except:
            logger.warning(f"Missing primary key for {model_name} object: {obj}")
            return None

def extract_basic_fields(obj):
    return {
        'licenseno': getattr(obj, 'licenseno', '') or '',
        'name': getattr(obj, 'name', '') or '',
        'fathername': getattr(obj, 'fathername', '') or '',
        'cnic': getattr(obj, 'cnic', '') or '',
        'dob': getattr(obj, 'dob', '') or '',
        'address': getattr(obj, 'address', '') or '',
    }

def prepare_result_object(obj, model_name, db_source):
    fields = extract_basic_fields(obj)
    primary_key = get_primary_key(obj, model_name)
    if primary_key is None:
        return None
    fields.update({
        'data': obj,
        'model': model_name,
        'db_source': db_source,
        'primary_key': primary_key,
        'unique_key': f"{fields['licenseno']}_{fields['name']}_{fields['fathername']}".lower().strip()
    })
    return fields

def sort_key(result):
    licenseno = result['licenseno'] or ''
    db_priority = 0 if result['db_source'] == 'New Database' else 1
    return (licenseno.lower(), db_priority)

def deduplicate_results(results):
    unique_results = []
    seen_keys = set()
    for result in results:
        unique_key = result['unique_key']
        db_source = result['db_source']
        db_specific_key = f"{unique_key}_{db_source}"
        if unique_key and db_specific_key not in seen_keys:
            seen_keys.add(db_specific_key)
            unique_results.append(result)
        elif not unique_key:
            unique_results.append(result)
    unique_results.sort(key=sort_key)
    for result in unique_results:
        result.pop('unique_key', None)
    return unique_results

def paginate_results(request, results):
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

def get_search_params(request):
    return {
        k: request.GET.get(k, '').strip()
        for k in ['licenseno', 'cnic', 'name', 'fathername', 'dob', 'address']
    }

def get_search_models():
    return [
        ('License', License, 'New Database'),
        ('OldLicense', OldLicense, 'Old Database'),
    ]

def get_db_counts(results):
    return {
        'new_database': sum(1 for r in results if r['db_source'] == 'New Database'),
        'old_database': sum(1 for r in results if r['db_source'] == 'Old Database')
    }

def get_search_context(page_obj, total_results, search_params, has_search, db_counts):
    return {
        'results': page_obj,
        'total_results': total_results,
        'search_params': search_params,
        'has_search': has_search,
        'db_counts': db_counts
    }

def get_empty_search_context(search_params):
    return {
        'results': [],
        'total_results': 0,
        'search_params': search_params,
        'has_search': False
    }

def add_search_message(total_results):
    if total_results == 0:
        messages.info(messages.get_request(), 'No results found for your search criteria.')
    else:
        messages.success(messages.get_request(), f'Found {total_results} matching records from both databases.')

@login_required
def search_view(request):
    search_params = get_search_params(request)
    has_search = any(search_params.values())
    results = []
    search_models = get_search_models()
    if has_search:
        for model_name, model, db_source in search_models:
            try:
                q = build_search_query(model, search_params)
                if q.children:
                    queryset = model.objects.filter(q).distinct()
                    for obj in queryset:
                        result = prepare_result_object(obj, model_name, db_source)
                        if result:
                            results.append(result)
            except Exception as e:
                logger.error(f"Error searching {model_name}: {str(e)}")
                continue
        results = deduplicate_results(results)
        db_counts = get_db_counts(results)
        page_obj = paginate_results(request, results)
        total_results = len(results)
        if total_results == 0:
            messages.info(request, 'No results found for your search criteria.')
        else:
            messages.success(request, f'Found {total_results} matching records from both databases.')
        context = get_search_context(page_obj, total_results, search_params, has_search, db_counts)
    else:
        context = get_empty_search_context(search_params)
    return render(request, 'licenses/search.html', context)

def get_model_from_name(model_name):
    try:
        return apps.get_model('licenses', model_name)
    except LookupError:
        logger.error(f"Model '{model_name}' not found in licenses app")
        raise Http404("Model not found")

def get_pk_field(model):
    field_names = [f.name for f in model._meta.get_fields()]
    if 'serialno' in field_names:
        return 'serialno'
    elif not getattr(model._meta, 'managed', True) and 'id' in field_names:
        return 'id'
    else:
        return model._meta.pk.name if model._meta.pk else None

def get_object_by_pk(model, pk_field, pk, model_name):
    try:
        logger.info(f"Attempting to fetch {model_name} with {pk_field}={pk}")
        obj = model.objects.get(**{pk_field: pk})
        logger.info(f"Successfully fetched {model_name} object: {obj}")
        return obj
    except model.DoesNotExist:
        logger.error(f"{model_name} object with {pk_field}={pk} not found")
        raise Http404("Record not found")
    except Exception as e:
        logger.error(f"Error fetching {model_name} object with {pk_field}={pk}: {str(e)}")
        raise Http404(f"Error retrieving record: {str(e)}")

def get_model_fields(model):
    try:
        return [
            f for f in model._meta.get_fields()
            if f.concrete and not f.auto_created and hasattr(f, 'name')
        ]
    except Exception as e:
        logger.error(f"Error getting fields for {model.__name__}: {str(e)}")
        try:
            return [f for f in model._meta.fields if hasattr(f, 'name')]
        except:
            return []

def get_endo_related(obj):
    related_qs = Endo.objects.filter(licenseno=obj.licenseno)
    related_data = {'Endo': related_qs}
    try:
        endo_model = related_qs.model
        related_fields = {
            'Endo': [
                f for f in endo_model._meta.get_fields()
                if getattr(f, 'concrete', False)
                and not getattr(f, 'auto_created', False)
                and hasattr(f, 'name')
                and f.name != 'computerno'
            ]
        }
    except Exception:
        related_fields = {'Endo': []}
    return related_data, related_fields

def get_license_related(obj):
    related_data = {}
    related_fields = {}
    license_no = getattr(obj, 'licenseno', None)
    computer_no = getattr(obj, 'computerno', None)
    if license_no:
        try:
            license_vehicles = Licensevehicle.objects.filter(licenseno=license_no)
            related_data['LicenseVehicle'] = list(license_vehicles)
            related_fields['LicenseVehicle'] = [
                f for f in Licensevehicle._meta.get_fields()
                if f.concrete and not f.auto_created and hasattr(f, 'name')
            ]
        except Exception as e:
            logger.error(f"Error fetching LicenseVehicle data: {str(e)}")
            related_data['LicenseVehicle'] = []
            related_fields['LicenseVehicle'] = []
    if computer_no:
        try:
            license_updations = Licenseupdation.objects.filter(computerno=computer_no)
            related_data['LicenseUpdation'] = list(license_updations)
            related_fields['LicenseUpdation'] = [
                f for f in Licenseupdation._meta.get_fields()
                if f.concrete and not f.auto_created
            ]
        except Exception as e:
            logger.error(f"Error fetching LicenseUpdation data: {str(e)}")
            related_data['LicenseUpdation'] = []
            related_fields['LicenseUpdation'] = []
    try:
        endorse_numbers = Endorsenumber.objects.all()[:10]
        related_data['EndorseNumber'] = list(endorse_numbers)
        related_fields['EndorseNumber'] = [
            f for f in Endorsenumber._meta.get_fields()
            if f.concrete and not f.auto_created and hasattr(f, 'name')
        ]
    except Exception as e:
        logger.error(f"Error fetching EndorseNumber data: {str(e)}")
        related_data['EndorseNumber'] = []
        related_fields['EndorseNumber'] = []
    try:
        updation_types = Updationtype.objects.all()[:10]
        related_data['UpdationType'] = list(updation_types)
        related_fields['UpdationType'] = [
            f for f in Updationtype._meta.get_fields()
            if f.concrete and not f.auto_created and hasattr(f, 'name')
        ]
    except Exception as e:
        logger.error(f"Error fetching UpdationType data: {str(e)}")
        related_data['UpdationType'] = []
        related_fields['UpdationType'] = []
    try:
        vehicle_types = Vehicletype.objects.all()[:10]
        related_data['VehicleType'] = list(vehicle_types)
        related_fields['VehicleType'] = [
            f for f in Vehicletype._meta.get_fields()
            if f.concrete and not f.auto_created and hasattr(f, 'name')
        ]
    except Exception as e:
        logger.error(f"Error fetching VehicleType data: {str(e)}")
        related_data['VehicleType'] = []
        related_fields['VehicleType'] = []
    for key in ['LicenseVehicle', 'LicenseUpdation', 'EndorseNumber', 'UpdationType', 'VehicleType']:
        if key not in related_data:
            related_data[key] = []
            related_fields[key] = []
    return related_data, related_fields

def get_related_data_and_fields(model_name, obj):
    if model_name == "OldLicense":
        return get_endo_related(obj)
    elif model_name == "License":
        return get_license_related(obj)
    else:
        return {}, {}

def get_license_detail_context(record, fields, model_name, related_data, related_fields):
    return {
        'record': record,
        'fields': fields,
        'model_name': model_name,
        'related_data': related_data,
        'related_fields': related_fields,
    }

@login_required
def license_detail_view(request, model_name, pk):
    model = get_model_from_name(model_name)
    pk_field = get_pk_field(model)
    if pk_field is None:
        logger.error(f"No valid primary key field found for model '{model_name}'")
        raise Http404("Primary key not found for this model")
    obj = get_object_by_pk(model, pk_field, pk, model_name)
    record = obj
    fields = get_model_fields(model)
    related_data, related_fields = get_related_data_and_fields(model_name, obj)
    context = get_license_detail_context(record, fields, model_name, related_data, related_fields)
    return render(request, 'licenses/license_detail.html', context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('licenses:login')
    return render(request, "registration/logout.html")

def get_login_credentials(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    return username, password

def authenticate_and_login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return True, user
    return False, None

def login_view(request):
    if request.user.is_authenticated:
        return redirect("licenses:search")
    if request.method == "POST":
        username, password = get_login_credentials(request)
        success, user = authenticate_and_login(request, username, password)
        if success:
            return redirect("licenses:search")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "registration/login.html")
