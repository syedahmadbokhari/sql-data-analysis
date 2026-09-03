let products = [];
let visibleProducts = [];
let selectedProduct = null;
let cart = [];

const listEl = document.getElementById("product-list");
const detailEl = document.getElementById("detail-panel");
const searchEl = document.getElementById("search");
const brandFilterEl = document.getElementById("brand-filter");
const cartCountEl = document.getElementById("cart-count");
const trackingStatusEl = document.getElementById("tracking-status");

function trackingEnabled() {
  return Boolean(window.RETAIL_ANALYTICS_CONFIG.gtmContainerId);
}

function pushEvent(eventName, ecommerce = {}, extra = {}) {
  const payload = {
    event: eventName,
    ecommerce,
    demo_data_notice: "synthetic/demo interaction from portfolio retail demo",
    ...extra,
  };
  window.dataLayer.push(payload);
  return payload;
}

function itemPayload(product, index) {
  return {
    item_id: product.item_id,
    item_name: product.item_name,
    item_brand: product.item_brand,
    item_category: product.item_category,
    price: product.price,
    discount: product.discount,
    index,
  };
}

function renderProducts() {
  listEl.innerHTML = "";
  visibleProducts.forEach((product, index) => {
    const article = document.createElement("article");
    article.className = "product-card";
    article.innerHTML = `
      <p class="eyebrow">${product.item_brand}</p>
      <h2>${product.item_name}</h2>
      <div class="metric-row"><span>Price</span><strong>GBP ${product.price.toFixed(2)}</strong></div>
      <div class="metric-row"><span>Discount</span><strong>${Math.round(product.discount * 100)}%</strong></div>
      <button type="button" data-product-id="${product.item_id}">View product</button>
    `;
    article.querySelector("button").addEventListener("click", () => selectProduct(product, index));
    listEl.appendChild(article);
  });

  pushEvent("view_item_list", {
    item_list_id: "retail_demo_top_products",
    item_list_name: "Retail demo top products",
    items: visibleProducts.map(itemPayload),
  });
}

function renderDetail(product) {
  detailEl.innerHTML = `
    <p class="eyebrow">${product.item_brand}</p>
    <h2>${product.item_name}</h2>
    <div class="metric-row"><span>Product ID</span><strong>${product.item_id}</strong></div>
    <div class="metric-row"><span>Category</span><strong>${product.item_category}</strong></div>
    <div class="metric-row"><span>Price</span><strong>GBP ${product.price.toFixed(2)}</strong></div>
    <div class="metric-row"><span>Historic revenue</span><strong>GBP ${product.revenue.toLocaleString()}</strong></div>
    <button id="add-to-cart" type="button">Add to cart</button>
    <button id="begin-checkout" type="button">Begin checkout</button>
  `;
  document.getElementById("add-to-cart").addEventListener("click", () => addToCart(product));
  document.getElementById("begin-checkout").addEventListener("click", beginCheckout);
}

function selectProduct(product, index) {
  selectedProduct = product;
  pushEvent("select_item", {
    item_list_id: "retail_demo_top_products",
    item_list_name: "Retail demo top products",
    items: [itemPayload(product, index)],
  });
  pushEvent("view_item", {
    currency: "GBP",
    value: product.price,
    items: [itemPayload(product, index)],
  });
  renderDetail(product);
}

function addToCart(product) {
  cart.push(product);
  cartCountEl.textContent = String(cart.length);
  pushEvent("add_to_cart", {
    currency: "GBP",
    value: product.price,
    items: [{...itemPayload(product, 0), quantity: 1}],
  });
}

function beginCheckout() {
  const checkoutItems = cart.length ? cart : selectedProduct ? [selectedProduct] : [];
  if (!checkoutItems.length) return;
  pushEvent("begin_checkout", {
    currency: "GBP",
    value: checkoutItems.reduce((total, item) => total + item.price, 0),
    items: checkoutItems.map((product, index) => ({...itemPayload(product, index), quantity: 1})),
  });
}

function applyFilters() {
  const query = searchEl.value.trim().toLowerCase();
  const brand = brandFilterEl.value;
  visibleProducts = products.filter((product) => {
    const matchesSearch = !query ||
      product.item_name.toLowerCase().includes(query) ||
      product.item_brand.toLowerCase().includes(query);
    const matchesBrand = !brand || product.item_brand === brand;
    return matchesSearch && matchesBrand;
  });
  if (brand) {
    pushEvent("filter_applied", {items: []}, {filter_name: "brand", filter_value: brand});
  }
  renderProducts();
}

searchEl.addEventListener("change", () => {
  if (searchEl.value.trim()) {
    pushEvent("search", {}, {search_term: searchEl.value.trim()});
  }
  applyFilters();
});
brandFilterEl.addEventListener("change", applyFilters);

fetch("/products.json")
  .then((response) => response.json())
  .then((data) => {
    products = data;
    visibleProducts = data;
    [...new Set(products.map((product) => product.item_brand))].sort().forEach((brand) => {
      const option = document.createElement("option");
      option.value = brand;
      option.textContent = brand;
      brandFilterEl.appendChild(option);
    });
    trackingStatusEl.textContent = trackingEnabled()
      ? "GTM enabled from environment config"
      : "GTM disabled until GTM_CONTAINER_ID is set";
    renderProducts();
  });
