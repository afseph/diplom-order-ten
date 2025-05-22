from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Asset, AssetType, Location, AssetLog
from .forms import AssetForm

@login_required
def dashboard(request):
    # Get statistics
    total_assets = Asset.objects.count()
    assets_by_status = Asset.objects.values('status').annotate(count=Count('id'))
    assets_by_type = Asset.objects.values('type__name').annotate(count=Count('id'))
    
    context = {
        'total_assets': total_assets,
        'assets_by_status': assets_by_status,
        'assets_by_type': assets_by_type,
    }
    return render(request, 'assets/dashboard.html', context)

@login_required
def asset_list(request):
    assets = Asset.objects.all()
    
    # Filters
    status = request.GET.get('status')
    type_id = request.GET.get('type')
    location_id = request.GET.get('location')
    
    if status:
        assets = assets.filter(status=status)
    if type_id:
        assets = assets.filter(type_id=type_id)
    if location_id:
        assets = assets.filter(location_id=location_id)
    
    context = {
        'assets': assets,
        'types': AssetType.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'assets/asset_list.html', context)

@login_required
def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    return render(request, 'assets/asset_detail.html', {'asset': asset})

@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.responsible = request.user
            asset.save()
            # Create log entry
            AssetLog.objects.create(
                asset=asset,
                action='Создание актива',
                user=request.user,
                details=f'Актив {asset.name} ({asset.serial_number}) создан'
            )
            messages.success(request, 'Актив успешно создан')
            return redirect('assets:asset_detail', pk=asset.pk)
    else:
        form = AssetForm()
    return render(request, 'assets/asset_form.html', {'form': form})

@login_required
def asset_update(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            # Create log entry
            AssetLog.objects.create(
                asset=asset,
                action='Обновление актива',
                user=request.user,
                details=f'Актив {asset.name} ({asset.serial_number}) обновлен'
            )
            messages.success(request, 'Актив успешно обновлен')
            return redirect('assets:asset_detail', pk=asset.pk)
    else:
        form = AssetForm(instance=asset)
    return render(request, 'assets/asset_form.html', {'form': form})

@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        # Create log entry before deletion
        AssetLog.objects.create(
            asset=asset,
            action='Удаление актива',
            user=request.user,
            details=f'Актив {asset.name} ({asset.serial_number}) удален'
        )
        asset.delete()
        messages.success(request, 'Актив успешно удален')
        return redirect('assets:asset_list')
    return render(request, 'assets/asset_confirm_delete.html', {'asset': asset})
