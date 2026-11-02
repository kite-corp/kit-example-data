-- Kettle & Crumb (cafe) and Seabrook Family Dental (clinic). Invented data only.

CREATE SCHEMA IF NOT EXISTS cafe;
CREATE SCHEMA IF NOT EXISTS clinic;

CREATE TABLE cafe.menu_items (
    id text PRIMARY KEY,
    name text NOT NULL,
    category text NOT NULL,
    price_cents integer NOT NULL CHECK (price_cents >= 0),
    vegan boolean NOT NULL DEFAULT false,
    gluten_free boolean NOT NULL DEFAULT false,
    CHECK (category IN ('coffee', 'tea', 'breakfast', 'lunch', 'bakery'))
);

CREATE TABLE cafe.stock (
    item_id text NOT NULL REFERENCES cafe.menu_items (id),
    day date NOT NULL,
    left_count integer NOT NULL CHECK (left_count >= 0),
    PRIMARY KEY (item_id, day)
);

CREATE TABLE cafe.loyalty_cards (
    member_id text PRIMARY KEY,
    stamps integer NOT NULL CHECK (stamps >= 0)
);

CREATE TABLE cafe.orders (
    id text PRIMARY KEY,
    member_id text NOT NULL,
    status text NOT NULL,
    placed_at timestamptz NOT NULL,
    total_cents integer NOT NULL CHECK (total_cents >= 0),
    CHECK (status IN ('received', 'being_made', 'ready', 'collected', 'cancelled'))
);

CREATE TABLE cafe.order_items (
    order_id text NOT NULL REFERENCES cafe.orders (id),
    line integer NOT NULL CHECK (line >= 1),
    item_id text NOT NULL REFERENCES cafe.menu_items (id),
    milk text,
    size text NOT NULL DEFAULT 'regular',
    qty integer NOT NULL CHECK (qty >= 1),
    price_cents integer NOT NULL CHECK (price_cents >= 0),
    PRIMARY KEY (order_id, line),
    CHECK (size IN ('regular', 'large'))
);

CREATE TABLE clinic.dentists (
    id text PRIMARY KEY,
    name text NOT NULL,
    role text NOT NULL,
    CHECK (role IN ('dentist', 'hygienist'))
);

CREATE TABLE clinic.treatments (
    id text PRIMARY KEY,
    name text NOT NULL,
    price_cents integer NOT NULL CHECK (price_cents >= 0),
    from_price boolean NOT NULL DEFAULT false,
    minutes integer NOT NULL CHECK (minutes > 0)
);

CREATE TABLE clinic.patients (
    id text PRIMARY KEY,
    name text NOT NULL,
    phone text NOT NULL
);

CREATE TABLE clinic.slots (
    id text PRIMARY KEY,
    starts_at timestamptz NOT NULL,
    minutes integer NOT NULL CHECK (minutes > 0),
    chair text NOT NULL,
    dentist_id text NOT NULL REFERENCES clinic.dentists (id),
    free boolean NOT NULL DEFAULT true
);

CREATE TABLE clinic.appointments (
    id text PRIMARY KEY,
    slot_id text NOT NULL REFERENCES clinic.slots (id),
    patient_id text NOT NULL REFERENCES clinic.patients (id),
    treatment_id text NOT NULL REFERENCES clinic.treatments (id),
    state text NOT NULL,
    CHECK (state IN ('booked', 'cancelled', 'done'))
);
