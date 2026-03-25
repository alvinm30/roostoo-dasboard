<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Roostoo Trading Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js"></script>
  <style>
    body { background: #0b1020; }
    .card { background: linear-gradient(180deg, #111a34 0%, #0e152a 100%); border: 1px solid #25304f; }
    .tab-btn.active { background: #1e293b; color: #e2e8f0; border-color: #334155; }
    .pill { border: 1px solid #334155; background: #0f172a; }
    .muted { color: #94a3b8; }
    .table-wrap { max-height: 420px; overflow: auto; }
    .mono { font-variant-numeric: tabular-nums; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
  </style>
</head>
<body class="text-slate-100 min-h-screen">
  <div class="max-w-7xl mx-auto p-4 md:p-6 space-y-4">
    <header class="card rounded-2xl p-4 md:p-5 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Roostoo Trading Dashboard</h1>
        <p class="muted text-sm">Live account, orders, and market tracking via Roostoo Mock API</p>
      </div>
      <div class="flex flex-wrap items-center gap-2 text-sm">
        <span class="pill rounded-lg px-3 py-1">Server Time: <span id="serverTime" class="mono">-</span></span>
        <span class="pill rounded-lg px-3 py-1">API: <span id="apiStatus" class="mono text-amber-300">Unknown</span></span>
        <button id="refreshAllBtn" class="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500">Refresh</button>
        <button id="settingsBtn" class="px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600">API Settings</button>
      </div>
    </header>

    <div id="alertBox" class="hidden rounded-xl border border-rose-500/40 bg-rose-950/50 text-rose-200 px-4 py-3 text-sm"></div>

    <nav class="flex gap-2">
      <button class="tab-btn active px-4 py-2 rounded-xl border border-slate-700" data-tab="session1">Session 1</button>
      <button class="tab-btn px-4 py-2 rounded-xl border border-slate-700" data-tab="session2">Session 2</button>
    </nav>

    <section id="session1" class="space-y-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="card rounded-2xl p-4">
          <p class="text-sm muted">BTC</p>
          <p id="pvBTCPrice" class="text-2xl font-semibold mono">$-</p>
          <p id="pvBTCChange" class="mono text-sm mt-1">-%</p>
        </div>
        <div class="card rounded-2xl p-4">
          <p class="text-sm muted">ETH</p>
          <p id="pvETHPrice" class="text-2xl font-semibold mono">$-</p>
          <p id="pvETHChange" class="mono text-sm mt-1">-%</p>
        </div>
        <div class="card rounded-2xl p-4">
          <p class="text-sm muted">SOL</p>
          <p id="pvSOLPrice" class="text-2xl font-semibold mono">$-</p>
          <p id="pvSOLChange" class="mono text-sm mt-1">-%</p>
        </div>
        <div class="card rounded-2xl p-4">
          <p class="text-sm muted">XPR</p>
          <p id="pvXPRPrice" class="text-2xl font-semibold mono">$-</p>
          <p id="pvXPRChange" class="mono text-sm mt-1">-%</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="card rounded-2xl p-4">
          <p class="text-sm muted">Initial Wallet</p>
          <p id="initialWallet" class="text-3xl font-semibold mono">$-</p>
        </div>
        <div class="card rounded-2xl p-4">
          <p class="text-sm muted">Current Portfolio Value + % PNL</p>
          <p id="portfolioValue" class="text-3xl font-semibold mono">$-</p>
          <p id="portfolioPnlPct" class="text-sm mono muted">-%</p>
        </div>
        <div class="card rounded-2xl p-4">
          <p class="text-sm muted">Unrealized PNL Today</p>
          <p id="unrealizedToday" class="text-3xl font-semibold mono">$-</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div class="lg:col-span-2 card rounded-2xl p-4">
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-lg font-semibold">Live Wallet Balances</h2>
            <span id="walletUpdatedAt" class="muted text-xs mono">-</span>
          </div>
          <div class="table-wrap">
            <table class="w-full text-sm">
              <thead class="text-slate-300">
                <tr class="border-b border-slate-700">
                  <th class="text-left py-2">Coin</th>
                  <th class="text-right py-2">Free</th>
                  <th class="text-right py-2">Locked</th>
                  <th class="text-right py-2">USD Value</th>
                  <th class="text-right py-2">Total</th>
                </tr>
              </thead>
              <tbody id="walletTableBody"></tbody>
            </table>
          </div>
        </div>

        <div class="space-y-4">
          <div class="card rounded-2xl p-4">
            <h2 class="text-lg font-semibold mb-3">Quick Market Order</h2>
            <div class="space-y-3">
              <p class="text-xs muted">
                Trading actions are disabled in this web dashboard (market orders not available).
              </p>
              <label class="block text-sm muted">Pair</label>
              <select id="quickPair" disabled class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 opacity-60 cursor-not-allowed"></select>
              <label class="block text-sm muted">Quantity</label>
              <input id="quickQty" disabled type="number" min="0" step="any" placeholder="Enter quantity" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 mono opacity-60 cursor-not-allowed" />
              <div class="grid grid-cols-2 gap-2">
                <button id="buyBtn" disabled class="px-3 py-2 rounded-lg bg-emerald-600 opacity-50 cursor-not-allowed">BUY</button>
                <button id="sellBtn" disabled class="px-3 py-2 rounded-lg bg-rose-600 opacity-50 cursor-not-allowed">SELL</button>
              </div>
            </div>
          </div>
          <div class="card rounded-2xl p-4">
            <h2 class="text-lg font-semibold mb-2">Pending & Trade Stats</h2>
            <p class="text-sm">Pending Orders: <span id="pendingCount" class="mono">-</span></p>
            <p class="text-sm">Total Trades: <span id="totalTrades" class="mono">-</span></p>
            <p class="text-sm">Win Rate: <span id="winRate" class="mono">-</span></p>
            <p class="text-sm">Last Order Created: <span id="lastOrderTime" class="mono">-</span></p>
            <p class="text-sm">Last Filled Finished: <span id="lastFilledTime" class="mono">-</span></p>
          </div>
        </div>
      </div>
    </section>

    <section id="session2" class="hidden space-y-4">
      <div class="card rounded-2xl p-4">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <h2 class="text-lg font-semibold">Live & Historical Trades</h2>
          <div class="flex gap-2">
            <button id="refreshOrdersBtn" class="px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600">Refresh Orders</button>
            <button id="cancelAllBtn" class="px-3 py-1.5 rounded-lg bg-rose-700 hover:bg-rose-600">Cancel All Pending</button>
          </div>
        </div>
        <div class="table-wrap">
          <table class="w-full text-sm">
            <thead class="text-slate-300">
              <tr class="border-b border-slate-700">
                <th class="text-left py-2">Created</th>
                <th class="text-left py-2">Finished</th>
                <th class="text-left py-2">Pair</th>
                <th class="text-left py-2">Side</th>
                <th class="text-left py-2">Type</th>
                <th class="text-right py-2">Qty</th>
                <th class="text-right py-2">Price</th>
                <th class="text-right py-2">Filled</th>
                <th class="text-right py-2">Avg Fill</th>
                <th class="text-left py-2">Status</th>
                <th class="text-left py-2">Action</th>
              </tr>
            </thead>
            <tbody id="ordersTableBody"></tbody>
          </table>
        </div>
      </div>
    </section>
  </div>

  <div id="settingsModal" class="hidden fixed inset-0 z-40 bg-black/60 p-4">
    <div class="max-w-md mx-auto mt-20 card rounded-2xl p-5">
      <h3 class="text-lg font-semibold mb-3">API Credentials</h3>
      <p class="text-xs muted mb-3">Stored in localStorage on this browser only.</p>
      <label class="block text-sm muted mb-1">API Key</label>
      <input id="apiKeyInput" class="w-full mb-3 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 mono" />
      <label class="block text-sm muted mb-1">API Secret</label>
      <input id="apiSecretInput" type="password" class="w-full mb-4 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 mono" />
      <div class="flex justify-end gap-2">
        <button id="closeSettingsBtn" class="px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600">Close</button>
        <button id="saveSettingsBtn" class="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500">Save</button>
      </div>
    </div>
  </div>

  <script>
    (() => {
      const BASE_URL = "https://mock-api.roostoo.com";
      const LS_KEY = "roostoo_api_key";
      const LS_SECRET = "roostoo_api_secret";
      const LS_INITIAL_WALLET = "roostoo_initial_wallet";
      const INITIAL_WALLET_BASE = 1000000;
      const LS_DAY_START_VALUE = "roostoo_day_start_value";
      const LS_DAY_MARK = "roostoo_day_mark";

      const state = {
        activeTab: "session1",
        pairs: [],
        exchangeInfo: null,
        apiInitialWallet: null,
        tickerMap: {},
        priceViewerInFlight: false,
        wallet: {},
        portfolioValue: null,
        pendingCount: 0,
        orders: [],
        chartPair: null,
        chart: null,
        chartSeries: [],
        tradeMarkers: [],
        intervals: [],
      };

      const el = {
        serverTime: document.getElementById("serverTime"),
        apiStatus: document.getElementById("apiStatus"),
        alertBox: document.getElementById("alertBox"),
        quickPair: document.getElementById("quickPair"),
        initialWallet: document.getElementById("initialWallet"),
        portfolioValue: document.getElementById("portfolioValue"),
        portfolioPnlPct: document.getElementById("portfolioPnlPct"),
        unrealizedToday: document.getElementById("unrealizedToday"),
        pvBTCPrice: document.getElementById("pvBTCPrice"),
        pvBTCChange: document.getElementById("pvBTCChange"),
        pvETHPrice: document.getElementById("pvETHPrice"),
        pvETHChange: document.getElementById("pvETHChange"),
        pvSOLPrice: document.getElementById("pvSOLPrice"),
        pvSOLChange: document.getElementById("pvSOLChange"),
        pvXPRPrice: document.getElementById("pvXPRPrice"),
        pvXPRChange: document.getElementById("pvXPRChange"),
        walletTableBody: document.getElementById("walletTableBody"),
        walletUpdatedAt: document.getElementById("walletUpdatedAt"),
        pendingCount: document.getElementById("pendingCount"),
        totalTrades: document.getElementById("totalTrades"),
        winRate: document.getElementById("winRate"),
        lastOrderTime: document.getElementById("lastOrderTime"),
        lastFilledTime: document.getElementById("lastFilledTime"),
        ordersTableBody: document.getElementById("ordersTableBody"),
        quickQty: document.getElementById("quickQty"),
        settingsModal: document.getElementById("settingsModal"),
        apiKeyInput: document.getElementById("apiKeyInput"),
        apiSecretInput: document.getElementById("apiSecretInput"),
      };

      function nowMs() {
        return Date.now();
      }

      function fmtNum(value, digits = 4) {
        if (!Number.isFinite(Number(value))) return "-";
        return Number(value).toLocaleString(undefined, { maximumFractionDigits: digits });
      }

      function fmtUsd(value, digits = 2) {
        if (!Number.isFinite(Number(value))) return "$-";
        return "$" + Number(value).toLocaleString(undefined, { maximumFractionDigits: digits, minimumFractionDigits: 2 });
      }

      function formatTs(ts) {
        const n = Number(ts);
        if (!Number.isFinite(n) || n <= 0) return "-";
        return new Date(n).toLocaleString();
      }

      function showAlert(message) {
        el.alertBox.textContent = message;
        el.alertBox.classList.remove("hidden");
      }

      function clearAlert() {
        el.alertBox.classList.add("hidden");
        el.alertBox.textContent = "";
      }

      function getApiCredentials() {
        return {
          apiKey: localStorage.getItem(LS_KEY) || "",
          secret: localStorage.getItem(LS_SECRET) || "",
        };
      }

      function openSettings() {
        const creds = getApiCredentials();
        el.apiKeyInput.value = creds.apiKey;
        el.apiSecretInput.value = creds.secret;
        el.settingsModal.classList.remove("hidden");
      }

      function closeSettings() {
        el.settingsModal.classList.add("hidden");
      }

      function sortedQuery(params) {
        const keys = Object.keys(params).filter((k) => params[k] !== undefined && params[k] !== null);
        keys.sort();
        return keys.map((k) => `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`).join("&");
      }

      function buildSignedPayload(inputParams = {}) {
        const { apiKey, secret } = getApiCredentials();
        if (!apiKey || !secret) {
          throw new Error("API credentials missing. Open API Settings and save your key/secret.");
        }
        const params = { ...inputParams, timestamp: nowMs() };
        const query = sortedQuery(params);
        const signature = CryptoJS.HmacSHA256(query, secret).toString(CryptoJS.enc.Hex);
        return {
          headers: {
            "RST-API-KEY": apiKey,
            "MSG-SIGNATURE": signature,
          },
          query,
          params,
        };
      }

      async function requestPublic(endpoint, params = {}) {
        const q = sortedQuery(params);
        const url = `${BASE_URL}${endpoint}${q ? `?${q}` : ""}`;
        const res = await fetch(url);
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          throw new Error(data?.Message || `${endpoint} failed with status ${res.status}`);
        }
        return data;
      }

      async function requestSigned(endpoint, method = "GET", params = {}, options = {}) {
        const signed = buildSignedPayload(params);
        const headers = { ...signed.headers };
        const upperMethod = method.toUpperCase();
        let url = `${BASE_URL}${endpoint}`;
        let body;

        if (upperMethod === "GET") {
          url += `?${signed.query}`;
        } else {
          headers["Content-Type"] = "application/x-www-form-urlencoded";
          body = signed.query;
        }

        const res = await fetch(url, { method: upperMethod, headers, body });
        const data = await res.json().catch(() => ({}));
        const allowSuccessFalse = options.allowSuccessFalse === true;
        if (!res.ok || (data?.Success === false && !allowSuccessFalse)) {
          throw new Error(data?.Message || `${endpoint} request failed`);
        }
        return data;
      }

      async function fetchServerTime() {
        const res = await requestPublic("/v3/serverTime");
        const t = res.serverTime || res.ServerTime || res.timestamp || res.Timestamp || nowMs();
        el.serverTime.textContent = new Date(Number(t)).toLocaleString();
        el.apiStatus.textContent = "Online";
        el.apiStatus.className = "mono text-emerald-300";
      }

      async function fetchExchangeInfo() {
        const res = await requestPublic("/v3/exchangeInfo");
        state.exchangeInfo = res;
        const tradePairsObj = res.TradePairs || res.Data?.TradePairs || {};
        const pairList = Object.keys(tradePairsObj || {});
        state.pairs = [...new Set(pairList)];
        if (!state.pairs.length) {
          throw new Error("No trading pairs found from /v3/exchangeInfo.");
        }
        const initialUsd = Number(res.InitialWallet?.USD ?? res.Data?.InitialWallet?.USD);
        state.apiInitialWallet = Number.isFinite(initialUsd) ? initialUsd : 1000000;
        renderPairSelectors();
      }

      async function fetchTicker(pair) {
        const res = await requestPublic("/v3/ticker", { pair, timestamp: nowMs() });
        const ticker = res.Data?.[pair] || res.data?.[pair] || res[pair] || {};
        state.tickerMap[pair] = ticker;
        return ticker;
      }

      async function fetchAllTickers() {
        const res = await requestPublic("/v3/ticker", { timestamp: nowMs() });
        const data = res.Data || {};
        if (data && typeof data === "object") {
          state.tickerMap = { ...state.tickerMap, ...data };
        }
      }

      async function fetchTickerByPair(pair) {
        const res = await requestPublic("/v3/ticker", { pair, timestamp: nowMs() });
        const ticker = res?.Data?.[pair];
        return ticker || null;
      }

      function renderPriceChange(elChange, changePct) {
        if (!Number.isFinite(changePct)) {
          elChange.textContent = "-%";
          elChange.className = "mono text-sm mt-1";
          return;
        }
        const sign = changePct >= 0 ? "+" : "";
        elChange.textContent = `${sign}${fmtNum(changePct, 2)}%`;
        elChange.className = `mono text-sm mt-1 ${changePct >= 0 ? "text-emerald-300" : "text-rose-300"}`;
      }

      async function refreshPriceViewer() {
        if (state.priceViewerInFlight) return;
        state.priceViewerInFlight = true;
        try {
          const targets = [
            { pair: "BTC/USD", priceEl: el.pvBTCPrice, changeEl: el.pvBTCChange },
            { pair: "ETH/USD", priceEl: el.pvETHPrice, changeEl: el.pvETHChange },
            { pair: "SOL/USD", priceEl: el.pvSOLPrice, changeEl: el.pvSOLChange },
          ];

          const xprTargets = [
            { pair: "XPR/USD", priceEl: el.pvXPRPrice, changeEl: el.pvXPRChange },
            { pair: "XRP/USD", priceEl: el.pvXPRPrice, changeEl: el.pvXPRChange },
          ];

          for (const t of targets) {
            const ticker = await fetchTickerByPair(t.pair);
            const price = Number(ticker?.LastPrice ?? ticker?.lastPrice ?? ticker?.Price ?? 0);
            const changePct = Number(ticker?.Change ?? ticker?.change ?? 0) * 100;
            if (price > 0) t.priceEl.textContent = fmtUsd(price, 8);
            else t.priceEl.textContent = "$-";
            renderPriceChange(t.changeEl, price > 0 ? changePct : NaN);
          }

          let used = false;
          for (const t of xprTargets) {
            if (used) break;
            const ticker = await fetchTickerByPair(t.pair);
            const price = Number(ticker?.LastPrice ?? ticker?.lastPrice ?? ticker?.Price ?? 0);
            if (price > 0) {
              const changePct = Number(ticker?.Change ?? ticker?.change ?? 0) * 100;
              t.priceEl.textContent = fmtUsd(price, 8);
              renderPriceChange(t.changeEl, changePct);
              used = true;
            }
          }
          if (!used) {
            el.pvXPRPrice.textContent = "$-";
            renderPriceChange(el.pvXPRChange, NaN);
          }
        } finally {
          state.priceViewerInFlight = false;
        }
      }

      async function fetchBalances() {
        const res = await requestSigned("/v3/balance", "GET");
        state.wallet = res.SpotWallet || res.Wallet || res.Data?.Wallet || {};
        renderWallet();
      }

      async function fetchPendingCount() {
        const res = await requestSigned("/v3/pending_count", "GET", {}, { allowSuccessFalse: true });
        state.pendingCount = Number(res.TotalPending ?? res.Data?.TotalPending ?? 0);
        el.pendingCount.textContent = fmtNum(state.pendingCount, 0);
      }

      async function fetchOrders(limit = 200) {
        const res = await requestSigned("/v3/query_order", "POST", { limit });
        const rows = res.OrderMatched || res.Data?.Orders || res.Orders || [];
        state.orders = Array.isArray(rows) ? rows : [];
        renderOrders();
        computeTradeStats();
      }

      async function placeMarketOrder(side) {
        const pair = el.quickPair.value;
        const quantity = Number(el.quickQty.value);
        if (!pair) throw new Error("Select a pair before placing an order.");
        if (!(quantity > 0)) throw new Error("Quantity must be greater than zero.");
        await requestSigned("/v3/place_order", "POST", {
          pair,
          side,
          type: "MARKET",
          quantity,
        });
        await Promise.all([fetchPendingCount(), fetchOrders(200), fetchBalances()]);
      }

      async function cancelOrder(orderId) {
        await requestSigned("/v3/cancel_order", "POST", { order_id: orderId });
      }

      function currentPortfolioValue() {
        let total = 0;
        Object.entries(state.wallet || {}).forEach(([coin, obj]) => {
          const free = Number(obj?.Free ?? obj?.free ?? 0);
          const locked = Number(obj?.Lock ?? obj?.Locked ?? obj?.lock ?? 0);
          const amount = free + locked;
          if (!Number.isFinite(amount)) return;
          if (coin === "USD" || coin === "USDT") {
            total += amount;
          } else {
            const pair1 = `${coin}/USD`;
            const pair2 = `${coin}/USDT`;
            const t = state.tickerMap[pair1] || state.tickerMap[pair2];
            const px = Number(t?.LastPrice ?? t?.lastPrice ?? t?.Price ?? 0);
            total += amount * (Number.isFinite(px) ? px : 0);
          }
        });
        return total;
      }

      function updatePnlCards() {
        const pv = currentPortfolioValue();
        state.portfolioValue = pv;
        const dayMark = new Date().toISOString().slice(0, 10);
        const storedDayMark = localStorage.getItem(LS_DAY_MARK);
        let dayStart = Number(localStorage.getItem(LS_DAY_START_VALUE));

        if (storedDayMark !== dayMark || !Number.isFinite(dayStart)) {
          localStorage.setItem(LS_DAY_MARK, dayMark);
          localStorage.setItem(LS_DAY_START_VALUE, String(pv));
          dayStart = pv;
        }

        const initialWallet = INITIAL_WALLET_BASE;
        const pnlPct = initialWallet > 0 ? ((pv - initialWallet) / initialWallet) * 100 : 0;
        const unrealizedToday = Number.isFinite(dayStart) ? pv - dayStart : 0;

        el.initialWallet.textContent = fmtUsd(initialWallet);
        el.portfolioValue.textContent = fmtUsd(pv);
        el.portfolioPnlPct.textContent = `${fmtNum(pnlPct, 2)}%`;
        el.portfolioPnlPct.className = `text-sm mono ${pnlPct >= 0 ? "text-emerald-300" : "text-rose-300"}`;
        el.unrealizedToday.textContent = fmtUsd(unrealizedToday);
        el.unrealizedToday.className = `text-3xl font-semibold mono ${unrealizedToday >= 0 ? "text-emerald-300" : "text-rose-300"}`;
      }

      function renderWallet() {
        const rows = [];
        Object.entries(state.wallet || {}).forEach(([coin, obj]) => {
          const free = Number(obj?.Free ?? obj?.free ?? 0);
          const locked = Number(obj?.Lock ?? obj?.Locked ?? obj?.lock ?? 0);
          const total = free + locked;
          let usdValue = 0;
          if (coin === "USD" || coin === "USDT") {
            usdValue = total;
          } else {
            const t = state.tickerMap[`${coin}/USD`] || state.tickerMap[`${coin}/USDT`];
            usdValue = total * Number(t?.LastPrice ?? t?.lastPrice ?? 0);
          }
          rows.push({ coin, free, locked, total, usdValue });
        });

        rows.sort((a, b) => b.usdValue - a.usdValue);
        el.walletTableBody.innerHTML = rows.map((r) => `
          <tr class="border-b border-slate-800">
            <td class="py-2">${r.coin}</td>
            <td class="py-2 text-right mono">${fmtNum(r.free, 8)}</td>
            <td class="py-2 text-right mono">${fmtNum(r.locked, 8)}</td>
            <td class="py-2 text-right mono">${fmtUsd(r.usdValue)}</td>
            <td class="py-2 text-right mono">${fmtNum(r.total, 8)}</td>
          </tr>
        `).join("");

        el.walletUpdatedAt.textContent = `Updated ${new Date().toLocaleTimeString()}`;
        updatePnlCards();
      }

      function normalizeOrder(order) {
        const createdTs = Number(order.CreateTimestamp ?? order.Time ?? order.CreateTime ?? order.Timestamp ?? order.UpdateTime ?? 0);
        const finishedTs = Number(order.FinishTimestamp ?? order.FinishTime ?? 0);
        const pair = order.Pair || order.pair || "-";
        const side = order.Side || order.side || "-";
        const type = order.Type || order.type || "-";
        const qty = Number(order.Quantity ?? order.quantity ?? 0);
        const price = Number(order.Price ?? order.price ?? 0);
        const filled = Number(order.FilledQuantity ?? order.filled ?? order.DealQuantity ?? 0);
        const avgFill = Number(order.FilledAverPrice ?? order.AvgFillPrice ?? order.avg_fill_price ?? 0);
        const status = order.Status || order.status || "-";
        const orderId = order.OrderID || order.OrderId || order.order_id || order.id || "";
        return {
          time: createdTs, // used for sorting
          createdTs,
          finishedTs,
          pair,
          side,
          type,
          qty,
          price,
          filled,
          avgFill,
          status,
          orderId,
        };
      }

      function renderOrders() {
        const normalized = state.orders.map(normalizeOrder).sort((a, b) => b.time - a.time);
        el.ordersTableBody.innerHTML = normalized.map((o) => `
          <tr class="border-b border-slate-800">
            <td class="py-2 mono">${formatTs(o.createdTs)}</td>
            <td class="py-2 mono">${formatTs(o.finishedTs)}</td>
            <td class="py-2">${o.pair}</td>
            <td class="py-2 ${o.side === "BUY" ? "text-emerald-300" : o.side === "SELL" ? "text-rose-300" : ""}">${o.side}</td>
            <td class="py-2">${o.type}</td>
            <td class="py-2 text-right mono">${fmtNum(o.qty, 8)}</td>
            <td class="py-2 text-right mono">${fmtNum(o.price, 8)}</td>
            <td class="py-2 text-right mono">${fmtNum(o.filled, 8)}</td>
            <td class="py-2 text-right mono">${fmtNum(o.avgFill, 8)}</td>
            <td class="py-2">${o.status}</td>
            <td class="py-2">
              ${String(o.status).toUpperCase().includes("PEND") && o.orderId
                ? `<button class="cancel-order px-2 py-1 rounded bg-rose-700 hover:bg-rose-600 text-xs" data-order-id="${o.orderId}">Cancel</button>`
                : "-"}
            </td>
          </tr>
        `).join("");
      }

      function computeTradeStats() {
        const normalized = state.orders.map(normalizeOrder);
        const completed = normalized.filter((o) => String(o.status).toUpperCase().includes("FILLED"));
        const totalTrades = completed.length;
        let wins = 0;
        completed.forEach((o) => {
          const px = o.avgFill || o.price;
          if (o.side === "SELL" && px > 0) wins += 1;
        });
        const winRate = totalTrades > 0 ? (wins / totalTrades) * 100 : 0;
        el.totalTrades.textContent = fmtNum(totalTrades, 0);
        el.winRate.textContent = `${fmtNum(winRate, 2)}%`;

        // Session 1: show latest order timestamps
        const lastCreated = normalized.reduce((m, o) => (o.createdTs > m ? o.createdTs : m), 0);
        const filledOnly = completed.length ? completed : [];
        const lastFilled = filledOnly.reduce((m, o) => (o.finishedTs > m ? o.finishedTs : m), 0) || 0;
        el.lastOrderTime.textContent = formatTs(lastCreated);
        el.lastFilledTime.textContent = formatTs(lastFilled);
      }

      function renderPairSelectors() {
        const options = state.pairs.map((p) => `<option value="${p}">${p}</option>`).join("");
        el.quickPair.innerHTML = options;
        if (!state.chartPair || !state.pairs.includes(state.chartPair)) {
          state.chartPair = state.pairs[0];
        }
        el.quickPair.value = state.chartPair;
      }

      function upsertCandlePoint(ts, price) {
        const minute = Math.floor(ts / 60000) * 60000;
        const last = state.chartSeries[state.chartSeries.length - 1];
        if (!last || last.t !== minute) {
          state.chartSeries.push({ t: minute, o: price, h: price, l: price, c: price });
          if (state.chartSeries.length > 300) state.chartSeries.shift();
        } else {
          last.h = Math.max(last.h, price);
          last.l = Math.min(last.l, price);
          last.c = price;
        }
      }

      function extractTradeMarkers(pair) {
        return state.orders
          .map(normalizeOrder)
          .filter((o) => o.pair === pair)
          .filter((o) => o.time && o.time > 0)
          .filter((o) => String(o.status).toUpperCase().includes("FILLED"))
          .map((o) => ({ x: o.time, y: o.avgFill || o.price, side: o.side }))
          .filter((m) => Number.isFinite(m.x) && m.x > 0 && Number.isFinite(m.y) && m.y > 0);
      }

      function initChart() {
        const ctx = document.getElementById("priceChart").getContext("2d");
        state.chart = new Chart(ctx, {
          type: "line",
          data: {
            datasets: [
              {
                label: "Price",
                data: [],
                borderColor: "#38bdf8",
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.15,
              },
              {
                label: "BUY fills",
                data: [],
                pointBackgroundColor: "#22c55e",
                pointBorderColor: "#22c55e",
                pointRadius: 4,
                showLine: false,
              },
              {
                label: "SELL fills",
                data: [],
                pointBackgroundColor: "#ef4444",
                pointBorderColor: "#ef4444",
                pointRadius: 4,
                showLine: false,
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                type: "time",
                time: { unit: "minute" },
                ticks: { color: "#94a3b8" },
                grid: { color: "rgba(51,65,85,0.35)" },
              },
              y: {
                ticks: { color: "#94a3b8" },
                grid: { color: "rgba(51,65,85,0.35)" },
              },
            },
            plugins: {
              legend: {
                labels: { color: "#cbd5e1" },
              },
            },
          }
        });
      }

      function refreshChartView() {
        if (!state.chart) return;
        const priceDataset = state.chartSeries.map((c) => ({ x: c.t, y: c.c }));
        const markers = extractTradeMarkers(state.chartPair);
        const buyMarkers = markers.filter((m) => m.side === "BUY").map((m) => ({ x: m.x, y: m.y }));
        const sellMarkers = markers.filter((m) => m.side === "SELL").map((m) => ({ x: m.x, y: m.y }));
        state.chart.data.datasets[0].data = priceDataset;
        state.chart.data.datasets[1].data = buyMarkers;
        state.chart.data.datasets[2].data = sellMarkers;
        state.chart.update();
      }

      async function updateChartTick() {
        if (!state.chartPair) return;
        const t = await fetchTicker(state.chartPair);
        const price = Number(t?.LastPrice ?? t?.lastPrice ?? t?.Price ?? 0);
        const change = Number(t?.Change ?? t?.change ?? 0) * 100;
        if (Number.isFinite(price) && price > 0) {
          upsertCandlePoint(nowMs(), price);
          el.livePrice.textContent = fmtUsd(price, 8);
        }
        el.liveChange.textContent = `${fmtNum(change, 2)}%`;
        el.liveChange.className = `mono ${change >= 0 ? "text-emerald-300" : "text-rose-300"}`;
        refreshChartView();
      }

      async function refreshCoreData() {
        clearAlert();
        try {
          await fetchServerTime();
          await fetchAllTickers();
          await Promise.all([fetchBalances(), fetchPendingCount(), fetchOrders(200)]);
        } catch (err) {
          el.apiStatus.textContent = "Error";
          el.apiStatus.className = "mono text-rose-300";
          showAlert(err.message || "Failed to refresh data.");
        }
      }

      function clearIntervals() {
        state.intervals.forEach((id) => clearInterval(id));
        state.intervals = [];
      }

      function setupIntervals() {
        clearIntervals();
        state.intervals.push(setInterval(() => fetchServerTime().catch((e) => showAlert(e.message)), 15000));
        state.intervals.push(setInterval(() => {
          Promise.all([fetchAllTickers(), fetchBalances(), fetchPendingCount(), fetchOrders(200)])
            .catch((e) => showAlert(e.message));
        }, 15000));
        state.intervals.push(setInterval(() => {
          if (state.activeTab === "session1") refreshPriceViewer().catch((e) => showAlert(e.message));
        }, 4000));
        state.intervals.push(setInterval(() => {
          if (state.activeTab === "session2") fetchOrders(200).catch((e) => showAlert(e.message));
        }, 4000));
      }

      function setActiveTab(tabId) {
        state.activeTab = tabId;
        document.querySelectorAll("[data-tab]").forEach((btn) => {
          btn.classList.toggle("active", btn.dataset.tab === tabId);
        });
        ["session1", "session2"].forEach((id) => {
          document.getElementById(id).classList.toggle("hidden", id !== tabId);
        });
      }

      function wireEvents() {
        document.querySelectorAll("[data-tab]").forEach((btn) => {
          btn.addEventListener("click", () => setActiveTab(btn.dataset.tab));
        });

        document.getElementById("settingsBtn").addEventListener("click", openSettings);
        document.getElementById("closeSettingsBtn").addEventListener("click", closeSettings);
        document.getElementById("saveSettingsBtn").addEventListener("click", () => {
          localStorage.setItem(LS_KEY, el.apiKeyInput.value.trim());
          localStorage.setItem(LS_SECRET, el.apiSecretInput.value.trim());
          closeSettings();
          refreshCoreData();
        });

        document.getElementById("refreshAllBtn").addEventListener("click", () => {
          refreshCoreData();
        });
        document.getElementById("refreshOrdersBtn").addEventListener("click", () => fetchOrders(200));

        document.getElementById("cancelAllBtn").addEventListener("click", async () => {
          try {
            const pending = state.orders.map(normalizeOrder).filter((o) => String(o.status).toUpperCase().includes("PEND") && o.orderId);
            for (const p of pending) {
              await cancelOrder(p.orderId);
            }
            await Promise.all([fetchOrders(200), fetchPendingCount()]);
          } catch (err) {
            showAlert(err.message || "Cancel all failed");
          }
        });

        el.ordersTableBody.addEventListener("click", async (e) => {
          const btn = e.target.closest(".cancel-order");
          if (!btn) return;
          try {
            await cancelOrder(btn.dataset.orderId);
            await Promise.all([fetchOrders(200), fetchPendingCount()]);
          } catch (err) {
            showAlert(err.message || "Cancel order failed");
          }
        });

      }

      async function bootstrap() {
        wireEvents();
        try {
          await fetchExchangeInfo();
          await refreshCoreData();
          setupIntervals();
        } catch (err) {
          showAlert(err.message || "Initialization failed");
          openSettings();
        }
      }

      bootstrap();
    })();
  </script>
</body>
</html>
