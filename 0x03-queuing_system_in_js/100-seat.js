import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

// Redis Client Setup
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to reserve a seat
async function reserveSeat(number) {
  await setAsync('available_seats', number.toString());
}

// Function to get the current number of available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats) || 0;
}

// Initialize available seats and reservation status
reserveSeat(50);
let reservationEnabled = true;

// Kue Queue Setup
const queue = kue.createQueue();

// Express App Setup
const app = express();
const port = 1245;

// Route to get current number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });
});

// Route to process the reservation queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    let currentAvailableSeats = await getCurrentAvailableSeats();
    if (currentAvailableSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      currentAvailableSeats--;
      await reserveSeat(currentAvailableSeats);
      if (currentAvailableSeats === 0) {
        reservationEnabled = false;
      }
      // console.log(`Seat reservation job ${job.id} completed`);
      done();
    }
  });
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
