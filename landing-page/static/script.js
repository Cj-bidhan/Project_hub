function updateClock() {
  const now = new Date();
  const sec = now.getSeconds();
  const min = now.getMinutes();
  const hr = now.getHours();

  document.getElementById("second-hand").style.transform = `rotate(${sec * 6}deg)`;
  document.getElementById("minute-hand").style.transform = `rotate(${min * 6 + sec * 0.1}deg)`;
  document.getElementById("hour-hand").style.transform = `rotate(${hr * 30 + min * 0.5}deg)`;

  const timeText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  const dateText = now.toLocaleDateString([], { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });

  document.getElementById("time-text").textContent = timeText;
  document.getElementById("date-text").textContent = dateText;
}

setInterval(updateClock, 1000);
updateClock();
