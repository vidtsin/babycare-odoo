def migrate(cr, version):
    cr.execute(
        "UPDATE product_category SET sequence = 1 WHERE sequence IS NULL")
    cr.execute(
        """
        UPDATE product_category pc
        SET parent_sequence = parent.sequence
        FROM product_category parent
        WHERE pc.parent_id = parent.id
        """)
