from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorDetailSerializer, SensorSerializer, \
    MeasurementSerializer


class SensorView(ListAPIView):
    # 4. Получить список датчиков. Выдаётся список с краткой информацией по
    # датчикам: ID, название и описание.
    # GET {{baseUrl}}/sensors/ Content-Type: application/json
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    # 1. Создать датчик. Указываются название и описание датчика.
    # POST {{baseUrl}}/sensors/ Content-Type: application/json
    def post(self, request):

        sensor_name = request.data.get('name')
        if sensor_name:
            sensors = Sensor.objects.filter(name=sensor_name)
            if sensors:
                status = 200
                return_data = {'msg': 'Object with same name already exist. '
                                      f'ID: {sensors[0].id}'}
            else:
                status = 201
                return_data = {
                    'sensor_id': self.new_sensor(sensor_name,
                                                 request.data.get(
                                                     'description'))}
        else:
            status = 400
            return_data = {'msg': 'Required parameters are not filled'}

        return Response(data=return_data, status=status)

    def new_sensor(self, name, description):
        new_sensor = Sensor.objects.create()
        new_sensor.name = name
        new_sensor.description = description
        new_sensor.save()
        return new_sensor.id


class SensorDetailView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    # 5. Получить информацию по конкретному датчику.
    # Выдаётся полная информация по
    # датчику: ID, название, описание и список всех измерений
    # с температурой и временем.
    # GET {{baseUrl}}/sensors/1/ Content-Type: application/json
    def get(self, request, id):
        sensor = Sensor.objects.get(pk=id)
        return_data = SensorDetailSerializer(sensor).data
        status = 200
        return Response(data=return_data, status=status)

    # 2. Изменить датчик. Указываются название и описание.
    # PATCH {{baseUrl}}/sensors/1/ Content-Type: application/json
    def patch(self, request, id):
        sensor = Sensor.objects.get(pk=id)
        for key, value in request.data.items():
            if key == 'name':
                sensor.name = value
            elif key == 'description':
                sensor.description = value
        sensor.save()
        status = 200
        return_data = {'msg': 'Item updated'}
        return Response(data=return_data, status=status)


class MeasurementView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    # 3. Добавить измерение. Указываются ID датчика и температура.
    # POST {{baseUrl}}/measurements/ Content-Type: application/json
    def post(self, request):
        new_measurement = Measurement.objects.create(
            sensor_id=request.data.get('sensor'),
            temperature=request.data.get('temperature'))
        new_measurement.save()
        status = 200
        return_data = {'msg': 'Item created'}
        return Response(data=return_data, status=status)
