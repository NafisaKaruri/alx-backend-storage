-- Creates a trigger that decreases the quality of an item after adding a new order.
CREATE TRIGGER order_trigger
AFTER INSERT ON orders
FOR EACH ROW
	UPDATE items
	SET quality = quality - NEW.number
	WHERE name = NEW.item_name;
