// Sample REST API for kit-example-data (Node built-ins, data/showcase.json).
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const DATA_PATH = path.join(here, "..", "data", "showcase.json");
const BODY_LIMIT = 16 * 1024;

const MENU = {
  coffee: [
    { name: "Espresso", price: "$3.00" },
    { name: "Americano", price: "$3.50" },
    { name: "Flat white", price: "$4.20" },
    { name: "Cappuccino", price: "$4.20" },
    { name: "Latte", price: "$4.50" },
    { name: "Mocha", price: "$4.90" },
  ],
  tea: [
    { name: "English breakfast tea", price: "$3.20" },
    { name: "Earl grey tea", price: "$3.20" },
    { name: "Chai", price: "$4.40" },
    { name: "Matcha", price: "$4.80" },
    { name: "Hot chocolate", price: "$4.20" },
  ],
  breakfast: [
    { name: "Sourdough toast with butter", price: "$5.50" },
    { name: "Avocado toast", price: "$11.00" },
    { name: "Bacon and egg roll", price: "$9.50" },
    { name: "Granola bowl", price: "$8.50" },
  ],
  lunch: [
    { name: "Chicken and pesto toastie", price: "$12.50" },
    { name: "Roast pumpkin salad", price: "$13.00" },
    { name: "Soup of the day with bread", price: "$10.50" },
  ],
  bakery: [
    { name: "Butter croissant", price: "$3.80" },
    { name: "Almond croissant", price: "$4.60" },
    { name: "Cinnamon bun", price: "$4.20" },
    { name: "Banana bread", price: "$4.00" },
  ],
};

const menuNames = new Set(
  Object.values(MENU)
    .flat()
    .map((item) => item.name.toLowerCase()),
);

const DAY_PREFIX = {
  monday: "Monday",
  tuesday: "Tuesday",
  wednesday: "Wednesday",
  thursday: "Thursday",
  friday: "Friday",
  saturday: "Saturday",
  sunday: "Sunday",
};

let db = loadData();
let nextOrderSeq = maxOrderSeq(db) + 1;
let nextBookingSeq = maxBookingSeq(db) + 1;

function loadData() {
  return JSON.parse(fs.readFileSync(DATA_PATH, "utf8"));
}

function maxOrderSeq(data) {
  let max = 2040;
  for (const id of Object.keys(data.orders || {})) {
    const m = /^K-(\d+)$/.exec(id);
    if (m) max = Math.max(max, Number(m[1]));
  }
  return max;
}

function maxBookingSeq(data) {
  let max = 3100;
  for (const id of Object.keys(data.bookings || {})) {
    const m = /^B-(\d+)$/.exec(id);
    if (m) max = Math.max(max, Number(m[1]));
  }
  return max;
}

export function reloadFromFile() {
  db = loadData();
  nextOrderSeq = maxOrderSeq(db) + 1;
  nextBookingSeq = maxBookingSeq(db) + 1;
}

const own = (table, key) =>
  table && Object.hasOwn(table, key) ? table[key] : undefined;

const getRoutes = [
  [/^\/v1\/orders\/([A-Z]{1,3}-\d{1,6})$/, (id) => own(db.orders, id)],
  [/^\/v1\/stock\/([a-z]+)$/, (category) => own(db.stock, category)],
  [/^\/v1\/slots\/([a-z]+)$/, (day) => (day === "sunday" ? [] : own(db.slots, day))],
  [/^\/v1\/bookings\/([A-Z]{1,3}-\d{1,6})$/, (id) => own(db.bookings, id)],
  [/^\/v1\/loyalty\/(M-\d{1,6})$/, (id) => own(db.loyalty, id)],
  [
    /^\/v1\/orders\/([A-Z]{1,3}-\d{1,6})\/(eta|track|pass)$/,
    (id, part) => own(own(db.track, id) || {}, part),
  ],
  [/^\/v1\/members\/(M-\d{1,6})\/notifications$/, (id) => own(db.notifications, id)],
  [
    /^\/v1\/sales\/(\d{4}-\d{2}-\d{2})\/([a-z_]+)$/,
    (day, part) => own(own(db.sales, day) || {}, part),
  ],
  [
    /^\/v1\/calendar\/(\d{4}-\d{2})$/,
    (month) => (own(db.calendar, month) ? { month, ...db.calendar[month] } : undefined),
  ],
  [/^\/v1\/times\/(\d{4}-\d{2}-\d{2})$/, (date) => own(db.times, date)],
  [
    /^\/v1\/bookings\/([A-Z]{1,3}-\d{1,6})\/(status|pass)$/,
    (id, part) => own(own(db.visits, id) || {}, part),
  ],
  [
    /^\/v1\/clinic\/(\d{4}-W\d{2})\/([a-z_]+)$/,
    (week, part) => own(own(db.clinic, week) || {}, part),
  ],
  [/^\/v1\/invoices\/(INV-\d{1,6})$/, (id) => (own(db.invoices, id) || {}).invoice],
  [/^\/v1\/invoices\/(INV-\d{1,6})\/claim$/, (id) => (own(db.invoices, id) || {}).claim],
  [/^\/v1\/menu$/, () => MENU],
  [/^\/v1\/menu\/([a-z]+)$/, (category) => own(MENU, category)],
];

export function lookup(pathname) {
  for (const [re, get] of getRoutes) {
    const m = re.exec(pathname);
    if (m) return get(...m.slice(1));
  }
  return undefined;
}

function bookingTaken(day, time) {
  const prefix = DAY_PREFIX[day];
  if (!prefix) return false;
  for (const row of Object.values(db.bookings || {})) {
    if (
      typeof row.Day === "string" &&
      row.Day.startsWith(prefix) &&
      row.Time === time
    ) {
      return true;
    }
  }
  return false;
}

function slotFree(day, time) {
  if (day === "sunday") return false;
  const slots = own(db.slots, day);
  if (!Array.isArray(slots)) return false;
  if (!slots.some((s) => s.Time === time)) return false;
  return !bookingTaken(day, time);
}

function removeSlot(day, time) {
  const slots = db.slots[day];
  if (!Array.isArray(slots)) return;
  db.slots[day] = slots.filter((s) => s.Time !== time);
}

function restoreSlot(day, time, chair) {
  if (day === "sunday" || !Object.hasOwn(db.slots, day)) return;
  const slots = db.slots[day];
  if (slots.some((s) => s.Time === time)) return;
  slots.push({ Time: time, Length: "30 min", Chair: chair || "Chair 1" });
  slots.sort((a, b) => a.Time.localeCompare(b.Time));
}

async function readBody(req) {
  const chunks = [];
  let total = 0;
  for await (const chunk of req) {
    total += chunk.length;
    if (total > BODY_LIMIT) {
      const err = new Error("payload too large");
      err.code = "PAYLOAD_TOO_LARGE";
      throw err;
    }
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8");
}

function jsonResponse(res, status, body, extraHeaders = {}) {
  const headers = {
    "content-type": "application/json",
    ...extraHeaders,
  };
  res.writeHead(status, headers);
  res.end(JSON.stringify(body));
}

function parseJson(text) {
  if (!text.trim()) return {};
  try {
    return JSON.parse(text);
  } catch {
    const err = new Error("request body is not valid JSON");
    err.code = "BAD_JSON";
    throw err;
  }
}

function formatOrderItems(items) {
  return items
    .map((it) => {
      let line = it.name;
      if (it.milk) line += ` with ${it.milk} milk`;
      if (it.size === "large") line = `Large ${line.toLowerCase()}`;
      return line;
    })
    .join(", ");
}

function handlePost(pathname, body, req, res) {
  if (pathname === "/reset") {
    const token = process.env.KITEXAMPLE_RESET_TOKEN;
    if (!token) {
      return jsonResponse(res, 404, { error: "not found" });
    }
    const header = req.headers["x-reset-token"];
    if (header !== token) {
      return jsonResponse(res, 403, { error: "forbidden" });
    }
    reloadFromFile();
    return jsonResponse(res, 200, { ok: true });
  }

  if (pathname === "/v1/orders") {
    const memberId = body.member_id;
    const items = body.items;
    if (!memberId || !Array.isArray(items) || items.length === 0) {
      return jsonResponse(res, 400, { error: "member_id and items required" });
    }
    for (const it of items) {
      if (!it?.name || !menuNames.has(String(it.name).toLowerCase())) {
        return jsonResponse(res, 400, { error: "unknown menu item" });
      }
    }
    const id = `K-${nextOrderSeq++}`;
    const order = {
      Order: id,
      Status: "Received",
      Items: formatOrderItems(items),
      Total: "$0.00",
      Placed: "now",
    };
    db.orders[id] = order;
    return jsonResponse(res, 201, order);
  }

  if (pathname === "/v1/bookings") {
    const { day, time, treatment, patient_name: patientName } = body;
    if (!day || !time || !treatment || !patientName) {
      return jsonResponse(res, 400, { error: "day, time, treatment, patient_name required" });
    }
    if (!Object.hasOwn(DAY_PREFIX, day)) {
      return jsonResponse(res, 400, { error: "invalid day" });
    }
    if (!slotFree(day, time)) {
      return jsonResponse(res, 409, { error: "slot not available" });
    }
    const slots = db.slots[day];
    const slot = slots.find((s) => s.Time === time);
    removeSlot(day, time);
    const id = `B-${nextBookingSeq++}`;
    const booking = {
      Booking: id,
      Treatment: treatment,
      Day: `${DAY_PREFIX[day]} (new)`,
      Time: time,
      Chair: slot?.Chair || "Chair 1",
      Price: "$145",
    };
    db.bookings[id] = booking;
    return jsonResponse(res, 201, booking);
  }

  return jsonResponse(res, 404, { error: "not found" });
}

function handleDelete(pathname, res) {
  const m = /^\/v1\/bookings\/([A-Z]{1,3}-\d{1,6})$/.exec(pathname);
  if (!m) return jsonResponse(res, 404, { error: "not found" });
  const id = m[1];
  const booking = own(db.bookings, id);
  if (!booking) return jsonResponse(res, 404, { error: "not found" });
  delete db.bookings[id];
  for (const [day, prefix] of Object.entries(DAY_PREFIX)) {
    if (typeof booking.Day === "string" && booking.Day.startsWith(prefix)) {
      restoreSlot(day, booking.Time, booking.Chair);
      break;
    }
  }
  return jsonResponse(res, 200, { ok: true, cancelled: id });
}

export async function handleRequest(req, res) {
  const url = new URL(req.url, "http://127.0.0.1");
  const pathname = url.pathname;
  const method = req.method || "GET";

  if (method === "GET") {
    const body = lookup(pathname);
    const headers = { "access-control-allow-origin": "*" };
    if (body === undefined) {
      return jsonResponse(res, 404, { error: "not found" }, headers);
    }
    return jsonResponse(res, 200, body, headers);
  }

  if (method === "DELETE") {
    return handleDelete(pathname, res);
  }

  if (method === "POST") {
    let text;
    try {
      text = await readBody(req);
    } catch (e) {
      if (e.code === "PAYLOAD_TOO_LARGE") {
        return jsonResponse(res, 413, { error: "payload too large" });
      }
      throw e;
    }
    let body;
    try {
      body = parseJson(text);
    } catch (e) {
      if (e.code === "BAD_JSON") {
        return jsonResponse(res, 400, { error: e.message });
      }
      throw e;
    }
    return handlePost(pathname, body, req, res);
  }

  return jsonResponse(res, 405, { error: "method not allowed" });
}

const port = Number(process.env.PORT || 18704);
if (port < 18700 || port > 18709) {
  throw new Error("PORT must be between 18700 and 18709");
}

const server = http.createServer((req, res) => {
  handleRequest(req, res).catch(() => {
    if (!res.headersSent) {
      jsonResponse(res, 500, { error: "internal error" });
    }
  });
});

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  server.listen(port, "127.0.0.1", () => {
    console.log(`sample data API on http://127.0.0.1:${port}`);
  });
}

export { server, port, DATA_PATH, getRoutes, MENU };
