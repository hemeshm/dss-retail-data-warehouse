-- triggers.sql
USE retail_dss0;

-- 1) Drop any old triggers
DROP TRIGGER IF EXISTS insert_customer;
DROP TRIGGER IF EXISTS insert_employee;
DROP TRIGGER IF EXISTS insert_product;
DROP TRIGGER IF EXISTS insert_payment;

-- 2) Define new triggers with proper schema references
DELIMITER $$

CREATE TRIGGER insert_customer
AFTER INSERT ON customers
FOR EACH ROW
BEGIN
  INSERT INTO dwh_customers
    (customer_id, first_name, last_name, full_name, country_id, credit_provider_id)
  VALUES
    (NEW.customer_id,
     NEW.first_name,
     NEW.last_name,
     NEW.full_name,
     NEW.country_id,
     NEW.credit_provider_id);
END$$

CREATE TRIGGER insert_employee
AFTER INSERT ON employees
FOR EACH ROW
BEGIN
  INSERT INTO dwh_employees
    (employee_id, first_name, last_name, full_name, city, department_id)
  VALUES
    (NEW.employee_id,
     NEW.first_name,
     NEW.last_name,
     NEW.full_name,
     NEW.city,
     NEW.department_id);
END$$

CREATE TRIGGER insert_product
AFTER INSERT ON products
FOR EACH ROW
BEGIN
  INSERT INTO dwh_products
    (product_id, Product_Name, Alcohol_Percent, Alcohol_Amount, Alcohol_Price)
  VALUES
    (NEW.product_id,
     NEW.Product_Name,
     NEW.Alcohol_Percent,
     NEW.Alcohol_Amount,
     NEW.Alcohol_Price);
END$$

CREATE TRIGGER insert_payment
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
  INSERT INTO dwh_fact
    (payment_id, Date_key, customer_id, employee_id, product_id, price)
  SELECT
    NEW.payment_id,
    d.Date_key,
    NEW.customer_id,
    NEW.employee_id,
    NEW.product_id,
    NEW.price
  FROM dwh_date AS d
  WHERE d.Dates = NEW.date;
END$$

DELIMITER ;

-- 3) List triggers to confirm
SHOW TRIGGERS;
