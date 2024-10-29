
        /* Deletion of data */
        DELETE FROM Orders WHERE purchase_date > '2024-09-30';
        /* Confirmation */
        SELECT * FROM Orders WHERE purchase_date > '2024-09-30';
        