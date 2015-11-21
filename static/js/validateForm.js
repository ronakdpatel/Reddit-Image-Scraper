(function() {
  'use strict';
  function validateForm() {
    var form = document.getElementById('form');
    var input = document.getElementById('num-of-submissions');
    var submissions = input.value;
    var errorSymbol = document.getElementById('error-symbol');
    var errorMessage = document.getElementById('error-message');
    if (/\D/.test(submissions)) {
      errorSymbol.textContent = '\u2718'; 
      errorMessage.textContent = 'Please enter a number from 1-100';
      input.classList.add('error-box');
      return false;
    }
    errorSymbol.textContent = '';
    errorMessage.textContent = '';
    input.classList.remove('error-box');
    return true; 
  };
  form.addEventListener('submit',function (e) {
    if (validateForm()){
    }
    else{
      e.preventDefault(validateForm());
    }
  });
})();