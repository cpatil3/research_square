-- # Average Monthly Sales By City --

WITH tbl_summ AS(
			SELECT cust.city, cust.state, DATE_FORMAT(ord.order_date, '%m-%Y') AS orderdate_MY, SUM(ord.total_price) AS total_pr
			FROM
				order_f ord
					INNER JOIN
				customer_dim cust ON ord.custid = cust.custid
					INNER JOIN
				product_dim prod ON ord.productid = prod.productid
			WHERE
				YEAR(ord.order_date) = '2021'
			GROUP BY cust.city , cust.state , orderdate_MY
			ORDER BY cust.city , cust.state , orderdate_MY
            )
SELECT city, state, SUM(total_pr) AS total_sales, CAST(AVG(total_pr) AS DECIMAL (10,2)) AS monthly_avg_sales
FROM
    tbl_summ
GROUP BY city , state
ORDER BY city , state
;