-- ----------------------------------------------------------------------------------------------------------------------------------
-- #1
CREATE TABLE `customer_stg` (
  `customeremail` varchar(100) NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `accountdate` datetime DEFAULT NULL,
  PRIMARY KEY (`customeremail`),
  UNIQUE KEY `customerEmail_UNIQUE` (`customeremail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Legacy Customer Info - Staging table';

-- ----------------------------------------------------------------------------------------------------------------------------------
-- #2
CREATE TABLE `transaction_stg` (
  `tranid` varchar(45) NOT NULL,
  `customer_email` varchar(100) NOT NULL,
  `order_date` datetime NOT NULL,
  `line_num` int NOT NULL,
  `product` varchar(45) NOT NULL,
  `quantity` int NOT NULL,
  `color` varchar(50) DEFAULT NULL,
  `item_size` varchar(45) DEFAULT NULL,
  `total_price` decimal(5,2) DEFAULT NULL,
  KEY `custemail_idx` (`customer_email`),
  KEY `product_idx` (`product`),
  KEY `tranid_idx` (`tranid`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Transaction data staging table';

-- ----------------------------------------------------------------------------------------------------------------------------------
-- #3
CREATE TABLE `customer_dim` (
  `custid` int NOT NULL AUTO_INCREMENT,
  `customerEmail` varchar(100) NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `accountdate` datetime DEFAULT NULL,
  PRIMARY KEY (`custid`),
  UNIQUE KEY `customerEmail_UNIQUE` (`customerEmail`),
  UNIQUE KEY `custid_UNIQUE` (`custid`)
) ENGINE=InnoDB AUTO_INCREMENT=16384 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Customer data dimension table';

-- ----------------------------------------------------------------------------------------------------------------------------------
-- #4
CREATE TABLE `product_dim` (
  `productid` int NOT NULL AUTO_INCREMENT,
  `product` varchar(45) NOT NULL,
  `color` varchar(50) DEFAULT NULL,
  `item_size` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`productid`),
  UNIQUE KEY `prodid_UNIQUE` (`productid`),
  UNIQUE KEY `product_UNIQUE` (`product`)
) ENGINE=InnoDB AUTO_INCREMENT=256 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='product data dimension table';

-- ----------------------------------------------------------------------------------------------------------------------------------
-- #5
CREATE TABLE `order_f` (
  `trannum` int NOT NULL AUTO_INCREMENT,
  `tranid` varchar(45) NOT NULL,
  `custid` int DEFAULT NULL,
  `order_date` datetime NOT NULL,
  `line_num` int NOT NULL,
  `productid` int DEFAULT NULL,
  `quantity` int NOT NULL,
  `total_price` decimal(5,2) NOT NULL,
  PRIMARY KEY (`trannum`),
  UNIQUE KEY `prodid_UNIQUE` (`trannum`),
  KEY `custid_idx` (`custid`),
  KEY `productid_idx` (`productid`),
  CONSTRAINT `custid` FOREIGN KEY (`custid`) REFERENCES `customer_dim` (`custid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `productid` FOREIGN KEY (`productid`) REFERENCES `product_dim` (`productid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=131071 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='product data fact table';

-- ----------------------------------------------------------------------------------------------------------------------------------
