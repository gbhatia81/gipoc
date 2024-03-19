INSERT INTO `sample.BKPSalesNested`
(store_id, transaction_id, item, date)
VALUES
('STORE_1', 'TRANSACTION_1', 
  [
    STRUCT('ITEM_ID_1' AS item_id, 1 AS qty, 10.0 AS sale_price, 10.1 AS actual_sale_price),
    STRUCT('ITEM_ID_2' AS item_id, 2 AS qty, 20 AS sale_price, 19 AS actual_sale_price)
    -- Add more STRUCTs for additional items if needed
  ],
  TIMESTAMP('2024-01-01 09:00:00')
);
INSERT INTO `sample.BKPSalesNested`
(store_id, transaction_id, item, date)
VALUES
('STORE_1', 'TRANSACTION_2', 
  [
    STRUCT('ITEM_ID_1' AS item_id, 1 AS qty, 11.0 AS sale_price, 11.0 AS actual_sale_price),
    STRUCT('ITEM_ID_2' AS item_id, 2 AS qty, 22 AS sale_price, 22.0 AS actual_sale_price)
    -- Add more STRUCTs for additional items if needed
  ],
  TIMESTAMP('2024-01-01 09:10:00')
);
INSERT INTO `sample.BKPSalesNested`
(store_id, transaction_id, item, date)
VALUES
('STORE_2', 'TRANSACTION_3', 
  [
    STRUCT('ITEM_ID_3' AS item_id, 5 AS qty, 10.0 AS sale_price, 11.0 AS actual_sale_price),
    STRUCT('ITEM_ID_4' AS item_id, 6 AS qty, 11 AS sale_price, 12.0 AS actual_sale_price)
    -- Add more STRUCTs for additional items if needed
  ],
  TIMESTAMP('2024-01-02 09:20:00')
);

