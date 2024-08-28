const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const PORT = 1245;
const HOST = '127.0.0.1';

const client = redis.createClient();
const hgetAsync = promisify(client.hget).bind(client);
const hsetAsync = promisify(client.hset).bind(client);

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

function getItemById(id) {
  return listProducts.find(item => item.id === parseInt(id, 10));
}

app.get('/list_products', (req, res) => {
  const products = listProducts.map(item => ({
    itemId: item.id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock
  }));
  res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  try {
    const reservedStock = await getCurrentReservedStockById(itemId);
    const currentQuantity = item.stock - (reservedStock || 0);
    res.json({
      itemId: item.id,
      itemName: item.name,
      price: item.price,
      initialAvailableQuantity: item.stock,
      currentQuantity
    });
  } catch (error) {
    res.status(500).json({ status: 'Internal server error' });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  try {
    const reservedStock = await getCurrentReservedStockById(itemId);
    const currentQuantity = item.stock - (reservedStock || 0);

    if (currentQuantity <= 0) {
      return res.json({ status: 'Not enough stock available', itemId });
    }

    await reserveStockById(itemId, (reservedStock || 0) + 1);
    res.json({ status: 'Reservation confirmed', itemId });
  } catch (error) {
    res.status(500).json({ status: 'Internal server error' });
  }
});

async function reserveStockById(itemId, stock) {
  await hsetAsync(`item.${itemId}`, 'reserved_stock', stock);
}

async function getCurrentReservedStockById(itemId) {
  const reservedStock = await hgetAsync(`item.${itemId}`, 'reserved_stock');
  return parseInt(reservedStock, 10) || 0;
}

app.listen(PORT, HOST, () => {
  console.log(`Server running on http://${HOST}:${PORT}`);
});
