function email_validator(email) {
  email = email.toLocaleLowerCase();
  const pattern1 = /[\.\@\-]{2,}/;
  let isvalid = email.search(pattern1);

  if (isvalid !== -1) return false;

  const pattern2 =
    /^[a-z][a-z\.\d]{1,}[a-z\d]\@(?:[a-z]|[a-z][a-z\d\-]{0,}[a-z\d]{1,})\.((?:[a-z]{2,}[\.\-]{0,1}[a-z]{2,}|[a-z]{2,}))$/;
  isvalid = email.search(pattern2);

  if (isvalid) return false;

  return true;
}

function password_validator(password) {
  password = password;
  const pattern1 = /^[a-zA-Z0-9\@\$\^\(\)\?\~\.\/]{8,30}$/;
  let isvalid = password.search(pattern1);

  if (isvalid !== 0) return false;

  const pattern2 = /[A-Z]+/;
  const pattern3 = /[a-z]+/;
  const pattern4 = /[0-9]+/;
  const pattern5 = /[\@\$\^\(\)\?\~\.\/\&\*\+\-]+/;

  if (password.search(pattern2) === -1) return false;
  if (password.search(pattern3) === -1) return false;
  if (password.search(pattern4) === -1) return false;
  if (password.search(pattern5) === -1) return false;
  
  return true;
}
