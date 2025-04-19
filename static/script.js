const BASE_URL = "http://localhost:8083";

function register() {
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;
    fetch(`${BASE_URL}/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}

function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(({status, body}) => {
        alert(body.message);
        if (status === 200) window.location.href = "dashboard.html";
    });
}

function calculate() {
    const data = {
        username: document.getElementById("calc-username").value,
        password: document.getElementById("calc-password").value,
        operation: document.getElementById("operation").value,
        operand1: parseFloat(document.getElementById("operand1").value),
        operand2: parseFloat(document.getElementById("operand2").value)
    };
    fetch(`${BASE_URL}/calculate`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = data.result || data.message;
    });
}

function viewHistory() {
    const data = {
        username: document.getElementById("history-username").value,
        password: document.getElementById("history-password").value
    };
    fetch(`${BASE_URL}/history`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("history-result").innerText = JSON.stringify(data, null, 2);
    });
}

function clearHistory() {
    const data = {
        username: document.getElementById("clear-username").value,
        password: document.getElementById("clear-password").value
    };
    fetch(`${BASE_URL}/clear-history`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("clear-result").innerText = data.message;
    });
}
