import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { handleRequest, reloadFromFile } from "../api/server.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const showcase = JSON.parse(
  fs.readFileSync(path.join(here, "..", "data", "showcase.json"), "utf8"),
);

function mockReq(method, url, { headers = {}, body } = {}) {
  const chunks = body === undefined ? [] : [typeof body === "string" ? body : JSON.stringify(body)];
  return {
    method,
    url,
    headers,
    [Symbol.asyncIterator]: async function* () {
      for (const c of chunks) yield Buffer.from(c);
    },
  };
}

async function call(method, url, opts = {}) {
  let status;
  let headers = {};
  const chunks = [];
  const res = {
    writeHead(code, h = {}) {
      status = code;
      headers = h;
    },
    end(data) {
      if (data) chunks.push(data);
    },
  };
  await handleRequest(mockReq(method, url, opts), res);
  const text = chunks.length
    ? chunks.map((c) => (typeof c === "string" ? c : c.toString("utf8"))).join("")
    : "";
  let json;
  try {
    json = text ? JSON.parse(text) : undefined;
  } catch {
    json = text;
  }
  return { status, headers, json, text };
}

test.beforeEach(() => {
  reloadFromFile();
});

test("showcase GET routes return showcase rows", async () => {
  const cases = [
    ["/v1/orders/K-2041", showcase.orders["K-2041"]],
    ["/v1/stock/bakery", showcase.stock.bakery],
    ["/v1/slots/monday", showcase.slots.monday],
    ["/v1/slots/sunday", []],
    ["/v1/bookings/B-3107", showcase.bookings["B-3107"]],
    ["/v1/loyalty/M-1182", showcase.loyalty["M-1182"]],
    ["/v1/orders/K-2041/eta", showcase.track["K-2041"].eta],
    ["/v1/orders/K-2041/track", showcase.track["K-2041"].track],
    ["/v1/orders/K-2041/pass", showcase.track["K-2041"].pass],
    ["/v1/members/M-1182/notifications", showcase.notifications["M-1182"]],
    ["/v1/sales/2026-11-01/revenue", showcase.sales["2026-11-01"].revenue],
    [
      "/v1/calendar/2026-11",
      { month: "2026-11", ...showcase.calendar["2026-11"] },
    ],
    ["/v1/times/2026-11-05", showcase.times["2026-11-05"]],
    ["/v1/bookings/B-3107/status", showcase.visits["B-3107"].status],
    ["/v1/bookings/B-3107/pass", showcase.visits["B-3107"].pass],
    [
      "/v1/clinic/2026-W45/today",
      showcase.clinic["2026-W45"].today,
    ],
    ["/v1/invoices/INV-5521", showcase.invoices["INV-5521"].invoice],
    ["/v1/invoices/INV-5521/claim", showcase.invoices["INV-5521"].claim],
  ];
  for (const [url, expected] of cases) {
    const { status, json } = await call("GET", url);
    assert.equal(status, 200, url);
    assert.deepEqual(json, expected, url);
    assert.equal(
      (await call("GET", url)).headers["access-control-allow-origin"],
      "*",
      url,
    );
  }
});

test("unknown id returns 404", async () => {
  const { status } = await call("GET", "/v1/orders/K-9999");
  assert.equal(status, 404);
});

test("__proto__ id returns 404", async () => {
  const { status } = await call("GET", "/v1/orders/__proto__");
  assert.equal(status, 404);
});

test("POST order 201 then GET", async () => {
  const { status, json } = await call("POST", "/v1/orders", {
    headers: { "content-type": "application/json" },
    body: { member_id: "M-1182", items: [{ name: "Flat white", milk: "oat" }] },
  });
  assert.equal(status, 201);
  assert.match(json.Order, /^K-2044$/);
  // Flat white $4.20 + oat milk 60 cents (data/kettle-and-crumb.md)
  assert.equal(json.Total, "$4.80");
  const got = await call("GET", `/v1/orders/${json.Order}`);
  assert.equal(got.status, 200);
  assert.equal(got.json.Order, json.Order);
});

test("booking a taken slot returns 409", async () => {
  const { status } = await call("POST", "/v1/bookings", {
    headers: { "content-type": "application/json" },
    body: {
      day: "thursday",
      time: "11:00 am",
      treatment: "Checkup and clean",
      patient_name: "Test Patient",
    },
  });
  assert.equal(status, 409);
});

test("POST /reset without env returns 404", async () => {
  const prev = process.env.KITEXAMPLE_RESET_TOKEN;
  delete process.env.KITEXAMPLE_RESET_TOKEN;
  try {
    const { status } = await call("POST", "/reset", {
      headers: { "x-reset-token": "anything" },
      body: {},
    });
    assert.equal(status, 404);
  } finally {
    if (prev !== undefined) process.env.KITEXAMPLE_RESET_TOKEN = prev;
  }
});

test("POST /reset wrong token returns 403", async () => {
  process.env.KITEXAMPLE_RESET_TOKEN = "test-reset-token";
  try {
    const { status } = await call("POST", "/reset", {
      headers: { "x-reset-token": "wrong" },
      body: {},
    });
    assert.equal(status, 403);
  } finally {
    delete process.env.KITEXAMPLE_RESET_TOKEN;
  }
});

test("body over 16 KB returns 413", async () => {
  const big = "x".repeat(16 * 1024 + 1);
  const { status } = await call("POST", "/v1/orders", {
    headers: { "content-type": "application/json" },
    body: big,
  });
  assert.equal(status, 413);
});

test("order total adds large and plant milk per item", async () => {
  const { json } = await call("POST", "/v1/orders", {
    headers: { "content-type": "application/json" },
    body: { member_id: "M-1182", items: [{ name: "Latte", size: "large", milk: "soy" }, { name: "Banana bread" }] },
  });
  // Latte $4.50 + large 80c + soy 60c + banana bread $4.00
  assert.equal(json.Total, "$9.90");
});

test("a booking takes its price from the treatment; an unknown treatment is 400", async () => {
  const ok = await call("POST", "/v1/bookings", {
    headers: { "content-type": "application/json" },
    body: { day: "monday", time: "1:00 pm", treatment: "Teeth whitening", patient_name: "Test Patient" },
  });
  assert.equal(ok.status, 201);
  assert.equal(ok.json.Price, "$490");
  const bad = await call("POST", "/v1/bookings", {
    headers: { "content-type": "application/json" },
    body: { day: "monday", time: "4:30 pm", treatment: "toString", patient_name: "Test Patient" },
  });
  assert.equal(bad.status, 400);
});

test("a body that is not JSON is 400", async () => {
  const { status } = await call("POST", "/v1/orders", { body: "{not json" });
  assert.equal(status, 400);
});
