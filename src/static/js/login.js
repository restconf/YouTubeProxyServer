$("body > form:nth-child(2) > p:nth-child(3) > input:nth-child(1)").click(function (e) {
  if ($("body > form:nth-child(2) > p:nth-child(1) > input:nth-child(2)").val() == "" ||
    $("body > form:nth-child(2) > p:nth-child(2) > input:nth-child(2)").val() == "") {
    alert('This or these field must have a value');
    return false;
  }
});