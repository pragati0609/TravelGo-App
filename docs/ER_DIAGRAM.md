# TravelGo: Entity Relationship (ER) Diagram & Database Schema Design

> **Epic**: Entity Relationship (ER) Diagram  
> **Task 1**: Entity Relationship (ER) Diagram for TravelGo  
> **Database Engine**: Amazon DynamoDB (NoSQL Key-Value & Document Database)

---

## 1. Executive Summary

**TravelGo** is a cloud-powered, real-time travel booking platform deployed on AWS. The data layer utilizes **Amazon DynamoDB** to provide single-digit millisecond latency, seamless horizontal scalability, and high availability without managing relational database servers.

To support user registration, multi-mode travel search and reservation (Buses, Trains, Flights, and Hotels), and personal travel history retrieval, the database schema is partitioned into two primary core tables along with an inventory catalog table:
1. **`TravelGo_Users`**: User registration, profile details, and authentication credentials.
2. **`TravelGo_Bookings`**: Booking records across all transportation and accommodation modes with status tracking (`CONFIRMED`, `CANCELLED`).
3. **`TravelGo_Listings`**: Available travel inventory (routes, schedules, vehicle/room types, pricing, and seat layouts).

---

## 2. Entity Relationship (ER) Diagram

```mermaid
erDiagram
    USERS ||--o{ BOOKINGS : "places (1:N)"
    LISTINGS ||--o{ BOOKINGS : "reserved_in (1:N)"

    USERS {
        string email PK "Partition Key (Unique)"
        string user_id "UUID v4"
        string full_name "User Full Name"
        string phone "Contact Number"
        string password_hash "Werkzeug / Argon2 Hash"
        string role "Role (user / admin)"
        string created_at "ISO-8601 Timestamp"
        string updated_at "ISO-8601 Timestamp"
    }

    BOOKINGS {
        string booking_id PK "Partition Key (UUID v4)"
        string user_email GSI_PK "Global Secondary Index PK"
        string booking_date GSI_SK "Global Secondary Index SK (ISO-8601)"
        string listing_id "Foreign reference to TravelGo_Listings"
        string travel_mode "bus | train | flight | hotel"
        string provider_name "e.g., IndiGo, KSRTC, Taj Residency"
        string origin "Departure City / Source"
        string destination "Arrival City / Destination"
        string departure_time "ISO-8601 or Time String"
        string arrival_time "ISO-8601 or Time String"
        string seat_numbers "Selected Seat IDs (e.g. '12A, 12B')"
        string room_preference "luxury | budget | executive"
        number total_amount "Total cost in INR"
        string currency "INR"
        string booking_status "CONFIRMED | CANCELLED"
        string payment_status "PAID | REFUNDED"
        string sns_message_id "AWS SNS Notification Message ID"
        string created_at "ISO-8601 Timestamp"
        string cancelled_at "Cancellation Timestamp (nullable)"
    }

    LISTINGS {
        string listing_id PK "Partition Key (UUID v4)"
        string travel_mode SK "Sort Key (bus | train | flight | hotel)"
        string provider_name "Operator or Hotel Brand"
        string origin "Source City"
        string destination "Destination City"
        string departure_time "Departure Time"
        string arrival_time "Arrival Time"
        number base_price "Base price per ticket / room"
        string category "budget | luxury | premium"
        number available_seats "Count of unbooked seats / rooms"
        string seat_layout "JSON schema of rows & seat status"
        number rating "Customer Rating (1.0 to 5.0)"
    }
```

---

## 3. Table Schema Specifications (DynamoDB Design)

### Table 1: `TravelGo_Users`
Stores user profile information, authentication credentials, and account metadata.

| Attribute Name | DynamoDB Type | Key Type | Description |
|---|---|---|---|
| `email` | String (`S`) | **Partition Key (PK)** | Unique user email address (login identifier) |
| `user_id` | String (`S`) | Attribute | Unique internal identifier (UUID) |
| `full_name` | String (`S`) | Attribute | Full legal name of user |
| `phone` | String (`S`) | Attribute | Mobile phone number for SMS/Contact |
| `password_hash` | String (`S`) | Attribute | Secure cryptographic hash (PBKDF2/Werkzeug) |
| `role` | String (`S`) | Attribute | User role (`user` or `admin`) |
| `created_at` | String (`S`) | Attribute | Account registration timestamp |
| `updated_at` | String (`S`) | Attribute | Last profile modification timestamp |

---

### Table 2: `TravelGo_Bookings`
Stores transaction records for all confirmed and cancelled bookings across buses, trains, flights, and hotels.

| Attribute Name | DynamoDB Type | Key Type | Description |
|---|---|---|---|
| `booking_id` | String (`S`) | **Partition Key (PK)** | Unique booking identifier (e.g. `BK-8931-ABCD`) |
| `user_email` | String (`S`) | **GSI-1 PK** | Reference to user email (Foreign Key) |
| `created_at` | String (`S`) | **GSI-1 SK** | Creation timestamp for chronological sorting |
| `listing_id` | String (`S`) | Attribute | Reference to the selected listing |
| `travel_mode` | String (`S`) | Attribute | Mode of travel: `bus`, `train`, `flight`, `hotel` |
| `provider_name` | String (`S`) | Attribute | Carrier/Hotel name (e.g. `Orange Travels`, `IndiGo`) |
| `origin` | String (`S`) | Attribute | Source location (e.g. `Hyderabad`) |
| `destination` | String (`S`) | Attribute | Destination location (e.g. `Bangalore`) |
| `travel_date` | String (`S`) | Attribute | Travel or check-in date (`YYYY-MM-DD`) |
| `seat_numbers` | List / String (`S`) | Attribute | Comma-separated seat numbers (e.g. `S1, S2`) |
| `room_preference` | String (`S`) | Attribute | Hotel tier (e.g. `Luxury Suite`, `Budget Standard`) |
| `total_amount` | Number (`N`) | Attribute | Total fare charged (INR) |
| `currency` | String (`S`) | Attribute | Currency code (`INR`) |
| `booking_status` | String (`S`) | Attribute | Current status: `CONFIRMED` or `CANCELLED` |
| `payment_status` | String (`S`) | Attribute | Payment status: `PAID` or `REFUNDED` |
| `sns_message_id` | String (`S`) | Attribute | AWS SNS publish confirmation message ID |
| `cancelled_at` | String (`S`) | Attribute | Timestamp of cancellation (or `null`) |

#### Global Secondary Index (GSI): `UserBookingsIndex`
- **Partition Key**: `user_email` (String)
- **Sort Key**: `created_at` (String)
- **Projection**: `ALL` attributes
- **Purpose**: Enables rapid query: *"Fetch all past and upcoming bookings for a specific user, sorted from newest to oldest"* for the Dynamic User Dashboard (Scenario 3) in `O(1)` query complexity without full-table scans.

---

### Table 3: `TravelGo_Listings` (Inventory Catalog)
Holds transportation schedules and hotel properties searchable by users.

| Attribute Name | DynamoDB Type | Key Type | Description |
|---|---|---|---|
| `listing_id` | String (`S`) | **Partition Key (PK)** | Listing ID (e.g. `BUS-101`, `HTL-504`) |
| `travel_mode` | String (`S`) | Attribute | `bus`, `train`, `flight`, `hotel` |
| `provider_name` | String (`S`) | Attribute | Service operator |
| `origin` | String (`S`) | Attribute | Origin city |
| `destination` | String (`S`) | Attribute | Destination city |
| `departure_time` | String (`S`) | Attribute | Departure / Check-in time |
| `arrival_time` | String (`S`) | Attribute | Arrival / Check-out time |
| `base_price` | Number (`N`) | Attribute | Starting price per passenger / room |
| `category` | String (`S`) | Attribute | Classification: `luxury` or `budget` |
| `available_seats` | Number (`N`) | Attribute | Total remaining seats / rooms |
| `rating` | Number (`N`) | Attribute | Review rating (e.g. `4.8`) |

---

## 4. Cardinality & Relationship Rationales

1. **User to Bookings (1 to Many)**:
   - A registered user can book multiple tickets across different travel modes over time.
   - Handled via `TravelGo_Bookings` GSI `UserBookingsIndex` where `user_email` partitions the query space.
2. **Listings to Bookings (1 to Many)**:
   - A single bus, flight, train, or hotel room inventory listing can receive reservations from multiple distinct users until capacity is exhausted.
3. **NoSQL Access Pattern Optimization**:
   - DynamoDB utilizes hash partitioning on Primary Keys. By using `email` for users and `booking_id` for bookings, write operations distribute uniformly across partitions.
   - Real-time updates (confirmations and cancellations) operate directly on single item key lookups (`GetItem`, `UpdateItem`) with sub-10ms response times.
