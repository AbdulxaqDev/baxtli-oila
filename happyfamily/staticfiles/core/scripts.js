function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrfToken = getCookie("csrftoken");``

function enableEdit(id) {
  document
    .querySelectorAll(".row-" + id + " input, .row-" + id + " select")
    .forEach((el) => {
      el.removeAttribute("readonly");
      el.removeAttribute("disabled");
      el.classList.add("editing");
    });

  document.getElementById("edit-" + id).classList.add("d-none");
  document.getElementById("save-" + id).classList.remove("d-none");
  document.getElementById("cancel-" + id).classList.remove("d-none");
}

function cancelEdit(id) {
  // Optionally revert changes here before resetting
  document
    .querySelectorAll(".row-" + id + " input, .row-" + id + " select")
    .forEach((el) => {
      el.setAttribute("readonly", true);
      el.setAttribute("disabled", true);
      el.classList.remove("editing");
    });
  location.reload();
}

function deleteStudent(id) {
  if (confirm("Are you sure you want to delete this student?")) {
    fetch(`/delete_student/${id}/`, {
      method: "POST",
      credentials: "same-origin",
      headers: { "X-CSRFToken": csrfToken },
    }).then(() => location.reload());
  }
}

function saveStudent(id) {
  const data = {};
  document.querySelectorAll(".row-" + id + " input").forEach((input) => {
    data[input.name] = input.value;
  });

  fetch(`/update_student/${id}/`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(data),
  }).then(() => {
    document
      .querySelectorAll(".row-" + id + " input, .row-" + id + " select")
      .forEach((el) => {
        el.setAttribute("readonly", true);
        el.setAttribute("disabled", true);
        el.classList.remove("editing");
      });
    location.reload();
  });
}

function saveUser(id) {
  const userId = document.querySelector(`.row-${id} [name="userId"]`).value;
  const role = document.querySelector(`.row-${id} [name="role"]`).value;

  fetch(`/update_user/${id}/`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ userId, role }),
  }).then(() => location.reload());
}

function deleteUser(id) {
  if (confirm("Are you sure you want to delete this user?")) {
    fetch(`/delete_user/${id}/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    }).then(() => location.reload());
  }
}
