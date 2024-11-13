from rest_framework.response import Response
from rest_framework.views import APIView
from myapp.serializers import ReservationSerializer


def available_wagons(wagons):
    """Limit the wagons to those that are less than 70% full."""
    available_ones = []
    for wagon in wagons:
        all_taken = wagon.get('occupied_seats') > (wagon.get('capacity') * 0.7)
        if not all_taken:
            available_ones.append(wagon)
    return available_ones


def total_seats(wagons):
    """Calculate the number of available seats."""
    total = 0
    for wagon in wagons:
        available_seats = wagon.get('capacity') - wagon.get('occupied_seats')
        if available_seats > 0:
            total += available_seats
    return total


def seats_in_wagons(wagons):
    """List the available seats and occupancy status in the wagons."""
    available_wagon_seats = []
    for wagon in wagons:
        available_seats = wagon.get('capacity') - wagon.get('occupied_seats')
        if available_seats > 0:
            available_wagon_seats.append({
                'name': wagon.get("name"),
                'available': available_seats,
                'capacity': wagon.get('capacity'),
                'taken': wagon.get('occupied_seats')
            })
    return available_wagon_seats


def arrange_seats(allow_different_wagons, wagons, num_of_people):
    """ Assign passengers to the appropriate wagons."""
    arranged = []
    remaining_people = num_of_people

    if not allow_different_wagons:
        # If passengers need to be placed in the same wagon.
        for wagon in wagons:
            available_seats = wagon['available']
            if available_seats >= remaining_people and (wagon['taken'] + remaining_people) <= (wagon['capacity'] * 0.7):
                arranged.append({"wagon": wagon['name'], "people": remaining_people})
                remaining_people = 0
                break
        if remaining_people > 0:
            # If we cannot place all passengers in the same wagon.
            arranged = []
    else:
        # If placing passengers in different wagons is allowed.
        for wagon in wagons:
            available_seats = wagon['available']
            if available_seats > 0:
                people_to_place = min(available_seats, remaining_people)
                arranged.append({"wagon": wagon['name'], "people": people_to_place})
                remaining_people -= people_to_place
                if remaining_people == 0:
                    break

    if remaining_people > 0:
        arranged = []

    return arranged


class TrainCapacityView(APIView):

    def post(self, req, *args, **kwargs):
        serializer = ReservationSerializer(data=req.data)

        if serializer.is_valid():
            train_capacity = serializer.validated_data

            wagons = available_wagons(train_capacity.get('train')['wagons'])
            total = total_seats(wagons)

            if total < train_capacity.get('num_of_people'):
                return Response({'reservation_status': False}, status=200)

            seats = seats_in_wagons(wagons)
            arranged = arrange_seats(train_capacity['allow_different_wagons'], seats, train_capacity.get('num_of_people'))

            if arranged:
                return Response({
                    "reservation_status": True,
                    "arrangement_details": arranged
                }, status=200)
            else:
                return Response({'reservation_status': False}, status=200)
        return Response(serializer.errors, status=200)
