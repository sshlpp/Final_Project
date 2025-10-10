function showTab(tabName) {
  document.getElementById("sallesTab").style.display =
    tabName === "salles" ? "block" : "none";
  document.getElementById("ordersTab").style.display =
    tabName === "orders" ? "block" : "none";

  document
    .getElementById("salles")
    .classList.toggle("activeTab", tabName === "salles");
  document
    .getElementById("orders")
    .classList.toggle("activeTab", tabName === "orders");
}
