import express from 'express';
import { createClient } from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';

const app = express();
const PORT = 1245;
const HOST = '127.0.0.1';
const client = createClient();
const queue = createQueue();

const hsetAsync = promisify(client.set).bind(client);
const hgetAsync = promisify(client.get).bind(client);

let reservationEnabled = true;
const INITIAL_SEATS = 50;

async function reserveSeat(number) {
  await hsetAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const availableSeats = await hgetAsync('available_seats');
  return parseInt(availableSeats, 10) || 0;
}

reserveSeat(INITIAL_SEATS);

app.use(express.json());

app.get('/available_seats', async (req, res) => {
  try {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
  } catch (error) {
    res.status(500).json({ status: 'Internal server error' });
  }
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', (result) => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      const currentSeats = await getCurrentAvailableSeats();
      if (currentSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }

      await reserveSeat(currentSeats - 1);
      done();
    } catch (error) {
      done(error);
    }
  });
});

app.listen(PORT, HOST, () => {
  console.log(`Server running on http://${HOST}:${PORT}`);
});
