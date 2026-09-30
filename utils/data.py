# TravelGo: Transport and Hotel Inventory Dataset
# utils/data.py - Custom transport and hotel data required by Epic 1

BUSES = [
    {
        "id": "BUS-01",
        "travel_mode": "bus",
        "provider_name": "Orange Travels",
        "origin": "Hyderabad",
        "destination": "Bangalore",
        "departure_time": "09:00 PM",
        "arrival_time": "06:30 AM",
        "total_amount": 1250,
        "base_price": 1250,
        "category": "Volvo Multi-Axle A/C Sleeper",
        "rating": 4.8,
        "available_seats": 28,
        "image": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600"
    },
    {
        "id": "BUS-02",
        "travel_mode": "bus",
        "provider_name": "KSRTC Airavat",
        "origin": "Bangalore",
        "destination": "Goa",
        "departure_time": "10:30 PM",
        "arrival_time": "08:00 AM",
        "total_amount": 950,
        "base_price": 950,
        "category": "Club Class A/C Semi-Sleeper",
        "rating": 4.6,
        "available_seats": 16,
        "image": "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=600"
    },
    {
        "id": "BUS-03",
        "travel_mode": "bus",
        "provider_name": "SRS Travels",
        "origin": "Mumbai",
        "destination": "Pune",
        "departure_time": "07:00 AM",
        "arrival_time": "11:00 AM",
        "total_amount": 450,
        "base_price": 450,
        "category": "Express Luxury AC",
        "rating": 4.4,
        "available_seats": 32,
        "image": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600"
    }
]

TRAINS = [
    {
        "id": "TRN-01",
        "travel_mode": "train",
        "provider_name": "Vande Bharat Express (20608)",
        "origin": "Chennai",
        "destination": "Mysore",
        "departure_time": "05:50 AM",
        "arrival_time": "12:20 PM",
        "total_amount": 1365,
        "base_price": 1365,
        "category": "Chair Car (CC) / Executive",
        "rating": 4.9,
        "available_seats": 42,
        "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=600"
    },
    {
        "id": "TRN-02",
        "travel_mode": "train",
        "provider_name": "Rajdhani Express (12433)",
        "origin": "Delhi",
        "destination": "Mumbai",
        "departure_time": "04:55 PM",
        "arrival_time": "08:35 AM",
        "total_amount": 2890,
        "base_price": 2890,
        "category": "3-Tier AC / 2-Tier AC",
        "rating": 4.7,
        "available_seats": 18,
        "image": "https://images.unsplash.com/photo-1532105956626-9569c03602f6?w=600"
    }
]

FLIGHTS = [
    {
        "id": "FLT-01",
        "travel_mode": "flight",
        "provider_name": "IndiGo (6E-512)",
        "origin": "Mumbai",
        "destination": "Goa",
        "departure_time": "11:15 AM",
        "arrival_time": "12:30 PM",
        "total_amount": 3499,
        "base_price": 3499,
        "category": "Non-Stop Economy",
        "rating": 4.5,
        "available_seats": 9,
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=600"
    },
    {
        "id": "FLT-02",
        "travel_mode": "flight",
        "provider_name": "Air India (AI-804)",
        "origin": "Delhi",
        "destination": "Bangalore",
        "departure_time": "06:30 PM",
        "arrival_time": "09:15 PM",
        "total_amount": 5190,
        "base_price": 5190,
        "category": "Economy with Meal Included",
        "rating": 4.3,
        "available_seats": 14,
        "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=600"
    }
]

HOTELS = [
    {
        "id": "HTL-01",
        "travel_mode": "hotel",
        "provider_name": "Taj Lake Palace & Resorts",
        "origin": "Udaipur",
        "destination": "Udaipur",
        "departure_time": "Check-in: 02:00 PM",
        "arrival_time": "Check-out: 11:00 AM",
        "total_amount": 8500,
        "base_price": 8500,
        "category": "luxury",
        "rating": 4.9,
        "available_seats": 5,
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600"
    },
    {
        "id": "HTL-02",
        "travel_mode": "hotel",
        "provider_name": "The Leela Palace",
        "origin": "Bangalore",
        "destination": "Bangalore",
        "departure_time": "Check-in: 02:00 PM",
        "arrival_time": "Check-out: 12:00 PM",
        "total_amount": 6200,
        "base_price": 6200,
        "category": "luxury",
        "rating": 4.8,
        "available_seats": 7,
        "image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=600"
    },
    {
        "id": "HTL-03",
        "travel_mode": "hotel",
        "provider_name": "Ginger Hotel Central",
        "origin": "Hyderabad",
        "destination": "Hyderabad",
        "departure_time": "Check-in: 12:00 PM",
        "arrival_time": "Check-out: 11:00 AM",
        "total_amount": 2100,
        "base_price": 2100,
        "category": "budget",
        "rating": 4.2,
        "available_seats": 22,
        "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600"
    },
    {
        "id": "HTL-04",
        "travel_mode": "hotel",
        "provider_name": "Zostel Heritage",
        "origin": "Jaipur",
        "destination": "Jaipur",
        "departure_time": "Check-in: 01:00 PM",
        "arrival_time": "Check-out: 10:30 AM",
        "total_amount": 899,
        "base_price": 899,
        "category": "budget",
        "rating": 4.5,
        "available_seats": 15,
        "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=600"
    }
]

# Combined Unified Catalog
TRAVEL_CATALOG = BUSES + TRAINS + FLIGHTS + HOTELS
