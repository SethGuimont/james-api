SELECT_ALL_POSTS = "SELECT * FROM menu_item;"
INSERT_MENUITEM_RETURN_ID = "INSERT INTO menu_item (name, description) VALUES (%s, %s) RETURNING id;"
DELETE_MENUITEM_BY_ID = "DELETE FROM menu_item WHERE id = (%s)"
