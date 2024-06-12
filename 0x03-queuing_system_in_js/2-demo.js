import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();
const addAsync = promisify(client.get).bind(client);

client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, res) => {
    console.log(res);
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

//(async() => {
//  await displaySchoolValue('Holberton');
//  setNewSchool('HolbertonSanFrancisco', '100');
//  await displaySchoolValue('HolbertonSanFrancisco');
//})();
