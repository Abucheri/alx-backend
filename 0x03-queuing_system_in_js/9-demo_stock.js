import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

// Array of products
const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

// Function to get item by itemId
function getItemById(itemId) {
  return listProducts.find((item) => item.itemId === itemId);
}

// Redis client setup
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

client.on('error', (error) => {
  console.error(`Redis client error: ${error}`);
});

// Express setup
const app = express();
const port = 1245;

app.use(express.json());

// Endpoint to list all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Endpoint to get product details by itemId
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.json({ status: 'Product not found' });
    return;
  }

  try {
    const currentStock = await getAsync(`item.${itemId}`);
    const stock = currentStock !== null ? parseInt(currentStock) : item.initialAvailableQuantity;

    res.json({
      itemId: item.itemId,
      itemName: item.itemName,
      price: item.price,
      initialAvailableQuantity: item.initialAvailableQuantity,
      currentQuantity: stock,
    });
  } catch (error) {
    console.error(`Error retrieving stock for item ${itemId}: ${error}`);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Endpoint to reserve product by itemId
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.json({ status: 'Product not found' });
    return;
  }

  try {
    let currentStock = await getAsync(`item.${itemId}`);

    if (currentStock === null) {
      currentStock = item.initialAvailableQuantity;
    } else {
      currentStock = parseInt(currentStock);
    }

    if (currentStock <= 0) {
      res.json({ status: 'Not enough stock available', itemId });
      return;
    }

    await setAsync(`item.${itemId}`, currentStock - 1);
    res.json({ status: 'Reservation confirmed', itemId });
  } catch (error) {
    console.error(`Error reserving stock for item ${itemId}: ${error}`);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
