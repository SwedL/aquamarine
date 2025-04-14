from carwash.models import CarWashRequestCall


def request_call_processing(call_id: int) -> None:
    processed_call = CarWashRequestCall.objects.get(id=call_id)
    processed_call.processed = True
    processed_call.save()
