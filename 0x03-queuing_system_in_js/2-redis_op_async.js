import redis from 'redis';
import { promisify } from 'util';

// Create a Redis client
const client = redis.createClient();

// Event listener for successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for connection errors
client.on('error', (err) => {
  console.error('Redis client not connected to the server:', err.message);
});

/**
 * Sets a new school name and value in Redis.
 * @param {string} schoolName - The key for the school name.
 * @param {string} value - The value to set for the school name.
 */
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Promisify the get function
const getAsync = promisify(client.get).bind(client);

/**
 * Displays the value of a given school name from Redis.
 * @param {string} schoolName - The key for the school name to get the value of.
 */
async function displaySchoolValue(schoolName) {
  try {
    const reply = await getAsync(schoolName);
    console.log(reply);
  } catch (err) {
    console.error(err);
  }
}

// Call the functions to test them
async function testRedisOperations() {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  setTimeout(async () => {
    await displaySchoolValue('HolbertonSanFrancisco');
  }, 100);
}

testRedisOperations();
