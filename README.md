# Train Reservation API

### Overview

A Train Reservation API will be developed to determine whether a reservation can be made for a given train, and if it is possible, to specify which wagon(s) the reservation can be placed in.

The API will respond to HTTP POST requests.

The API will receive the train details and the number of people for the reservation. The algorithm will return whether the reservation can be made and, if so, which wagons can accommodate the requested reservation.


### Requirements

 - A train may have multiple wagons.

 - Each wagon can have a different seating capacity.

 - The occupancy of a wagon should not exceed 70%. For example, if the capacity of a wagon is 100 and 70 seats are occupied, no reservations can be made in that wagon.

 - A reservation request may include multiple people.
 - The request will indicate whether the people can be placed in different wagons. Some requests will require all passengers to be in the same wagon, while others allow passengers to be distributed across different wagons.

 - If a reservation can be made, the API will return details of how many people can be placed in each wagon.


### API Request Format

The request will include the train's details, wagon details, the number of people for the reservation, and whether the passengers can be placed in different wagons. The input format will be as follows:

```json 
{
    "train": {
        "name": "Python Ekspres",
        "wagons": [
            {"name": "Vagon 1", "capacity": 100, "occupied_seats": 50},
            {"name": "Vagon 2", "capacity": 90, "occupied_seats": 80},
            {"name": "Vagon 3", "capacity": 80, "occupied_seats": 80},
            {"name": "Vagon 4", "capacity": 80, "occupied_seats": 52}
        ]
    },
    "num_of_people": 4,
    "allow_different_wagons": true
}
```

### API Response Format

If the reservation can be made, the response will indicate whether the reservation is possible and provide details on how the people will be placed in the wagons. The response will be in the following format:

```json 
{
    "ReservationPossible": true,
    "PlacementDetails": [
        {"WagonName": "Vagon 1", "PeopleCount": 2},
        {"WagonName": "Vagon 2", "PeopleCount": 1}
    ]
}
```

If the reservation cannot be made, the PlacementDetails array will be empty:

```json 
{
    "ReservationPossible": false,
    "PlacementDetails": []
}
```
