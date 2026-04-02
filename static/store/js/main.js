/* iEmporium Gadgets — main.js */

document.addEventListener('DOMContentLoaded', function () {

  // ---- Product Detail: Image Gallery Swap ----
  const mainImg = document.getElementById('main-product-img');
  const thumbs = document.querySelectorAll('.thumb');

  if (mainImg && thumbs.length) {
    thumbs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        mainImg.src = thumb.dataset.full;
        mainImg.alt = thumb.dataset.alt || '';
        thumbs.forEach(function (t) { t.classList.remove('active'); });
        thumb.classList.add('active');
      });
    });
  }

  // ---- Quantity Stepper ----
  document.querySelectorAll('.qty-plus').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var input = btn.closest('.qty-control').querySelector('input[type=number]');
      var max = parseInt(input.max) || 99;
      var val = parseInt(input.value) || 1;
      if (val < max) input.value = val + 1;
    });
  });

  document.querySelectorAll('.qty-minus').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var input = btn.closest('.qty-control').querySelector('input[type=number]');
      var val = parseInt(input.value) || 1;
      if (val > 1) input.value = val - 1;
    });
  });

  // ---- Checkout: Bank Transfer Details Toggle ----
  var paymentRadios = document.querySelectorAll('input[name="payment_method"]');
  var bankBox = document.getElementById('bank-details-box');

  function toggleBank() {
    var selected = document.querySelector('input[name="payment_method"]:checked');
    if (bankBox) {
      bankBox.style.display = (selected && selected.value === 'bank') ? 'block' : 'none';
    }
  }

  paymentRadios.forEach(function (radio) {
    radio.addEventListener('change', toggleBank);
  });

  toggleBank(); // run on load

  // ---- Cart: Inline Quantity Form Auto-Submit ----
  document.querySelectorAll('.cart-qty-input').forEach(function (input) {
    input.addEventListener('change', function () {
      input.closest('form').submit();
    });
  });

});
