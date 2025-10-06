async function run() {
  const algo = document.getElementById('algo').value;
  const rows = parseInt(document.getElementById('rows').value);
  const cols = parseInt(document.getElementById('cols').value);
  const obs = parseInt(document.getElementById('obs').value);

  const res = await fetch('https://YOUR-BACKEND-URL.onrender.com/simulate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      algorithm: algo,
      grid_size: [rows, cols],
      num_obstacles: obs
    })
  });

  const data = await res.json();
  animate(data.frames);
}

function animate(frames) {
  const canvas = document.getElementById('grid');
  const ctx = canvas.getContext('2d');
  const nrows = frames[0].length;
  const ncols = frames[0][0].length;
  const cell = canvas.width / ncols;
  let i = 0;
  const interval = setInterval(() => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let r=0; r<nrows; r++) {
      for (let c=0; c<ncols; c++) {
        ctx.fillStyle = frames[i][r][c] === 1 ? 'black' : frames[i][r][c] === 2 ? 'blue' : 'white';
        ctx.fillRect(c*cell, r*cell, cell, cell);
      }
    }
    i++;
    if (i >= frames.length) clearInterval(interval);
  }, 250);
}
