from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from adrf import mixins as amixins

from library_service.models.library_settings import LibrarySettings
from library_service.serializers.library_settings import LibrarySettingsSerializer

import requests
from datetime import datetime, timedelta

class LibrarySettingsViewSet(amixins.ListModelMixin, AsyncGenericViewSet):
    serializer_class = LibrarySettingsSerializer
    queryset = LibrarySettings.objects.all()

    async def aget_object(self):
        return await LibrarySettings.aget_settings()

    async def alist(self, *args, **kwargs):
        current_year = datetime.now().year

        settings: LibrarySettings = await self.aget_object()

        if len(settings.holidays) > 0 and int(settings.holidays[len(settings.holidays) -1][:4]) == current_year:
            settings.holidays += self.get_holidays(current_year+1)
        elif len(settings.holidays) == 0:
            settings.holidays = self.get_holidays(current_year) + self.get_holidays(current_year+1)
        await settings.asave()
        serializer = self.get_serializer(settings)
        return Response(await serializer.adata)
    
    def get_holidays(self, year):
        url = f"https://isdayoff.ru/api/getdata?year={year}&country=ru"
        response = requests.get(url)
        
        if response.status_code == 200:
            days = response.text
            holidays = []
            start_date = datetime(year, 1, 1)
            
            for i, day_status in enumerate(days):
                current_date = start_date + timedelta(days=i)
                if day_status in ['1'] and current_date.weekday() != 5:  
                    holidays.append(current_date.strftime('%Y-%m-%d'))
            
            return holidays
        else:
            return None
    
    async def aupdate(self, request, *args, **kwargs):
        return await super().aupdate(request, *args, **kwargs)

    @action(detail=False, url_path="update", methods=["put"], permission_classes=[IsAuthenticated])
    async def update_settings(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(await self.aget_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        await serializer.asave()

        return await self.alist(*args, **kwargs)
